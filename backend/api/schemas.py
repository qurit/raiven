from pydantic import BaseModel


class ApplicationEntity(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class ApplicationEntityCreate(BaseModel):
    title: str
