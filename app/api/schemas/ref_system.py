from pydantic import BaseModel, ConfigDict, EmailStr

class GetRefLinkByEmailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    ref_link: str

class GetReferralsById(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UpdateRefLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ref_link_exp: int = 30