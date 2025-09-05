
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    _id: int
    bal: Optional[int] = 0
    bank: Optional[int] = 0

