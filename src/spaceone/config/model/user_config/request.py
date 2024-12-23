from typing import Union
from pydantic import BaseModel

__all__ = [
    "UserConfigCreateRequest",
    "UserConfigUpdateRequest",
    "UserConfigSetRequest",
    "UserConfigDeleteRequest",
    "UserConfigGetRequest",
    "UserConfigSearchQueryRequest",
]


class UserConfigCreateRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    domain_id: str
    user_id: str


class UserConfigUpdateRequest(BaseModel):
    name: str
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    domain_id: str
    user_id: str


class UserConfigSetRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    domain_id: str
    user_id: str


class UserConfigDeleteRequest(BaseModel):
    name: str
    domain_id: str
    user_id: str


class UserConfigGetRequest(BaseModel):
    name: str
    domain_id: str
    user_id: str


class UserConfigSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    domain_id: str
    user_id: str
