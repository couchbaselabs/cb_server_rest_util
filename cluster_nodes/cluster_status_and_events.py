import json
from time import sleep

from cb_server_rest_util.cluster_nodes.cluster_api_helper import RestParser
from cb_server_rest_util.connection import CBRestConnection
from global_vars import logger


class ClusterStatusAndEvents(CBRestConnection):
    def __init__(self):
        super(ClusterStatusAndEvents, self).__init__()
        self.test_log = logger.get("test")

    def view_cluster_details(self):
        api = self.base_url + "pools/default/"
        status, content, header = self.http_request(api)
        cluster_details = json.loads(content)
        if status:
            return status, cluster_details, header
        else:
            return status, None, header

    def get_alerts(self):
        _, cluster_details, _ = self.view_cluster_details()
        if cluster_details is not None and "alerts" in cluster_details:
            return cluster_details['alerts']
        return None

    def get_nodes(self, inactive_added=False, inactive_failed=False):
        nodes = []
        api = self.base_url + 'pools/default'
        status, content, header = self.view_cluster_details()
        count = 0
        while not content and count < 7:
            self.test_log.warning("Retrying get_nodes() after 5 seconds")
            sleep(5)
            status, content, header = self.http_request(api)
            count += 1
        if count == 7:
            raise Exception("could not get node info after 30 seconds")
        json_parsed = json.loads(content)
        nodes_to_consider = ["active"]
        # this is really useful when we want to do cbcollect on failed over/recovered node
        if inactive_added:
            nodes_to_consider.append("inactiveAdded")
        if inactive_failed:
            nodes_to_consider.append("inactiveFailed")
        if status:
            if "nodes" in json_parsed:
                for json_node in json_parsed["nodes"]:
                    node = RestParser(self.type).parse_get_nodes_response(
                        json_node)
                    node.rest_username = self.username
                    node.rest_password = self.password
                    if node.ip == "127.0.0.1":
                        node.ip = self.ip
                    # Only add nodes which are active on cluster
                    if node.clusterMembership in nodes_to_consider:
                        nodes.append(node)
                    else:
                        self.test_log.warn("{0} - Node not part of cluster {1}"
                                           .format(node.ip,
                                                   node.clusterMembership))
        return nodes
