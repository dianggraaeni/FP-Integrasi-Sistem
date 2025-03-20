import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gunakan variabel lingkungan untuk URI MongoDB agar lebih aman
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://studianggra:27lDrfEa6zTi4Tmu@clustern.du2zm.mongodb.net/?appName=ClusterN")
DB_NAME = os.getenv("DB_NAME", "ClusterN")  # Ganti dengan nama database

# Buat koneksi MongoDB menggunakan AsyncIOMotorClient
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Koleksi users
users_collection = db["users"]
