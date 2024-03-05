"""
https://docs.couchbase.com/server/current/rest-api/rest-rebalance-overview.html
"""
from cb_server_rest_util.connection import CBRestConnection


class StatusAndEventsAPI(CBRestConnection):
    def __init__(self):
        super(StatusAndEventsAPI, self).__init__()

    def cluster_tasks(self):
        """
        GET /pools/default/tasks
        docs.couchbase.com/server/current/rest-api/rest-get-cluster-tasks.html
        """
        api = self.base_url + "/pools/default/tasks"
        status, content, response = self.http_request(api)
        return status, content

    def rebalance_report(self, report_id):
        """
        GET /logs/rebalanceReport?reportID=<report-id>
        docs.couchbase.com/server/current/rest-api/rest-get-cluster-tasks.html
        """

    def cluster_info(self):
        """
        GET /pools
        docs.couchbase.com/server/current/rest-api/rest-cluster-get.html
        """
        api = self.base_url + "/pools"
        status, content, header = self.http_request(api)
        return status, content

    def cluster_details(self):
        """
        GET /pools/default
        docs.couchbase.com/server/current/rest-api/rest-cluster-details.html
        """
        api = self.base_url + "/pools/default"
        status, content, header = self.http_request(api)
        return status, content

    def node_details(self):
        """
        GET /nodes/self
        docs.couchbase.com/server/current/rest-api/rest-getting-storage-information.html
        """
        api = self.base_url + "/nodes/self"
        status, content, response = self.http_request(api)
        return status, content

    def get_node_statuses(self):
        """
        GET :: /nodeStatuses
        Not documented in CB docs
        """
        api = self.base_url + "/nodeStatuses"
        status, content, response = self.http_request(api)
        return status, content

    def ui_logs(self):
        """
        GET :: /logs
        Not documented in CB docs
        """
        api = self.base_url + '/logs'
        status, json_parsed, _ = self.http_request(api)
        # json_parsed = json.loads(json_parsed.decode("utf-8", "ignore"))
        return status, json_parsed
