# (©)CodeXBotz and @EditorFred on Telegram

from models.profile import ProfileManager
from models.wallet import WalletManager

_profile = ProfileManager()
_wallet = WalletManager()


async def present_user(telegram_id: int):
    if not telegram_id:
        return None
    found = _profile.get_profile_by_telegram_id(telegram_id=telegram_id)
    return found


async def add_user(tid: int, chat_id: int, username, first_name, last_name): 
    user_account = _profile.insert_profile(
        tid, chat_id, username, first_name, last_name
    )
    user_wallet = _wallet.create_wallet(user_account.id, f"{tid}_wallet")
    return user_account, user_wallet


async def full_userbase():
    user_docs = _profile.get_all_users()
    return user_docs


async def del_user(telegram_id: int):
    _profile = ProfileManager()
    return _profile.delete_profile(telegram_id)

async def update_profile(telegram_id:int):
    return _profile.update_profile(telegram_id)
