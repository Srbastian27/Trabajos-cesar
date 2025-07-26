from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

def configurar_db():
    MONGO_URI = os.getenv('MONGO_URI')
    connect(host=MONGO_URI, alias='default')
    print("✅ Conexión exitosa a MongoDB Atlas")
