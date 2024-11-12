from sqlalchemy import update, delete

from app.db.models import Users
from app.repositories.base_repository import Repository

class UsersRepository(Repository):
    model = Users

    async def update_one(self, filters: dict, data: dict):
        query = update(self.model).where(self.model.login == filters['login']).values(**data).returning(self.model)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def delete_one(self, filters: dict):
        query = delete(self.model).where(self.model.id == filters['id']).returning()
        res = await self.session.execute(query)
        return res.scalar_one()