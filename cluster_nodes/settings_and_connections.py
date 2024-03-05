"""
https://docs.couchbase.com/server/current/rest-api/rest-rebalance-overview.html
"""
from cb_server_rest_util.connection import CBRestConnection


class SettingsAndConnectionsAPI(CBRestConnection):
    def __init__(self):
        super(SettingsAndConnectionsAPI, self).__init__()

    def set_internal_settings(self, key, value):
        """
        GET / POST :: /internalSettings
        docs.couchbase.com/server/current/rest-api/rest-get-internal-setting.html
        """
        api = self.base_url + "/internalSettings"
        status, content, response = self.http_request(
            api, CBRestConnection.POST, data={key: value})
        if status:
            content = response.json()
        return status, content
