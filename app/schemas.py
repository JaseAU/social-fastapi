from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Requests


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True

# Post
#   Title, Content, Published,
#   Id, Created_At, Owner_ID
#   Owner details
# VoteCnt


class PostVote(BaseModel):
    post: Post
    vote_cnt: int

    class Config:
        # orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    # updown: conint(le=1)
    updown: int = Field(..., ge=0, le=1)
