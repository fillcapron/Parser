from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    label: str
    link: str


class TagBase(BaseModel):
    name: str
    company_id: int


class CreateTag(TagBase):
    pass


class CompanyBase(BaseModel):
    name: str
    description: str
    status: str


class CreateCompany(CompanyBase):
    pass


class Post(PostBase):
    pass


class Tag(TagBase):
    id: int
    posts: List[Post] = []

    model_config = ConfigDict(from_attributes=True)


class Company(CompanyBase):
    id: int
    status: str
    tags: List[Tag] = []
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



