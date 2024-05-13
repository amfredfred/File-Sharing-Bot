from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(BigInteger, autoincrement="auto")
    telegram_id = Column(BigInteger, unique=True, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    level = Column(Integer)
    bio = Column(Text)
    location = Column(Text)
    avatar = Column(Text)
    website = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    posts = relationship(back_populates="owner")
    callbacks: Mapped["CallbackData"] = relationship(back_populates="owner")
    posts: Mapped["Post"] = relationship(back_populates="owner")
    searchings: Mapped["Searching"] = relationship(back_populates="owner")
    conversations: Mapped["Conversation"] = relationship(back_populates="owner")

class CallbackData(Base):
    __tablename__ = "callback_data"

    id = Column(BigInteger, primary_key=True)
    data = Column(Text)
    data_hash = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner_id = Column(BigInteger, ForeignKey("profiles.telegram_id"))
    owner:Mapped['Profile'] = relationship(back_populates="callbacks")


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True)
    content = Column(Text)
    cover_image = Column(String, nullable=True)
    media_url = Column(String, nullable=True)
    container_style = Column(JSON, nullable=True)
    text_style = Column(JSON, nullable=True)
    post_type = Column(String, default="default")
    settings = Column(JSON, nullable=True)
    owner_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner_id = Column(Integer, ForeignKey("profiles.telegram_id"))
    owner: Mapped["Profile"] = relationship(back_populates="posts")


class Searching(Base):
    __tablename__ = "searchings"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner_id = Column(BigInteger, ForeignKey("profiles.telegram_id"))
    owner: Mapped["Profile"] = relationship(back_populates="searchings")
    searched_for = Column(String)


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, ForeignKey("profiles.telegram_id"))
    name = Column(String)
    balance = Column(Float, default=0)
    currency = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    transactions: Mapped["Transaction"] = relationship(back_populates="wallet")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True)
    wallet_id = Column(BigInteger, ForeignKey("wallets.id"))
    amount = Column(Float)
    type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    current_step = Column(String)
    next_step = Column(String)
    prev_step = Column(String)
    owner_id = Column(Integer, ForeignKey("profiles.telegram_id"))
    owner: Mapped["Profile"] = relationship(back_populates="conversations")

    def __repr__(self):
        return f"<Conversation(chat_id={self.chat_id}, current_step={self.current_step}, next_step={self.next_step}, prev_step={self.prev_step})>"
