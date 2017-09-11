from __future__ import absolute_import

import six

from django.core.cache import cache, get_cache, InvalidCacheBackendError

from sentry.interfaces.base import get_interfaces


try:
    hash_cache = get_cache('preprocess_hash')
except InvalidCacheBackendError:
    hash_cache = cache


def get_raw_cache_key(project_id, event_id):
    return 'e:raw:{1}:{0}'.format(project_id, event_id)


def get_preprocess_hash_inputs(event):
    return get_preprocess_hash_inputs_with_reason(event)[1]


def get_preprocess_hash_inputs_with_reason(data):
    interfaces = get_interfaces(data, is_processed_data=False)
    for interface in six.itervalues(interfaces):
        # normalize_in_app hasn't run on the data, so
        # `in_app` isn't necessarily accurate
        result = interface.get_hash(data['platform'], system_frames=True)
        if not result:
            continue
        return (interface.get_path(), result)
    return ('message', [data['message']])
