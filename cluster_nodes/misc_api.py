import json
import urllib

from cb_server_rest_util.connection import CBRestConnection
from global_vars import logger


class OtherClusterAPI(CBRestConnection):
    def __init__(self):
        super(OtherClusterAPI).__init__()
        self.test_log = logger.get("test")

    def set_minimum_bucket_replica_for_cluster(self, minimum_replica):
        api = self.base_url + 'settings/dataService'
        params = urllib.urlencode({'minReplicasCount': minimum_replica})
        status, content, header = self.http_request(api, 'POST', params)
        return status, content

    def get_minimum_bucket_replica_for_cluster(self):
        api = self.base_url + 'settings/dataService'
        status, content, header = self.http_request(api, 'GET')
        if status:
            json_parsed = json.loads(content)
            return json_parsed["minReplicasCount"]
        else:
            return None

