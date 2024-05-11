from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from database import engine as DBEngine

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    telegram_id = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    level = Column(Integer)
    bio = Column(Text)
    location = Column(Text)
    avatar = Column(Text)
    website = Column(Text)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


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
            chat_id=chat_id,
            telegram_id=telegram_id,
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
            .filter(Profile.telegram_id is telegram_id)
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
