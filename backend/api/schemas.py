from pydantic import BaseModel


class ApplicationEntity(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class ApplicationEntityCreate(BaseModel):
    title: str

# TODO: fix the other schemas and models and stuff
class DicomPatient(BaseModel):
    id: str

    class Config:
        orm_mode = True

class DicomStoreEvent(BaseModel):
    id: int
    path: str

    class Config:
        orm_mode = True
