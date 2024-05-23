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
        self.profile_data = {}

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
        self.conversation.current_step = "username"
        await self.reply_message.edit_text("Please send me your username")
        self.update_conversation_steps(
            current_step="username", next_step="first_name", prev_step=None
        )

    async def prompt_first_name(self):
        self.conversation.current_step = "first_name"
        await self.reply_message.edit_text("Please send me your first name")
        self.update_conversation_steps(
            current_step="first_name", next_step="last_name", prev_step="username"
        )

    async def prompt_last_name(self):
        self.conversation.current_step = "last_name"
        await self.reply_message.edit_text("Please send me your last name")
        self.update_conversation_steps(
            current_step="last_name", next_step="bio", prev_step="first_name"
        )

    async def prompt_bio(self):
        self.conversation.current_step = "bio"
        await self.reply_message.edit_text("Please send me your bio")
        self.update_conversation_steps(
            current_step="bio", next_step="location", prev_step="last_name"
        )

    async def prompt_location(self):
        self.conversation.current_step = "location"
        await self.reply_message.edit_text("Please send me your location")
        self.update_conversation_steps(
            current_step="location", next_step="avatar", prev_step="bio"
        )

    async def prompt_avatar(self):
        self.conversation.current_step = "avatar"
        await self.reply_message.edit_text("Please send me your avatar URL")
        self.update_conversation_steps(
            current_step="avatar", next_step="website", prev_step="location"
        )

    async def prompt_website(self):
        self.conversation.current_step = "website"
        await self.reply_message.edit_text("Please send me your website URL")
        self.update_conversation_steps(
            current_step="website", next_step="end", prev_step="avatar"
        )
        await self.handle_response(self.message.text.strip())

    async def update_profile(self):
        profile_manager = ProfileManager()
        profile = profile_manager.get_profile_by_telegram_id(self.profile.telegram_id)
        profile.username = self.profile_data.get("username")
        profile.first_name = self.profile_data.get("first_name")
        profile.last_name = self.profile_data.get("last_name")
        profile.bio = self.profile_data.get("bio")
        profile.location = self.profile_data.get("location")
        profile.avatar = self.profile_data.get("avatar")
        profile.website = self.profile_data.get("website")
        updated_profile = profile_manager.update_profile(profile)

        print(f"Updated: {updated_profile}")
        await self.end()

    def update_conversation_steps(self, current_step, next_step, prev_step):
        self.manager.update_session(
            self.profile.id,
            current_step=current_step,
            next_step=next_step,
            prev_step=prev_step,
        )
        self.conversation.current_step = current_step
        self.conversation.next_step = next_step
        self.conversation.prev_step = prev_step

    async def handle_response(self, message):
        self.reply_message = await self.message.reply_text("Please Wait...", quote=True)

        step_handlers = {
            "username": self.prompt_first_name,
            "first_name": self.prompt_last_name,
            "last_name": self.prompt_bio,
            "bio": self.prompt_location,
            "location": self.prompt_avatar,
            "avatar": self.prompt_website,
            "website": self.update_profile,
        }

        if self.conversation.next_step in step_handlers:
            self.profile_data[self.conversation.current_step] = message
            await step_handlers[self.conversation.next_step]()

    async def end(self):
        self.conversation.current_step = None
        self.manager.update_session(self.profile.id, ended=True)
        await self.reply_message.edit_text("Profile updated successfully!")


# Example usage:
# profile = Profile(...)  # Load or create the Profile instance
# message = Message(...)  # The message object from pyrogram
# conversation = Conversation(...)  # Load or create the Conversation instance
# update_conv = UpdateAccountConversation(profile, message, conversation)
# await update_conv.initialize()
