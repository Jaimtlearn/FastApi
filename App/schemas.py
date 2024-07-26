from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    title: str
    content: str = "None"
    published: bool = False

class CreatePost(Post):
    pass

class PostResponse(Post):
    id: int
    created_at : datetime
    owner_id: int
    owner: UserResponse
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class VoteSchema(BaseModel):
    post_id: int
    direction: int

