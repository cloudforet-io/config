from typing import Union, Literal
from pydantic import BaseModel

__all__ = [
    "SharedConfigCreateRequest",
    "SharedConfigUpdateRequest",
    "SharedConfigDeleteRequest",
    "SharedConfigGetRequest",
    "SharedConfigSearchQueryRequest",
    "ResourceGroup",
]

ResourceGroup = Literal["DOMAIN", "WORKSPACE", "PROJECT"]


class SharedConfigCreateRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    resource_group: ResourceGroup
    domain_id: str
    workspace_id: Union[list, str, None] = None
    project_id: Union[list, str, None] = None


class SharedConfigUpdateRequest(BaseModel):
    name: str
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    domain_id: str
    workspace_id: Union[str, None] = None
    user_projects: Union[list, None] = None


class SharedConfigDeleteRequest(BaseModel):
    name: str
    domain_id: str
    workspace_id: Union[str, None] = None
    user_projects: Union[list, None] = None


class SharedConfigGetRequest(BaseModel):
    name: str
    domain_id: str
    workspace_id: Union[list, str, None] = None
    user_projects: Union[list, None] = None


class SharedConfigSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    domain_id: str
    workspace_id: Union[list, str, None] = None
    user_project: Union[list, None] = None
    project_id: Union[str, None] = None
