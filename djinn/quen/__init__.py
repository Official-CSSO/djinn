# MongoDB wrapper 

from djinn.constants import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.collection import Collection

class Quen:
    motor: AsyncIOMotorClient
    db: Database
    user: Collection

    def __init__(self):
        self.motor = AsyncIOMotorClient(MONGO_DB)
        self.db = self.motor["djinn"]
        self.user = self.db["user"]
    

