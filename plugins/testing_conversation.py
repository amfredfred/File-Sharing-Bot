from managers.conversation.manager import ConversationManager
from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message

# Define steps
START, NAME, AGE, END = range(4)

# Create a ConversationManager instance
conversation_manager = ConversationManager()

# Define command names
COMMAND_START = "cs"
COMMAND_END = "end"


# Handler for the /start command
@Bot.on_message(filters.command(COMMAND_START))
async def start_command(bot: Bot, message: Message):
    session = conversation_manager.get_session(message.chat.id)
    session.current_step = START
    session.next_step = NAME
    session.prev_step = None
    await message.reply_text("Hi! What is your name?")


# Handler for end command
@Bot.on_message(filters.command(COMMAND_END))
async def end_command(bot: Bot, message: Message):
    session = conversation_manager.get_session(message.chat.id)
    session.current_step = END
    session.next_step = None
    session.prev_step = None
    await message.reply_text("Conversation ended.")


# Handler for text messages
@Bot.on_message(filters.text)
async def handle_text(bot: Bot, message: Message):
    session = conversation_manager.get_session(message.chat.id)
    current_step = session.current_step
    next_step = session.next_step
    prev_step = session.prev_step

    if current_step == START:
        # Save name and move to next step
        session.current_step = NAME
        session.next_step = AGE
        session.prev_step = START
        session.name = message.text
        await message.reply_text("How old are you?")

    elif current_step == NAME:
        # Save age and move to next step
        session.current_step = AGE
        session.next_step = END
        session.prev_step = NAME
        session.age = message.text
        await message.reply_text("Thank you! Your data has been recorded.")
        conversation_manager.update_session(message.chat.id, END, None, None)

    print(f"{next_step} {prev_step}")
