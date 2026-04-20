from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel): # Pydantic model
    title: str
    content: str

class PostCreate(PostBase):
    # Inherits title and content (required)
    # Adds published (optional, defaults to True)
    published: Optional[bool] = True

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    # This tells Pydantic to work with ORM objects, allowing us to return SQLAlchemy models directly from our path operations without needing to convert them to dictionaries first.
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# This model is used for the response when a user is created. It includes the id, email, and created_at fields, but excludes the password for security reasons.    
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str