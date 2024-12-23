import logging
from typing import Tuple, List
from mongoengine import QuerySet

from spaceone.core.manager import BaseManager

from spaceone.config.model.shared_config.database import SharedConfig

_LOGGER = logging.getLogger(__name__)


class SharedConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared_config_model = SharedConfig

    def create_shared_config(self, params: dict) -> SharedConfig:
        def _rollback(vo: SharedConfig):
            _LOGGER.info(
                f"[create_shared_config._rollback] " f"Delete shared config : {vo.name}"
            )
            vo.delete()

        shared_config_vo: SharedConfig = self.shared_config_model.create(params)
        self.transaction.add_rollback(_rollback, shared_config_vo)

        return shared_config_vo

    def update_shared_config_by_vo(
        self, params: dict, shared_config_vo: SharedConfig
    ) -> SharedConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f'[update_shared_config_by_vo._rollback] Revert Data : {old_data["name"]}'
            )
            shared_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, shared_config_vo.to_dict())

        return shared_config_vo.update(params)

    def delete_shared_config_by_vo(self, shared_config_vo: SharedConfig) -> None:
        shared_config_vo.delete()

    def get_shared_config(
        self,
        name: str,
        domain_id: str,
        workspace_id: str = None,
        user_projects: List[str] = None
    ) -> SharedConfig:
        conditions = {"name": name, "domain_id": domain_id}

        if workspace_id:
            conditions["workspace_id"] = workspace_id

        if user_projects:
            conditions["project_id"] = user_projects

        return self.shared_config_model.get(**conditions)

    def filter_shared_configs(self, **conditions) -> QuerySet:
        return self.shared_config_model.filter(**conditions)

    def list_shared_configs(self, query: dict) -> Tuple[QuerySet, int]:
        return self.shared_config_model.query(**query)

    def stat_shared_configs(self, query: dict) -> dict:
        return self.shared_config_model.stat(**query)
