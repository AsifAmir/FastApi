from dotenv import load_dotenv
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.config import settings
load_dotenv()

class Post(Base):
    __tablename__ = settings.TABLE_NAME
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Establishing a relationship between the Post and User models. This allows us to access the user who created a post using post.owner and to access all posts created by a user using user.posts.
    owner = relationship("User")

class User(Base):
    __tablename__ = settings.USER_TABLE_NAME
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = settings.VOTE_TABLE_NAME
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(f"{settings.TABLE_NAME}.id", ondelete="CASCADE"), primary_key=True)