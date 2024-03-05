"""
https://docs.couchbase.com/server/current/rest-api/rest-rebalance-overview.html
"""
from cb_server_rest_util.connection import CBRestConnection


class RebalanceRestAPI(CBRestConnection):
    def __init__(self):
        super(RebalanceRestAPI, self).__init__()

    def rebalance(self, known_nodes, eject_nodes=None):
        """
        POST :: /controller/rebalance
        docs.couchbase.com/server/current/rest-api/rest-cluster-rebalance.html
        """
        api = self.base_url + "/controller/rebalance"
        known_nodes = ','.join(known_nodes)
        params = {"knownNodes": known_nodes}
        if eject_nodes:
            params["ejectedNodes"] = eject_nodes
        status, content, _ = self.http_request(api, self.POST,
                                               data=params)
        return status, content

    def stop_rebalance(self):
        """
        POST :: /controller/stopRebalance
        No documentation present
        """
        api = self.base_url + '/controller/stopRebalance'
        status, content, _ = self.http_request(api, 'POST')
        return status, content

    def rebalance_progress(self):
        """
        GET :: /pools/default/rebalanceProgress
        docs.couchbase.com/server/current/rest-api/rest-get-rebalance-progress.html
        """
        raise NotImplementedError()

    def retry_rebalance(self, enabled=None, after_time_period=None,
                        max_attempts=None):
        """
        GET / POST :: /pools/default/retryRebalance
        docs.couchbase.com/server/current/rest-api/rest-configure-rebalance-retry.html
        """
        method = self.GET
        if enabled is not None \
                or after_time_period is not None \
                or max_attempts is not None:
            method = self.POST
            params = {"enabled": enabled,
                      "afterTimePeriod": after_time_period,
                      "maxAttempts": max_attempts}
        raise NotImplementedError()

    def pending_retry_rebalance(self):
        """
        GET :: /pools/default/pendingRetryRebalance
        docs.couchbase.com/server/current/rest-api/rest-get-rebalance-retry.html
        """
        raise NotImplementedError()

    def cancel_retry_rebalance(self, rebalance_id):
        """
        POST :: /controller/cancelRebalanceRetry/<rebalance-id>
        docs.couchbase.com/server/current/rest-api/rest-cancel-rebalance-retry.html
        """
        raise NotImplementedError()

    def limit_concurrent_vbucket_moves(self, rebalance_moves_per_node=None):
        """
        GET / POST :: /settings/rebalance
        docs.couchbase.com/server/current/rest-api/rest-limit-rebalance-moves.html
        """
        method = self.GET
        if rebalance_moves_per_node is not None:
            method = self.POST
            params = {"rebalanceMovesPerNode": rebalance_moves_per_node}
        raise NotImplementedError()

    def set_index_aware_rebalance(self, index_aware_rebalace_disabled):
        """
        POST :: /internalSettings
        docs.couchbase.com/server/current/rest-api/rest-cluster-disable-query.html
        """
        params = {"indexAwareRebalanceDisabled": index_aware_rebalace_disabled}
        raise NotImplementedError()
