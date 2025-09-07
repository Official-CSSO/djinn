# MongoDB wrapper 

from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from .user import User

class Quen:
    motor: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    user: AsyncIOMotorCollection

    def __init__(self, motor: AsyncIOMotorClient):
        self.motor = motor
        self.db = self.motor["djinn"]
        self.user = self.db["user"]
    
    
    async def get_user(self, id: int) -> Optional[User]:
        u = await self.user.find_one({"_id": id})
        if not u:
            # create if none
            x = User(_id=id, bal=0, bank=0)
            await self.user.insert_one(x.model_dump())
            return x
        
        return User(**u)

    async def update_user_bal(self, id: int, amount: int) -> User:
        u = await self.user.find_one_and_update(
            {"_id": id},
            {
                "$inc": {"bal": amount}
            },
            upsert=True,
            return_document=True
        )
        return User(**u)

