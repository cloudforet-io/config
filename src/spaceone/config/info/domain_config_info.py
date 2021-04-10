import functools
from spaceone.api.config.v1 import domain_config_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from spaceone.config.model.domain_config_model import DomainConfig

__all__ = ['DomainConfigInfo', 'DomainConfigsInfo']


def DomainConfigInfo(domain_config_vo: DomainConfig, minimal=False):
    info = {
        'name': domain_config_vo.name,
    }

    if not minimal:
        info.update({
            'data': change_struct_type(domain_config_vo.data),
            'tags': change_struct_type(utils.tags_to_dict(domain_config_vo.tags)),
            'schema': domain_config_vo.schema,
            'domain_id': domain_config_vo.domain_id,
            'created_at': utils.datetime_to_iso8601(domain_config_vo.created_at)
        })

    return domain_config_pb2.DomainConfigInfo(**info)


def DomainConfigsInfo(domain_config_vos, total_count, **kwargs):
    return domain_config_pb2.DomainConfigsInfo(results=list(
        map(functools.partial(DomainConfigInfo, **kwargs), domain_config_vos)), total_count=total_count)
