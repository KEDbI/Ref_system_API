import string
import secrets

from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import NoResultFound

from app.api.schemas.ref_system import GetRefLinkByEmailResponse, GetRefLinkByEmail, GetReferralsById, UpdateRefLink
from app.api.schemas.users import RegisterUser, UserResponse
from app.utils.unitofwork import IUnitOfWork
from app.core.security import create_jwt

class RefSystemService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @staticmethod
    async def _generate_ref_link(login: str, length: int = 22) -> str:
        characters = string.ascii_letters + string.digits
        return "".join(secrets.choice(characters) for _ in range(length)) + ':' + login

    @staticmethod
    async def _get_referrer_login_from_link(ref_link: str):
        login = ''
        for i in ref_link[::-1]:
            if i == ':':
                break
            login += i
        return login[::-1]


    async def register_user(self, user: RegisterUser) -> UserResponse:
        async with self.uow:
            # проверка наличия логина в бд
            user_db = await self.uow.users.select_one({'login': user.login})
            if user_db:
                raise HTTPException(status_code=400, detail='This login already exists!')

            user.password = pbkdf2_sha256.hash(user.password)
            user_dict = user.model_dump()
            # проверка наличия реферальной ссылки
            if user_dict['ref_link']:
                user_dict['ref_link'] = self._get_referrer_login_from_link(user_dict['ref_link'])
                referrer = await self.uow.users.select_one({'login': user_dict['login']})
                referrer_id = referrer['id']
                user_dict['ref_link'] = referrer_id

            user_to_db = await self.uow.users.insert_one(user_dict)
            user_response = UserResponse.model_validate(user_to_db)
            await self.uow.commit()
            return user_response

    async def get_jwt(self, user_data: OAuth2PasswordRequestForm) -> str:
        async with self.uow:
            user_db = await self.uow.users.select_one({'login': user_data.username})
            if user_db is None or not pbkdf2_sha256.verify(user_data.password, user_db.password):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid login or password",
                    headers={"WWW-Authenticate": "Bearer"})
            data_for_jwt = {'sub': user_db.login}
            return create_jwt(data_for_jwt)

    async def update_ref_link(self, user: str,
                              ref_link_exp_days: UpdateRefLink) -> UserResponse:
        async with self.uow:
            exp_days_dict = ref_link_exp_days.model_dump()
            update_ref = await self.uow.users.update_one(filters={'login': user},
                                                             data={'ref_link': self._generate_ref_link(login=user),
                                                                   **exp_days_dict})
            response = UserResponse.model_validate(update_ref)
            await self.uow.commit()
            return response

    async def delete_ref_link(self, user: str) -> UserResponse:
        async with self.uow:
            delete_ref = await self.uow.users.update_one(filters={'login': user},
                                                         data={'ref_link': None,
                                                         'ref_link_exp': None})
            response = UserResponse.model_validate(delete_ref)
            await self.uow.commit()
            return response

    async def get_ref_link_by_email(self, email: GetRefLinkByEmail) -> GetRefLinkByEmailResponse:
        async with self.uow:
            email_dict = email.model_dump()
            get_ref_link = await self.uow.users.select_one(filters=email_dict)
            if get_ref_link:
                response = GetRefLinkByEmailResponse.model_validate(get_ref_link)
                return response
            raise HTTPException(status_code=403, detail="Such email doesn't exist")

    async def get_referrals_by_referrer_id(self, user_id: GetReferralsById) -> list:
        async with self.uow:
            user_id_dict = user_id.model_dump()
            referrers_from_db = await self.uow.users.select_many(user_id_dict)
            res = [UserResponse.model_validate(i) for i in referrers_from_db]
            return res
