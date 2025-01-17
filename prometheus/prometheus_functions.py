from cb_server_rest_util.connection import CBRestConnection


class PrometheusFunctions(CBRestConnection):
    def __init__(self):
        super(PrometheusFunctions).__init__()

    def query_prometheus(self, query):
        """
        GET :: /_prometheus/api/v1/query?query={query}
        """

        api = self.base_url +  f"/_prometheus/api/v1/query?query={query}"
        status, content, _ = self.request(api, self.GET)
        return status, content