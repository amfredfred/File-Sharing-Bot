from models.profile import Profile, ProfileManager
from models.conversation import ConversationManager, Conversation
from pyrogram.types import Message
from conversations.conversation_dict import conversation_channels


class UpdateAccountConversation:

    def __init__(
        self, profile: Profile, message: Message, conversation: Conversation = None
    ) -> None:
        self.profile = profile
        self.message = message
        self.reply_message = None
        self.manager = ConversationManager()
        self.conversation = conversation

    async def initialize(self):
        if self.conversation:
            await self.handle_response(self.message.text.strip())
        else:
            await self.start()

    async def start(self):
        self.reply_message = await self.message.reply_text("Wait...", quote=True)
        self.conversation = self.manager.insert_conversation(
            self.profile.id,
            conversation_channel=conversation_channels["uac"],
            current_step="start",
            next_step="username",
        )
        await self.prompt_username()

    async def prompt_username(self):
        if self.profile.username is None:
            self.conversation.current_step = "username"
            await self.reply_message.edit_text("Please send me your username")
            self.conversation.next_step = "first_name"
            self.conversation.prev_step = None
        else:
            await self.prompt_first_name()

    async def prompt_first_name(self):
        if self.profile.first_name is None:
            self.conversation.current_step = "first_name"
            await self.reply_message.edit_text("Please send me your first name")
            self.conversation.next_step = "last_name"
            self.conversation.prev_step = "username"
        else:
            await self.prompt_last_name()

    async def prompt_last_name(self):
        if self.profile.last_name is None:
            self.conversation.current_step = "last_name"
            await self.reply_message.edit_text("Please send me your last name")
            self.conversation.next_step = "bio"
            self.conversation.prev_step = "first_name"
        else:
            await self.prompt_bio()

    async def prompt_bio(self):
        if self.profile.bio is None:
            self.conversation.current_step = "bio"
            await self.reply_message.edit_text("Please send me your bio")
            self.conversation.next_step = "location"
            self.conversation.prev_step = "last_name"
        else:
            await self.prompt_location()

    async def prompt_location(self):
        if self.profile.location is None:
            self.conversation.current_step = "location"
            await self.reply_message.edit_text("Please send me your location")
            self.conversation.next_step = "avatar"
            self.conversation.prev_step = "bio"
        else:
            await self.prompt_avatar()

    async def prompt_avatar(self):
        if self.profile.avatar is None:
            self.conversation.current_step = "avatar"
            await self.reply_message.edit_text("Please send me your avatar URL")
            self.conversation.next_step = "website"
            self.conversation.prev_step = "location"
        else:
            await self.prompt_website()

    async def prompt_website(self):
        if self.profile.website is None:
            self.conversation.current_step = "website"
            await self.reply_message.edit_text("Please send me your website URL")
            self.conversation.next_step = "save"
            self.conversation.prev_step = "avatar"
        else:
            await self.update_profile()

    async def update_profile(self):
        profile_manager = ProfileManager()
        profile = profile_manager.get_profile_by_telegram_id(self.profile.telegram_id)
        conversation_data = self.conversation.json_data
        return profile_manager.update_profile(profile.telegram_id, **conversation_data)

    async def handle_response(self, message):
        self.reply_message = await self.message.reply_text("Please Wait...", quote=True)

        step_handlers = {
            "username": self.prompt_first_name,
            "first_name": self.prompt_last_name,
            "last_name": self.prompt_bio,
            "bio": self.prompt_location,
            "location": self.prompt_avatar,
            "avatar": self.prompt_website,
            "website": self.end,
            "end": self.end,
            "save": self.save,
        }

        if self.conversation.next_step in step_handlers:
            self.conversation.json_data[self.conversation.current_step] = message
            await step_handlers[self.conversation.next_step]()
        self.manager.update_session(self.profile.id, **self.conversation.to_dict())

    async def save(self):
        self.conversation.current_step = None
        self.manager.update_session(self.profile.id, ended=True)
        try:
            await self.update_profile()
            await self.reply_message.edit_text("Profile updated successfully!")
            print(f"Session: {self.manager.remove_session(self.conversation.id)}")
        except Exception as E:
            print(E)
            await self.reply_message.edit_text("Something went wrong...")

    async def end(self):
        self.conversation.current_step = None
        self.manager.update_session(self.profile.id, ended=True)
        try:
            await self.update_profile()
            await self.reply_message.edit_text("Profile updated successfully!")
        except Exception as E:
            print(E)
            await self.reply_message.edit_text("Something went wrong...")
