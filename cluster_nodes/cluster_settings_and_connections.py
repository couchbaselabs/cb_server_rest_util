import json
import urllib

from cb_server_rest_util.connection import CBRestConnection
from global_vars import logger


class SettingAndConnectionsAPI(CBRestConnection):
    def __init__(self):
        super(SettingAndConnectionsAPI, self).__init__()
        self.test_log = logger.get("test")

    def get_internalSettings(self, param):
        """allows to get internalSettings values for:
            indexAwareRebalanceDisabled, rebalanceIndexWaitingDisabled,
            rebalanceIndexPausingDisabled, maxParallelIndexers,
            maxParallelReplicaIndexers, maxBucketCount"""
        api = self.base_url + "internalSettings"
        status, content, header = self.http_request(api)
        json_parsed = json.loads(content)
        param = json_parsed[param]
        return param

    def set_internalSetting(self, param, value):
        "Set any internal setting"
        api = self.base_url + "internalSettings"

        if isinstance(value, bool):
            value = str(value).lower()

        params = urllib.urlencode({param: value})
        status, content, header = self.http_request(api, "POST", params)
        self.test_log.debug('Update internal setting {0}={1}'.format(param, value))
        return status