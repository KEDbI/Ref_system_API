from pydantic import BaseModel, ConfigDict, EmailStr

class GetRefLinkByEmail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr

class GetRefLinkByEmailResponse(GetRefLinkByEmail):
    ref_link: str

class GetReferralsById(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UpdateRefLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ref_link_exp_days: int = 30