from typing import Union
from pydantic import BaseModel

__all__ = [
    "DomainConfigCreateRequest",
    "DomainConfigUpdateRequest",
    "DomainConfigSetRequest",
    "DomainConfigDeleteRequest",
    "DomainConfigGetRequest",
    "DomainConfigSearchQueryRequest",
]


class DomainConfigCreateRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    domain_id: str


class DomainConfigUpdateRequest(BaseModel):
    name: str
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    domain_id: str


class DomainConfigSetRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    domain_id: str


class DomainConfigDeleteRequest(BaseModel):
    name: str
    domain_id: str


class DomainConfigGetRequest(BaseModel):
    name: str
    domain_id: str


class DomainConfigSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    domain_id: str
