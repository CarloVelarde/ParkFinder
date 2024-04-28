import os 
from dotenv import load_dotenv
from beanie import init_beanie 
from motor.motor_asyncio import AsyncIOMotorClient
# from models.admins import Admin
from models.reviews import Reviews
from models.parks import Parks
from models.parkimage import ParkImages
from models.users import User


async def init_db():

   # Load environment variables
   load_dotenv()

   conn_str = os.getenv("DB_CONN")
   client = AsyncIOMotorClient(conn_str)

   await init_beanie(database = client.park_app, document_models=[Reviews, Parks, ParkImages, User])