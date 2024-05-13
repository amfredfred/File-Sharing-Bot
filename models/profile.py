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
            chat_id=int(chat_id),
            telegram_id=int(telegram_id),
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
        return True

    def get_profile_by_telegram_id(self, telegram_id):
        return (
            self.session.query(Profile)
            .filter(Profile.telegram_id == int(telegram_id))
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
        
    def update_profile(
        self,
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
        profile = self.get_profile_by_telegram_id(telegram_id)
        if profile:
            if username is not None:
                profile.username = username
            if first_name is not None:
                profile.first_name = first_name
            if last_name is not None:
                profile.last_name = last_name
            if level is not None:
                profile.level = level
            if bio is not None:
                profile.bio = bio
            if location is not None:
                profile.location = location
            if avatar is not None:
                profile.avatar = avatar
            if website is not None:
                profile.website = website

            self.session.commit()
            return True
        else:
            return False