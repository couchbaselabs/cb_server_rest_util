"""
https://docs.couchbase.com/server/current/rest-api/rest-adding-and-removing-nodes.html
"""
from cb_server_rest_util.connection import CBRestConnection


class NodeAdditionRemoval(CBRestConnection):
    def __init__(self):
        super(NodeAdditionRemoval).__init__()

    def add_node(self, host_name, username, password, services):
        """
        POST :: /controller/addNode
        docs.couchbase.com/server/current/rest-api/rest-cluster-addnodes.html
        """
        raise NotImplementedError()

    def join_node_to_cluster(self, cluster_member_host_ip, cluster_member_port,
                             username, password, services):
        """
        POST :: /node/controller/doJoinCluster
        docs.couchbase.com/server/current/rest-api/rest-cluster-joinnode.html
        """
        raise NotImplementedError()

    def eject_node(self, otp_node):
        """
        POST :: /controller/ejectNode
        docs.couchbase.com/server/current/rest-api/rest-cluster-removenode.html
        """
        raise NotImplementedError()

