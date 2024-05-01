# (©)CodeXBotz

from models.profile import profile

async def present_user(telegram_id: int):
    print(f"{telegram_id} TG ID")
    _profile = profile()
    found = _profile.get_profile_by_telegram_id(telegram_id=telegram_id)
    return bool(found)


async def add_user(tid: int, chat_id: int, username, first_name, last_name):
    _profile = profile()
    user_account = _profile.insert_profile(tid, chat_id, username, first_name, last_name)
    return user_account


async def full_userbase():
    user_docs = profile().get_all_users()
    return user_docs

async def del_user(telegram_id: int):
    _profile = profile()
    return _profile.delete_profile(telegram_id)
