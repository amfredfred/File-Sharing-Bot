from sqlalchemy.orm import sessionmaker
from database.connection import engine as db_engine
from models import Conversation, Base


class ConversationManager:
    def __init__(self):
        self.engine = db_engine
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_session(self, owner_id):
        conv_session = self.session.query(Conversation).filter_by(owner_id=owner_id, ended=False).first()
        return conv_session


    def remove_session(self, session_id):
        try:
            # Use `Conversation.id == session_id` instead of `id == session_id`
            self.session.query(Conversation).filter(Conversation.id == session_id).delete()
            # Commit the changes to the database
            self.session.commit()
            return True
        except Exception as e:
            # Print or log the exception for debugging
            print(f"An error occurred: {e}")
            # Rollback the session in case of an error
            self.session.rollback()
            return False

    def update_session(self, owner_iid, **kwargs):
        conv_session = self.get_session(owner_iid)
        for key, value in kwargs.items():
            if hasattr(conv_session, key):
                setattr(conv_session, key, value)
            else:
                print(f"Attribute '{key}' does not exist in Conversation Model.")
        self.session.commit()
        return conv_session

    def insert_conversation(
        self,
        owner_id,
        conversation_channel,
        current_step,
        next_step=None,
        prev_step=None,
        ended=False
    ):
        conversation = Conversation(
            owner_id=owner_id,
            current_step=current_step,
            next_step=next_step,
            prev_step=prev_step,
            ended=ended,
            conversation_channel=conversation_channel,
        )
        self.session.add(conversation)
        self.session.commit()
        return conversation
