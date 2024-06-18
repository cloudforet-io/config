import logging
from typing import Tuple, Union

from mongoengine import QuerySet
from spaceone.core.manager import BaseManager

from spaceone.config.model.public_config.database import PublicConfig

_LOGGER = logging.getLogger(__name__)


class PublicConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.public_config_model = PublicConfig

    def create_public_config(self, params: dict) -> PublicConfig:
        def _rollback(vo: PublicConfig) -> None:
            _LOGGER.info(
                f"[create_public_config._rollback] " f"Delete public config : {vo.name}"
            )
            vo.delete()

        public_config_vo: PublicConfig = self.public_config_model.create(params)
        self.transaction.add_rollback(_rollback, public_config_vo)

        return public_config_vo

    def update_public_config_by_vo(
            self, params: dict, public_config_vo: PublicConfig
    ) -> PublicConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f'[update_public_config_by_vo._rollback] Revert Data : {old_data["name"]}'
            )
            public_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, public_config_vo.to_dict())

        return public_config_vo.update(params)

    @staticmethod
    def delete_public_config_by_vo(public_config_vo: PublicConfig) -> None:
        public_config_vo.delete()

    def get_public_config(self, name: str, domain_id: str, workspace_id: Union[list, str, None],
                          project_id: Union[list, str, None]) -> PublicConfig:
        conditions = {
            "name": name,
            "domain_id": domain_id,
        }
        if workspace_id:
            conditions["workspace_id"] = workspace_id
        if project_id:
            conditions["project_id"] = project_id

        return self.public_config_model.get(**conditions)

    def filter_public_configs(self, **conditions):
        return self.public_config_model.filter(**conditions)

    def list_public_configs(self, query: dict) -> Tuple[QuerySet, int]:
        return self.public_config_model.query(**query)

    def stat_public_configs(self, query: dict) -> dict:
        return self.public_config_model.stat(**query)
