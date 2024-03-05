from cb_server_rest_util.cluster_nodes.cluster_init_provision \
    import ClusterInitializationProvision
from cb_server_rest_util.cluster_nodes.node_add_remove import \
    NodeAdditionRemoval
from cb_server_rest_util.cluster_nodes.rebalance \
    import RebalanceRestAPI
from cb_server_rest_util.cluster_nodes.settings_and_connections \
    import SettingsAndConnectionsAPI
from cb_server_rest_util.cluster_nodes.status_and_events \
    import StatusAndEventsAPI


class ClusterRestAPI(ClusterInitializationProvision,
                     NodeAdditionRemoval,
                     RebalanceRestAPI,
                     SettingsAndConnectionsAPI,
                     StatusAndEventsAPI):
    def __init__(self, server):
        """
        Main gateway for all Cluster Rest Operations
        """
        super(ClusterRestAPI, self).__init__()

        self.set_server_values(server)
        self.set_endpoint_urls(server)
        self.check_if_couchbase_is_active(self, max_retry=5)
