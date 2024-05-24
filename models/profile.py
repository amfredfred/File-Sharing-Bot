from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from database import engine as DBEngine
from models import Profile, Base

class ProfileManager:
    def __init__(self):
        engine = DBEngine
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_profile(
        self,
        chat_id,
        telegram_id,
        username=None,
        first_name=None,
        last_name=None,
        level=None,
        bio=None,
        location=None,
        avatar=None,
        website=None,
    ):
        profile = Profile(
            chat_id=str(chat_id),
            telegram_id=str(telegram_id),
            username=username,
            first_name=first_name,
            last_name=last_name,
            level=level,
            bio=bio,
            location=location,
            avatar=avatar,
            website=website,
        )
        self.session.add(profile)
        self.session.commit()
        return profile

    def get_profile_by_telegram_id(self, telegram_id):
        return (
            self.session.query(Profile)
            .filter(Profile.telegram_id == str(telegram_id))
            .first()
        )

    def get_all_users(self):
        return self.session.query(Profile).all()

    def delete_profile(self, telegram_id):
        profile = self.get_profile_by_telegram_id(telegram_id)
        if profile:
            self.session.delete(profile)
            self.session.commit()
            return 1
        return 0

    def get_active_users_last_24_hours(self):
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        return (
            self.session.query(Profile)
            .filter(Profile.updated_at >= twenty_four_hours_ago)
            .all()
        )


    def update_profile(self, telegram_id, **kwargs):
        profile = self.get_profile_by_telegram_id(telegram_id)
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            self.session.commit()
            return profile
        else:
            return False
