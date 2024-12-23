import logging
from typing import Tuple
from mongoengine import QuerySet

from spaceone.core.manager import BaseManager

from spaceone.config.model.domain_config.database import DomainConfig

_LOGGER = logging.getLogger(__name__)


class DomainConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_config_model = DomainConfig

    def create_domain_config(self, params: dict) -> DomainConfig:
        def _rollback(vo: DomainConfig):
            _LOGGER.info(
                f"[create_domain_config._rollback] " f"Delete domain config : {vo.name}"
            )
            vo.delete()

        domain_config_vo: DomainConfig = self.domain_config_model.create(params)
        self.transaction.add_rollback(_rollback, domain_config_vo)

        return domain_config_vo

    def update_domain_config_by_vo(
        self, params: dict, domain_config_vo: DomainConfig
    ) -> DomainConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f'[update_domain_config_by_vo._rollback] Revert Data : {old_data["name"]}'
            )
            domain_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, domain_config_vo.to_dict())

        return domain_config_vo.update(params)

    def delete_domain_config_by_vo(self, domain_config_vo: DomainConfig) -> None:
        domain_config_vo.delete()

    def get_domain_config(self, name: str, domain_id: str) -> DomainConfig:
        return self.domain_config_model.get(
            name=name, domain_id=domain_id
        )

    def filter_domain_configs(self, **conditions) -> QuerySet:
        return self.domain_config_model.filter(**conditions)

    def list_domain_configs(self, query: dict) -> Tuple[QuerySet, int]:
        return self.domain_config_model.query(**query)

    def stat_domain_configs(self, query: dict) -> dict:
        return self.domain_config_model.stat(**query)
