from pydantic import BaseModel

class PartBase(BaseModel):
    name: str

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int

    class Config:
        orm_mode = True

class ChangeoverTimeBase(BaseModel):
    from_part_id: int
    to_part_id: int
    time: float

class ChangeoverTimeCreate(ChangeoverTimeBase):
    pass

class ChangeoverTime(ChangeoverTimeBase):
    id: int

    class Config:
        orm_mode = True