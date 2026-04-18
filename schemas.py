from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel): # Pydantic model
    title: str
    content: str

class PostCreate(PostBase):
    # Inherits title and content (required)
    # Adds published (optional, defaults to True)
    published: Optional[bool] = True

class PostUpdate(PostBase):
    pass