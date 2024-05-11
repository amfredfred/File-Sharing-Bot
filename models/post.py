from sqlalchemy import Column, Integer, Text, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    cover_image = Column(String, nullable=True)
    media_url = Column(String, nullable=True)
    container_style = Column(JSON, nullable=True)
    text_style = Column(JSON, nullable=True)
    post_type = Column(String, default="default")
    settings = Column(JSON, nullable=True)
    owner_id = Column(Integer)
    timestamps = Column("timestamps", DateTime)

    # Define the foreign key relationship
    owner = relationship("Profile", back_populates="posts")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    # Define other columns in your Profile table as needed
    # Example: name = Column(String)

    # Define the relationship with posts
    posts = relationship("Post", back_populates="owner")
