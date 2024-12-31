import logging
from typing import Union

from spaceone.core.error import ERROR_REQUIRED_PARAMETER
from spaceone.core.service import *

from spaceone.config.manager.identity_manager import IdentityManager
from spaceone.config.manager.shared_config_manager import SharedConfigManager
from spaceone.config.model.shared_config.response import *
from spaceone.config.model.shared_config.request import *

_LOGGER = logging.getLogger(__name__)



@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class SharedConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared_config_mgr = SharedConfigManager()
        self.identity_mgr = IdentityManager()

    @transaction(permission="config:SharedConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def create(self, params: SharedConfigCreateRequest) -> Union[SharedConfigResponse, dict]:
        """Create shared config

        Args:
            params (SharedConfigCreateRequest): {
                'name': 'str',              # required
                'data': 'dict',             # required
                'tags': 'dict',
                'resource_group' : 'str',   # required
                'domain_id': 'str',         # injected from auth (required)
                'workspace_id': 'str'       # injected from auth
                'users_project_id': 'str',  # injected from auth
                'project_id': 'str'
            }

        Returns:
            SharedConfigResponse:
        """

        if params.resource_group == "PROJECT":
            if params.project_id is None:
                raise ERROR_REQUIRED_PARAMETER(key='project_id')

            project_info = self.identity_mgr.get_project(params.project_id, params.domain_id)
            params.workspace_id = project_info["workspace_id"]
        elif params.resource_group == "WORKSPACE":
            if params.workspace_id is None:
                raise ERROR_REQUIRED_PARAMETER(key='workspace_id')

            self.identity_mgr.check_workspace(params.workspace_id, params.domain_id)
            params.project_id = "*"
        else:
            params.workspace_id = "*"
            params.project_id = "*"

        shared_config_vo = self.shared_config_mgr.create_shared_config(params.dict())

        return SharedConfigResponse(**shared_config_vo.to_dict())

    @transaction(permission="config:SharedConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def update(self, params: SharedConfigUpdateRequest) -> Union[SharedConfigResponse, dict]:
        """Update shared config

        Args:
            params (dict): {
                'name': 'str',              # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str',         # injected from auth (required)
                'workspace_id': 'str'       # injected from auth
                "user_projects": 'list',    # injected from auth
            }

        Returns:
            domain_config_vo (object)
        """

        domain_id = params.domain_id
        workspace_id = params.workspace_id
        user_projects = params.user_projects

        shared_config_vo = self.shared_config_mgr.get_shared_config(
            params.name, domain_id, workspace_id, user_projects
        )

        shared_config_vo = self.shared_config_mgr.update_shared_config_by_vo(
            params.dict(exclude_unset=True), shared_config_vo
        )

        return SharedConfigResponse(**shared_config_vo.to_dict())

    @transaction(permission="config:SharedConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def delete(self, params: SharedConfigDeleteRequest) -> None:
        """Delete shared config

        Args:
            params (dict): {
                'name': 'str',              # required
                'domain_id': 'str',         # injected from auth (required)
                'workspace_id': 'str',      # injected from auth
                'user_projects': 'list',    # injected from auth
            }

        Returns:
            None
        """

        domain_id = params.domain_id
        workspace_id = params.workspace_id
        user_projects = params.user_projects

        shared_config_vo = self.shared_config_mgr.get_shared_config(
            params.name, domain_id, workspace_id, user_projects
        )
        self.shared_config_mgr.delete_shared_config_by_vo(shared_config_vo)

    @transaction(permission="config:SharedConfig.read",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @change_value_by_rule("APPEND", "workspace_id", "*")
    @change_value_by_rule("APPEND", "user_projects", "*")
    @convert_model
    def get(self, params: SharedConfigGetRequest) -> Union[SharedConfigResponse, dict]:
        """Get shared config

        Args:
            params (dict): {
                'name': 'str',              # required
                'domain_id': 'str',         # injected from auth (required)
                'workspace_id': 'str',      # injected from auth
                'user_projects': 'list',    # injected from auth
            }

        Returns:
            SharedConfigResponse:
        """

        domain_id = params.domain_id
        workspace_id = params.workspace_id
        user_projects = params.user_projects

        shared_config_vo = self.shared_config_mgr.get_shared_config(
            params.name, domain_id, workspace_id, user_projects
        )

        return SharedConfigResponse(**shared_config_vo.to_dict())

    @transaction(permission="config:SharedConfig.read",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @change_value_by_rule("APPEND", "workspace_id", "*")
    @change_value_by_rule("APPEND", "user_projects", "*")
    @append_query_filter(["name", "domain_id", "workspace_id", "users_project", "project_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def list(self, params: SharedConfigSearchQueryRequest) -> Union[SharedConfigsResponse, dict]:
        """List shared configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v2.Query)'
                'name': 'str',
                'domain_id': 'str',                             # injected from auth (required)
                'workspace_id': 'str',                          # injected from auth
                'user_projects': 'list',                        # injected from auth
                'project_id': 'str',
            }

        Returns:
            SharedConfigsResponse:
        """

        query = params.query or {}
        shared_config_vos, total_count = self.shared_config_mgr.list_shared_configs(query)
        shared_configs_info = [shared_config_vo.to_dict() for shared_config_vo in shared_config_vos]
        return SharedConfigsResponse(results=shared_configs_info, total_count=total_count)
