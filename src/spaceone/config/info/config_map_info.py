import functools
from spaceone.api.config.v1 import config_map_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.config.model.config_map_model import ConfigMap

__all__ = ['ConfigMapInfo', 'ConfigMapsInfo']


def ConfigMapInfo(config_map_vo: ConfigMap, minimal=False):
    info = {
        'name': config_map_vo.name,
    }

    if not minimal:
        info.update({
            'data': change_struct_type(config_map_vo.data),
            'tags': change_struct_type(config_map_vo.tags),
            'domain_id': config_map_vo.domain_id,
            'created_at': change_timestamp_type(config_map_vo.created_at)
        })

    return config_map_pb2.ConfigMapInfo(**info)


def ConfigMapsInfo(config_map_vos, total_count, **kwargs):
    return config_map_pb2.ConfigMapsInfo(results=list(
        map(functools.partial(ConfigMapInfo, **kwargs), config_map_vos)), total_count=total_count)
