# (©)CodeXBotz and @EditorFred on Telegram

from models.profile import Profile
from models.wallet import Wallet

async def present_user(telegram_id: int):
    _profile = Profile()
    found = _profile.get_profile_by_telegram_id(telegram_id=telegram_id)
    return bool(found)


async def add_user(tid: int, chat_id: int, username, first_name, last_name):
    _profile = Profile()
    _wallet = Wallet()
    user_account = _profile.insert_profile(tid, chat_id, username, first_name, last_name)
    user_wallet = _wallet.create_wallet(tid, f"{tid}_wallet")
    return user_account, user_wallet


async def full_userbase():
    user_docs = Profile().get_all_users()
    return user_docs

async def del_user(telegram_id: int):
    _profile = Profile()
    return _profile.delete_profile(telegram_id)
