from cb_server_rest_util.prometheus.prometheus_functions import PrometheusFunctions


class PrometheusRestAPI(PrometheusFunctions):
    def __init__(self, server):
        super(PrometheusRestAPI).__init__()

        self.set_server_values(server)
        self.set_endpoint_urls(server)
        self.check_if_couchbase_is_active(self, max_retry=5)
