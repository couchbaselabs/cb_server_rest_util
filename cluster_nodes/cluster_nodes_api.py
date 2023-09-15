from cb_server_rest_util.cluster_nodes.cluster_init_provision import ClusterInitializationProvision
from cb_server_rest_util.cluster_nodes.cluster_status_and_events import ClusterStatusAndEvents
from cb_server_rest_util.cluster_nodes.rebalance import RebalanceRestAPI
from cb_server_rest_util.cluster_nodes.misc_api import OtherClusterAPI


class ClusterRestAPI(ClusterInitializationProvision, RebalanceRestAPI, OtherClusterAPI,ClusterStatusAndEvents):
    def __init__(self, server):
        """
        Main gateway for all Cluster Rest Operations
        """
        super(ClusterRestAPI, self).__init__()

        self.set_server_values(server)
        self.set_endpoint_urls(server)
        self.check_if_couchbase_is_active(self, max_retry=5)
