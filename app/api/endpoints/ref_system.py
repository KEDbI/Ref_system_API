from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from app.api.schemas.users import UserResponse, RegisterUser
from app.api.schemas.ref_system import GetRefLinkByEmailResponse, GetRefLinkByEmail, GetReferralsById, UpdateRefLink
from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.services.ref_system_service import RefSystemService
from app.core.security import get_user_from_token

ref_system_router = APIRouter()

async def get_ref_system_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> RefSystemService:
    return RefSystemService(uow)


@ref_system_router.post('/register', response_model=UserResponse)
async def registration(user: RegisterUser,
                       ref_system_service: RefSystemService = Depends(get_ref_system_service)) -> UserResponse:
    # Создание нового пользователя с необходимыми данными
    return await ref_system_service.register_user(user)


@ref_system_router.post('/login')
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                 ref_system_service: RefSystemService = Depends(get_ref_system_service)) -> dict:
    # Аутентификация пользователя и выдача JWT-токена
    jwt = await ref_system_service.get_jwt(user_data)
    return {"access_token": jwt, "token_type": "bearer"}


@ref_system_router.post('/update_ref_link', response_model=UserResponse)
async def update_ref_link(ref_link_exp: UpdateRefLink,
                          ref_system_service: RefSystemService = Depends(get_ref_system_service),
                          current_user: str = Depends(get_user_from_token)):
    return await ref_system_service.update_ref_link(user=current_user, ref_link_exp_days=ref_link_exp)


@ref_system_router.delete('/delete_ref_link', response_model=UserResponse)
async def delete_ref_link(ref_system_service: RefSystemService = Depends(get_ref_system_service),
                          current_user: str = Depends(get_user_from_token)):
    return await ref_system_service.delete_ref_link(current_user)


@ref_system_router.get('/get_ref_link_by_email/{email}', response_model=GetRefLinkByEmailResponse)
async def get_ref_link_by_email(email: str,
                          ref_system_service: RefSystemService = Depends(get_ref_system_service),
                          current_user: str = Depends(get_user_from_token)):
    return await ref_system_service.get_ref_link_by_email(email=email)


@ref_system_router.get('/get_referrals_by_referrer_id/{referrer_id}')
async def get_referrals_by_referrer_id(referrer_id: str,
                          ref_system_service: RefSystemService = Depends(get_ref_system_service),
                          current_user: str = Depends(get_user_from_token)):
    return {'message': await ref_system_service.get_referrals_by_referrer_id(referrer_id=int(referrer_id))}

