from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Union
from datetime import datetime


class LabCreate(BaseModel):
    lab_name: str = Field(..., min_length=1, max_length=255)
    lab_url: Union[HttpUrl, str]


class ThesisTopicCreate(BaseModel):
    mt_title: str = Field(..., min_length=1, max_length=255)
    mt_url: Union[HttpUrl, str]
    added_date: datetime
    lab_id: int


class LabResponse(BaseModel):
    lab_id: int
    lab_name: str
    lab_url: Union[HttpUrl, str]

    class Config:
        orm_mode = True


class ThesisTopicResponse(BaseModel):
    topic_id: int
    mt_title: str
    mt_url: Union[HttpUrl, str]
    added_date: datetime
    lab_id: int

    class Config:
        orm_mode = True
