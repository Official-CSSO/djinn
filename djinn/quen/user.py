
from pydantic import BaseModel

class User(BaseModel):
    _id: int
    bal: int = 0
    bank: int = 0

