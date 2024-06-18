from datetime import datetime
from typing import Union, List
from pydantic import BaseModel

from spaceone.core import utils

from spaceone.config.model.public_config.request import ResourceGroup

__all__ = ["PublicConfigResponse", "PublicConfigsResponse"]


class PublicConfigResponse(BaseModel):
    name: Union[str, None] = None
    data: Union[dict, None] = None
    tags: Union[dict, None] = None
    resource_group: Union[ResourceGroup, None] = None
    project_id: Union[str, None] = None
    workspace_id: Union[str, None] = None
    domain_id: Union[str, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["created_at"] = utils.datetime_to_iso8601(data["created_at"])
        data["updated_at"] = utils.datetime_to_iso8601(data.get("updated_at"))
        return data


class PublicConfigsResponse(BaseModel):
    results: List[PublicConfigResponse] = []
    total_count: int
