from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    email: EmailStr
    ref_link: str | None = None
    ref_link_exp: datetime | None = None
    referrer_id: int | None


class RegisterUser(BaseModel):
    login: str
    password: str
    email: EmailStr
    # Здесь пользователь может ввести реферальную ссылку от реферера
    ref_link: str | None = None