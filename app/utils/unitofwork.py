from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.db.models import Users
from app.repositories.users_repository import UsersRepository

class IUnitOfWork(ABC):
    users: UsersRepository

    @abstractmethod
    def __init__(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass

class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()