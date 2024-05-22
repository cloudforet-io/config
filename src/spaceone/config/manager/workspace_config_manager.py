import logging
from typing import Tuple

from mongoengine import QuerySet
from spaceone.core.manager import BaseManager

from spaceone.config.model.workspace_config.database import WorkspaceConfig

_LOGGER = logging.getLogger(__name__)


class WorkspaceConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace_config_model = WorkspaceConfig

    def create_workspace_config(self, params: dict) -> WorkspaceConfig:
        def _rollback(vo: WorkspaceConfig) -> None:
            _LOGGER.info(
                f"[create_workspace_config._rollback] " f"Delete workspace config : {vo.name}"
            )
            vo.delete()

        workspace_config_vo: WorkspaceConfig = self.workspace_config_model.create(params)
        self.transaction.add_rollback(_rollback, workspace_config_vo)

        return workspace_config_vo

    def update_workspace_config_by_vo(
            self, params: dict, workspace_config_vo: WorkspaceConfig
    ) -> WorkspaceConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f'[update_workspace_config_by_vo._rollback] Revert Data : {old_data["name"]}'
            )
            workspace_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, workspace_config_vo.to_dict())

        return workspace_config_vo.update(params)

    @staticmethod
    def delete_workspace_config_by_vo(workspace_config_vo: WorkspaceConfig) -> None:
        workspace_config_vo.delete()

    def get_workspace_config(self, name: str, workspace_id: str, domain_id: str) -> WorkspaceConfig:
        return self.workspace_config_model.get(name=name, workspace_id=workspace_id, domain_id=domain_id)

    def filter_workspace_configs(self, **conditions):
        return self.workspace_config_model.filter(**conditions)

    def list_workspace_configs(self, query: dict) -> Tuple[QuerySet, int]:
        return self.workspace_config_model.query(**query)

    def stat_workspace_configs(self, query: dict) -> dict:
        return self.workspace_config_model.stat(**query)
