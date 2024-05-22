import logging
from typing import Union

from spaceone.core.service import *

from spaceone.config.model.workspace_config.response import *
from spaceone.config.model.workspace_config.request import *
from spaceone.config.manager.workspace_config_manager import WorkspaceConfigManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class WorkspaceConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace_config_mgr = WorkspaceConfigManager()

    @transaction(permission="config:WorkspaceConfig.write", role_types=["WORKSPACE_OWNER"])
    @convert_model
    def create(self, params: WorkspaceConfigCreateRequest) -> Union[WorkspaceConfigResponse, dict]:
        """Create workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',       # required
                'tags': 'dict',
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            workspace_config_vo (object)
        """

        workspace_config_vo = self.workspace_config_mgr.create_workspace_config(params.dict())

        return WorkspaceConfigResponse(**workspace_config_vo.to_dict())

    @transaction(permission="config:WorkspaceConfig.write", role_types=["WORKSPACE_OWNER"])
    @convert_model
    def update(self, params: WorkspaceConfigUpdateRequest) -> Union[WorkspaceConfigResponse, dict]:
        """Update workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',
                'tags': 'dict',
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            domain_config_vo (object)
        """

        workspace_config_vo = self.workspace_config_mgr.get_workspace_config(params.name, params.workspace_id,
                                                                             params.domain_id)

        workspace_config_vo = self.workspace_config_mgr.update_workspace_config_by_vo(params.dict(exclude_unset=True),
                                                                                      workspace_config_vo)

        return WorkspaceConfigResponse(**workspace_config_vo.to_dict())

    @transaction(permission="config:WorkspaceConfig.write", role_types=["WORKSPACE_OWNER"])
    @convert_model
    def set(self, params: WorkspaceConfigSetRequest) -> Union[WorkspaceConfigResponse, dict]:
        """Set domain config (create or update)

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',       # required
                'tags': 'dict',
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            workspace_config_vo (object)
        """

        workspace_config_vos = self.workspace_config_mgr.filter_workspace_configs(
            name=params.name, workspace_id=params.workspace_id, domain_id=params.domain_id
        )

        if workspace_config_vos.count() == 0:
            workspace_config_vo = self.workspace_config_mgr.create_workspace_config(params.dict())
        else:
            workspace_config_vo = self.workspace_config_mgr.update_workspace_config_by_vo(
                params.dict(exclude_unset=True), workspace_config_vos[0]
            )
        return WorkspaceConfigResponse(**workspace_config_vo.to_dict())

    @transaction(permission="config:WorkspaceConfig.write", role_types=["WORKSPACE_OWNER"])
    @convert_model
    def delete(self, params: WorkspaceConfigDeleteRequest) -> None:
        """Delete workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            None
        """
        workspace_config_vo = self.workspace_config_mgr.get_workspace_config(params.name, params.workspace_id,
                                                                             params.domain_id)
        self.workspace_config_mgr.delete_workspace_config_by_vo(workspace_config_vo)

    @transaction(permission="config:WorkspaceConfig.read", role_types=["WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @check_required(["name", "domain_id"])
    def get(self, params: WorkspaceConfigGetRequest) -> Union[WorkspaceConfigResponse, dict]:
        """Get workspace config

        Args:
            params (dict): {
                'name': 'str',        # required
                'workspace_id': 'str' # injected from auth
                'domain_id': 'str'    # injected from auth
            }

        Returns:
            workspace_config_vo (object)
        """

        workspace_config_vo = self.workspace_config_mgr.get_workspace_config(params.name, params.workspace_id,
                                                                             params.domain_id)

        return WorkspaceConfigResponse(**workspace_config_vo.to_dict())

    @transaction(permission="config:WorkspaceConfig.read", role_types=["WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @append_query_filter(["name", "workspace_id", "domain_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def list(self, params: WorkspaceConfigSearchQueryRequest) -> Union[WorkspaceConfigsResponse, dict]:
        """List workspace configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v2.Query)'
                'name': 'str',
                'workspace_id': 'str',                         # injected from auth
                'domain_id': 'str',                             # injected from auth
            }

        Returns:
            workspace_configs_vos (objects)
            total_count (int)
        """

        query = params.query or {}
        workspace_config_vos, total_count = self.workspace_config_mgr.list_workspace_configs(query)
        workspaces_info = [workspace_config_vo.to_dict() for workspace_config_vo in workspace_config_vos]
        return WorkspaceConfigsResponse(results=workspaces_info, total_count=total_count)

    @transaction(permission="config:WorkspaceConfig.read", role_types=["WORKSPACE_OWNER", "WORKSPACE_MEMBER"])
    @append_query_filter(["workspace_id", "domain_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def stat(self, params: WorkspaceConfigQueryRequest) -> dict:
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
        return self.workspace_config_mgr.stat_workspace_configs(query)
