from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base



class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    ref_link: Mapped[str | None] = mapped_column(unique=True)
    referer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    ref_link_exp: Mapped[datetime | None]

