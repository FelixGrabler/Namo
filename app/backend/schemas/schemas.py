from pydantic import BaseModel
from typing import Optional, Dict, Any


# User schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Name schemas
class NameBase(BaseModel):
    source: str
    name: str
    gender: Optional[str] = None
    rank: Optional[int] = None
    count: Optional[int] = None


class NameCreate(NameBase):
    pass


class NameResponse(NameBase):
    id: int

    class Config:
        from_attributes = True


class NameInfoResponse(BaseModel):
    name: str
    info: Dict[str, Any]

    class Config:
        from_attributes = True


# Vote schemas
class VoteBase(BaseModel):
    name_id: int
    vote: bool  # True = like, False = dislike


class VoteCreate(VoteBase):
    pass


class VoteResponse(VoteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class VoteWithName(BaseModel):
    id: int
    user_id: int
    name_id: int
    vote: bool
    name: NameResponse

    class Config:
        from_attributes = True
