from cb_server_rest_util.connection import CBRestConnection


class AnalyticsRestAPI(CBRestConnection):
    def __init__(self, server):
        super(AnalyticsRestAPI).__init__()

        self.set_server_values(server)
        self.set_endpoint_urls(server)
        self.check_if_couchbase_is_active(self, max_retry=5)
