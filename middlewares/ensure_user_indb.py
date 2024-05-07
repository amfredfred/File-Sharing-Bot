from pyrogram import Client
from pyrogram.types import Message


# Define your middleware function
def ensure_user_indb(client: Client, message: Message):
    # Preprocessing logic goes here
    print("Middleware executed!")
