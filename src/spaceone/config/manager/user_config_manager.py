import logging

from spaceone.core.manager import BaseManager

from spaceone.config.model.user_config_model import UserConfig

_LOGGER = logging.getLogger(__name__)


class UserConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_model: UserConfig = self.locator.get_model("UserConfig")

    def create_user_config(self, params: dict) -> UserConfig:
        def _rollback(vo: UserConfig):
            _LOGGER.info(
                f"[create_user_config._rollback] " f"Delete config map : {vo.name}"
            )
            vo.delete()

        user_config_vo: UserConfig = self.user_config_model.create(params)
        self.transaction.add_rollback(_rollback, user_config_vo)

        return user_config_vo

    def update_user_config(self, params: dict) -> UserConfig:
        user_config_vo: UserConfig = self.get_user_config(
            params["name"], params["user_id"], params["domain_id"]
        )
        return self.update_user_config_by_vo(params, user_config_vo)

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

    def delete_user_config(self, name: str, user_id: str, domain_id: str) -> None:
        user_config_vo: UserConfig = self.get_user_config(name, user_id, domain_id)
        user_config_vo.delete()

    def get_user_config(self, name: str, user_id: str, domain_id: str) -> UserConfig:
        return self.user_config_model.get(
            name=name, user_id=user_id, domain_id=domain_id
        )

    def filter_user_configs(self, **conditions: dict):
        return self.user_config_model.filter(**conditions)

    def list_user_configs(self, query: dict) -> dict:
        return self.user_config_model.query(**query)

    def state_user_configs(self, query: dict) -> dict:
        return self.user_config_model.stat(**query)
