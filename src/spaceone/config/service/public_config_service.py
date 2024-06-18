import logging
from typing import Union

from spaceone.core.error import ERROR_REQUIRED_PARAMETER
from spaceone.core.service import *

from spaceone.config.manager.identity_manager import IdentityManager
from spaceone.config.manager.public_config_manager import PublicConfigManager
from spaceone.config.model.public_config.database import PublicConfig
from spaceone.config.model.public_config.response import *
from spaceone.config.model.public_config.request import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class PublicConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.public_config_mgr = PublicConfigManager()

    @transaction(permission="config:PublicConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def create(self, params: PublicConfigCreateRequest) -> Union[PublicConfigResponse, dict]:
        """Create workspace config

        Args:
            params (dict): {
                'name': 'str',              # required
                'data': 'dict',             # required
                'tags': 'dict',
                'resource_group' : 'str',   # required
                'users_project_id': 'str',  # injected from auth
                'project_id': 'str'
                'workspace_id': 'str'       # injected from auth
                'domain_id': 'str'          # injected from auth
            }

        Returns:
            public_config_vo (object)
        """

        public_config_vo = self.create_public_config(params.dict())

        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def update(self, params: PublicConfigUpdateRequest) -> Union[PublicConfigResponse, dict]:
        """Update public config

        Args:
            params (dict): {
                'name': 'str',              # required
                'data': 'dict',
                'tags': 'dict',
                "user_projects": 'list',    # injected from auth
                'project_id': 'str',
                'workspace_id': 'str'       # injected from auth
                'domain_id': 'str'          # injected from auth
            }

        Returns:
            domain_config_vo (object)
        """

        domain_id = params.domain_id
        workspace_id = params.workspace_id
        project_id = params.user_projects or params.project_id

        public_config_vo = self.public_config_mgr.get_public_config(params.name, domain_id, workspace_id, project_id)

        public_config_vo = self.public_config_mgr.update_public_config_by_vo(params.dict(exclude_unset=True),
                                                                             public_config_vo)

        return PublicConfigResponse(**public_config_vo.to_dict())

    # @transaction(permission="config:PublicConfig.write",
    #              role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    # @convert_model
    # def set(self, params: PublicConfigSetRequest) -> Union[PublicConfigResponse, dict]:
    #     """Set domain config (create or update)
    #
    #     Args:
    #         params (dict): {
    #             'name': 'str',        # required
    #             'data': 'dict',       # required
    #             'tags': 'dict',
    #             'workspace_id': 'str' # injected from auth
    #             'domain_id': 'str'    # injected from auth
    #         }
    #
    #     Returns:
    #         public_config_vo (object)
    #     """
    #     # need resource_group
    #     domain_id = params.domain_id
    #     workspace_id = params.workspace_id
    #     project_id = params.user_projects or params.project_id
    #
    #     public_config_vos = self.public_config_mgr.filter_public_configs(
    #         name=params.name, domain_id=domain_id, workspace_id=workspace_id, project_id=project_id
    #     )
    #
    #     if public_config_vos.count() == 0:
    #         public_config_vo = self.create_public_config(params.dict())
    #     else:
    #         public_config_vo = self.public_config_mgr.update_public_config_by_vo(
    #             params.dict(exclude_unset=True), public_config_vos[0]
    #         )
    #     return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.write",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def delete(self, params: PublicConfigDeleteRequest) -> None:
        """Delete workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'user_projects': 'list',
                'project_id': 'str',
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            None
        """

        workspace_id = params.workspace_id
        project_id = params.project_id or params.user_projects

        public_config_vo = self.public_config_mgr.get_public_config(params.name, params.domain_id, workspace_id,
                                                                    project_id)
        self.public_config_mgr.delete_public_config_by_vo(public_config_vo)

    @transaction(permission="config:PublicConfig.read",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @convert_model
    def get(self, params: PublicConfigGetRequest) -> Union[PublicConfigResponse, dict]:
        """Get workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'user_projects': 'list',
                'project_id': 'str',
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            public_config_vo (object)
        """

        public_config_vo = self.public_config_mgr.get_public_config(params.name, params.domain_id, params.workspace_id,
                                                                    params.user_projects)

        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.read",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @append_query_filter(["name", "domain_id"])
    @append_keyword_filter(["name"])
    @change_value_by_rule("APPEND", "workspace_id", "*")
    @change_value_by_rule("APPEND", "project_id", "*")
    @convert_model
    def list(self, params: PublicConfigSearchQueryRequest) -> Union[PublicConfigsResponse, dict]:
        """List workspace configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v2.Query)'
                'name': 'str',
                'user_projects': 'list',
                'workspace_id': 'str',                         # injected from auth
                'domain_id': 'str',                             # injected from auth
            }

        Returns:
            public_configs_vos (objects)
            total_count (int)
        """

        query = params.query or {}
        public_config_vos, total_count = self.public_config_mgr.list_public_configs(query)
        workspaces_info = [public_config_vo.to_dict() for public_config_vo in public_config_vos]
        return PublicConfigsResponse(results=workspaces_info, total_count=total_count)

    @transaction(permission="config:PublicConfig.read",
                 role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @append_query_filter(["workspace_id", "domain_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def stat(self, params: PublicConfigQueryRequest) -> dict:
        """ Stat workspace configs
        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'    # required
                'workspace_id': 'str',                                    # injected from auth
                'domain_id': 'str',                                       # required
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.query or {}
        return self.public_config_mgr.stat_public_configs(query)

    def create_public_config(self, params: dict) -> PublicConfig:
        domain_id = params["domain_id"]
        resource_group = params["resource_group"]
        workspace_id = params.get("workspace_id")
        project_id = params.get("project_id")

        identity_mgr: IdentityManager = self.locator.get_manager(IdentityManager)

        if resource_group == 'DOMAIN':
            params["workspace_id"] = "*"
            params["project_id"] = "*"
        elif resource_group == 'WORKSPACE':
            if params.get("workspace_id") is None:
                raise ERROR_REQUIRED_PARAMETER(key='workspace_id')

            identity_mgr.check_workspace(workspace_id, domain_id)
            params["project_id"] = "*"
        else:
            if workspace_id is None:
                raise ERROR_REQUIRED_PARAMETER(key='workspace_id')
            if project_id is None:
                raise ERROR_REQUIRED_PARAMETER(key='project_id')

            identity_mgr.check_workspace(workspace_id, domain_id)
            identity_mgr.get_project(project_id, domain_id)

        public_config_vo = self.public_config_mgr.create_public_config(params)
        return public_config_vo
