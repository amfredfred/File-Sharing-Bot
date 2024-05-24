from pyrogram import Client
from models.profile import Profile
from models.conversation import Conversation
from conversations.conversation_dict import conversation_channels
from conversations.profile_update_conversations import UpdateAccountConversation

async def conversate(client: Client, profile: Profile, conversation: Conversation, message):
    if conversation.conversation_channel == conversation_channels["uac"]:
        conv = UpdateAccountConversation(profile, message, conversation)
        return await conv.initialize()
