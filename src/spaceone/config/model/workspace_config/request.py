from typing import Union
from pydantic import BaseModel

__all__ = [
    "WorkspaceConfigCreateRequest",
    "WorkspaceConfigUpdateRequest",
    "WorkspaceConfigSetRequest",
    "WorkspaceConfigDeleteRequest",
    "WorkspaceConfigGetRequest",
    "WorkspaceConfigSearchQueryRequest",
    "WorkspaceConfigQueryRequest",
]


class WorkspaceConfigCreateRequest(BaseModel):
    name: str
    data: dict
    tags: Union[dict, None] = None
    workspace_id: str
    domain_id: str


class WorkspaceConfigUpdateRequest(BaseModel):
    name: str
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    workspace_id: str
    domain_id: str


class WorkspaceConfigSetRequest(BaseModel):
    name: str
    data: str
    tags: Union[dict, None] = None
    workspace_id: str
    domain_id: str


class WorkspaceConfigDeleteRequest(BaseModel):
    name: str
    workspace_id: str
    domain_id: str


class WorkspaceConfigGetRequest(BaseModel):
    name: str
    workspace_id: str
    domain_id: str


class WorkspaceConfigSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    workspace_id: str
    domain_id: str


class WorkspaceConfigQueryRequest(BaseModel):
    query: dict
    workspace_id: str
    domain_id: str
