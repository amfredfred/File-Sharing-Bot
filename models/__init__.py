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
    Boolean,
)
from sqlalchemy.orm import relationship, class_mapper
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(String, unique=True)
    chat_id = Column(String, unique=True)
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

    callbacks = relationship(
        "CallbackData", back_populates="owner", cascade="all, delete"
    )
    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    searchings = relationship(
        "Searching", back_populates="owner", cascade="all, delete"
    )
    conversations = relationship(
        "Conversation", back_populates="owner", cascade="all, delete"
    )
    wallet = relationship("Wallet", back_populates="owner", cascade="all, delete")

    def to_dict(self):
        return {
            c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns
        }

    def __repr__(self):
        return f"<Profile(id={self.id}, username={self.username})>"


class CallbackData(Base):
    __tablename__ = "callback_data"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    data = Column(Text)
    data_hash = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner_id = Column(BigInteger, ForeignKey("sendbox_scheme.profiles.id"))
    owner = relationship("Profile", back_populates="callbacks")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    content = Column(Text)
    cover_image = Column(String, nullable=True)
    media_url = Column(String, nullable=True)
    container_style = Column(JSON, nullable=True)
    text_style = Column(JSON, nullable=True)
    post_type = Column(String, default="default")
    settings = Column(JSON, nullable=True)
    owner_id = Column(BigInteger, ForeignKey("sendbox_scheme.profiles.id"))
    owner = relationship("Profile", back_populates="posts")


class Searching(Base):
    __tablename__ = "searchings"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner_id = Column(BigInteger, ForeignKey("sendbox_scheme.profiles.id"))
    owner = relationship("Profile", back_populates="searchings")
    searched_for = Column(String)


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    balance = Column(Float, default=0)
    currency = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    transactions = relationship(
        "Transaction", back_populates="wallet", cascade="all, delete"
    )
    owner_id = Column(BigInteger, ForeignKey("sendbox_scheme.profiles.id"))
    owner = relationship("Profile", back_populates="wallet")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(BigInteger, primary_key=True)
    wallet_id = Column(BigInteger, ForeignKey("sendbox_scheme.wallets.id"))
    amount = Column(Float)
    type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    wallet = relationship("Wallet", back_populates="transactions")


class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = {"schema": "sendbox_scheme"}

    id = Column(Integer, primary_key=True)
    current_step = Column(String)
    next_step = Column(String)
    prev_step = Column(String)
    ended = Column(Boolean, default=False)
    json_data = Column(JSON, default={})
    conversation_channel = Column(String)
    message_id = Column(BigInteger)
    owner_id = Column(BigInteger, ForeignKey("sendbox_scheme.profiles.id"))

    owner = relationship(
        "Profile", back_populates="conversations", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "current_step": self.current_step,
            "next_step": self.next_step,
            "prev_step": self.prev_step,
            "ended": self.ended,
            "conversation_channel": self.conversation_channel,
            "owner_id": self.owner_id,
            "json_data": self.json_data,
        }

    def __repr__(self):
        return (
            f"<Conversation(id={self.id}, owner_id={self.owner_id}, "
            f"current_step={self.current_step}, next_step={self.next_step}, "
            f"prev_step={self.prev_step}, ended={self.ended}, "
            f"conversation_channel={self.conversation_channel})>"
            f"json_data={self.json_data}"
        )
