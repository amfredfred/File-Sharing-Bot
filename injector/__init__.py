from helper_func import present_user
from pyrogram.types import Message, CallbackQuery


def injector(func):
    async def wrapper(client, *args, **kwargs):
        telegram_id = None
        if args:
            arg = args[0]
            if isinstance(arg, Message):
                telegram_id = arg.from_user.id
            elif isinstance(arg, CallbackQuery):
                telegram_id = arg.message.from_user.id
            else:
                raise ValueError("No message or callback query found in args or kwargs")
        else:
            raise ValueError("No arguments provided")

        profile = await present_user(telegram_id)
        return await func(client, profile, *args, **kwargs)

    return wrapper
