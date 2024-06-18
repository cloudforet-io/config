from typing import Union, Literal
from pydantic import BaseModel

__all__ = [
    "PublicConfigCreateRequest",
    "PublicConfigUpdateRequest",
    "PublicConfigSetRequest",
    "PublicConfigDeleteRequest",
    "PublicConfigGetRequest",
    "PublicConfigSearchQueryRequest",
    "PublicConfigQueryRequest",
]

ResourceGroup = Literal["DOMAIN", "WORKSPACE", "PROJECT"]


class PublicConfigCreateRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    resource_group: ResourceGroup
    user_projects: Union[list, None] = None
    project_id: Union[list, str, None] = None
    workspace_id: Union[list, str, None] = None
    domain_id: str


class PublicConfigUpdateRequest(BaseModel):
    name: str
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    user_projects: Union[list, None] = None
    project_id: Union[str, None] = None
    workspace_id: Union[str, None] = None
    domain_id: str


class PublicConfigSetRequest(BaseModel):
    name: str
    data: str
    tags: Union[dict, None] = None
    user_projects: Union[list, None] = None
    project_id: Union[str, None] = None
    workspace_id: Union[str, None] = None
    domain_id: str


class PublicConfigDeleteRequest(BaseModel):
    name: str
    user_projects: Union[list, None] = None
    project_id: Union[str, None] = None
    workspace_id: Union[str, None] = None
    domain_id: str


class PublicConfigGetRequest(BaseModel):
    name: str
    user_projects: Union[list, None] = None
    project_id: Union[list, str, None] = None
    workspace_id: Union[list, str, None] = None
    domain_id: str


class PublicConfigSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    user_project: Union[list, None] = None
    project_id: Union[list, str, None] = None
    workspace_id: Union[list, str, None] = None
    domain_id: str


class PublicConfigQueryRequest(BaseModel):
    query: dict
    workspace_id: str
    domain_id: str
