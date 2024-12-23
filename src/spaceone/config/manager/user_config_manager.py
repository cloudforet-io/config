import logging
from typing import Tuple
from mongoengine import QuerySet

from spaceone.core.manager import BaseManager

from spaceone.config.model.user_config.database import UserConfig

_LOGGER = logging.getLogger(__name__)


class UserConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_model = UserConfig

    def create_user_config(self, params: dict) -> UserConfig:
        def _rollback(vo: UserConfig):
            _LOGGER.info(
                f"[create_user_config._rollback] " f"Delete user config : {vo.name}"
            )
            vo.delete()

        user_config_vo: UserConfig = self.user_config_model.create(params)
        self.transaction.add_rollback(_rollback, user_config_vo)

        return user_config_vo

    def update_user_config_by_vo(
        self, params: dict, user_config_vo: UserConfig
    ) -> UserConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f'[update_user_config_by_vo._rollback] Revert Data : {old_data["name"]}'
            )
            user_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, user_config_vo.to_dict())

        return user_config_vo.update(params)

    def delete_user_config_by_vo(self, user_config_vo: UserConfig) -> None:
        user_config_vo.delete()

    def get_user_config(self, name: str, domain_id: str, user_id: str) -> UserConfig:
        return self.user_config_model.get(
            name=name, domain_id=domain_id, user_id=user_id
        )

    def filter_user_configs(self, **conditions) -> QuerySet:
        return self.user_config_model.filter(**conditions)

    def list_user_configs(self, query: dict) -> Tuple[QuerySet, int]:
        return self.user_config_model.query(**query)

    def stat_user_configs(self, query: dict) -> dict:
        return self.user_config_model.stat(**query)
