from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def insert_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def select_one(self, filters: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, filters: dict, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, data: dict):
        raise NotImplementedError

class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def select_one(self, filters: dict):
        query = select(self.model).filter_by(**filters)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def select_many(self, filters: dict):
        query = select(self.model).filter_by(**filters)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def update_one(self, filters: dict, data: dict):
        pass

    async def delete_one(self, filters: dict):
        pass