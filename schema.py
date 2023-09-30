import pydantic


class CreateAd(pydantic.BaseModel):
    header: str
    description: str
    owner: str
    