from pydantic import BaseModel


class User_validation(BaseModel):
    login: str
    password: str
    email: str
    partner: str
    scratch_time_user: int
    scratch_time_partner: int


class Comment_validation(BaseModel):
    user_login: str
    comment: str
    date_of_creation: str
    likes: int
    dislikes: int
    test: bool
