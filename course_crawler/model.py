from pydantic import BaseModel


class Course(BaseModel):
    id: str
    name: str
    credit: str
    field: str
    area: str
    time: str
    room: str
    teacher: str
    english: bool
    type: int
