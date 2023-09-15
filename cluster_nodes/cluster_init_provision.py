"""
https://docs.couchbase.com/server/current/rest-api/rest-cluster-init-and-provisioning.html
https://docs.couchbase.com/server/current/rest-api/rest-adding-and-removing-nodes.html
"""
import urllib

from cb_server_rest_util.connection import CBRestConnection
from urllib3._collections import HTTPHeaderDict

from global_vars import logger


class ClusterInitializationProvision(CBRestConnection):
    def __init__(self):
        super(ClusterInitializationProvision).__init__()
        self.test_log = logger.get("test")

    def initialize_cluster(self, hostname, username, password,
                           data_path=None, index_path=None,
                           cbas_path=None, eventing_path=None,
                           java_home=None, send_stats=None,
                           cluster_name=None, services=None,
                           memory_quota=None, index_memory_quota=None,
                           eventing_memory_quota=None, fts_memory_quota=None,
                           cbas_memory_quota=None,
                           afamily=None, afamily_only=None,
                           node_encryption=None, indexer_storage_mode=None,
                           port='SAME', allowed_hosts=None):
        """
        POST /clusterInit
        docs.couchbase.com/server/current/rest-api/rest-initialize-cluster.html
        """
        end_point = '/clusterInit'
        url = self.base_url + end_point
        set_path = False

        data = HTTPHeaderDict()

        if hostname is not None:
            set_path = True
            data.add("hostname", hostname)

        if username is not None:
            set_path = True
            data.add("username", username)

        if password is not None:
            set_path = True
            data.add("password", password)

        if data_path is not None:
            set_path = True
            data.add("data_path", password)

        if data_path is not None:
            set_path = True
            data.add("data_path", password)

        if index_path is not None:
            data.add("index_path", index_path)

        if cbas_path is not None:
            data.add("cbas_path", cbas_path)

        if eventing_path is not None:
            data.add("eventing_path", eventing_path)

        if java_home is not None:
            data.add("java_home", java_home)

        if send_stats is not None:
            data.add("sendStats", send_stats)

        if cluster_name is not None:
            data.add("clusterName", cluster_name)

        if services is not None:
            data.add("services", services)
        else:
            data.add("services", ["kv"])

        if memory_quota is not None:
            data.add("memoryQuota", memory_quota)

        if index_memory_quota is not None:
            data.add("indexMemoryQuota", index_memory_quota)

        if eventing_memory_quota is not None:
            data.add("eventingMemoryQuota", eventing_memory_quota)

        if fts_memory_quota is not None:
            data.add("ftsMemoryQuota", fts_memory_quota)

        if cbas_memory_quota is not None:
            data.add("cbasMemoryQuota", cbas_memory_quota)

        if afamily is not None:
            data.add("afamily", afamily)

        if afamily_only is not None:
            data.add("afamilyOnly", afamily_only)

        if node_encryption is not None:
            data.add("nodeEncryption", node_encryption)

        if indexer_storage_mode is not None:
            data.add("indexerStorageMode", indexer_storage_mode)

        if port is not None:
            data.add("port", port)

        if allowed_hosts is not None:
            data.add("allowedHosts", allowed_hosts)

        if set_path:
            data = urllib.urlencode(data)
            status, content, header = self.http_request(url, 'POST', data)
            if status:
                self.test_log.debug("Setting paths: {0}: status {1}"
                                    .format(data, status))
            else:
                self.test_log.error("Unable to set data_path {0}: {1}"
                                    .format(data, content))
            return status

    def set_jre_path(self, jre_path=None, check=True):

        api = self.base_url + '/nodes/self/controller/settings'
        data = HTTPHeaderDict()
        paths = {}

        if jre_path:
            data.add('java_home', jre_path)
            paths['java_home'] = jre_path

        if paths:
            params = urllib.urlencode(paths)
            self.test_log.debug('/nodes/self/controller/settings params: {0}'
                                .format(urllib.urlencode(data)))
            status, content, header = self.http_request(api, 'POST', urllib.urlencode(data))
            if status:
                self.test_log.debug("Setting paths: {0}: status {1}"
                                    .format(data, status))
            else:
                self.test_log.warning("Unable to set data_path {0}: status {1}"
                                      .format(data, status))
                if not check:
                    return content
                else:
                    exit(1)
            return status

    def set_data_path(self, data_path=None, index_path=None, eventing_path=None, cbas_path=[]):
        """
        POST /nodes/self/controller/settings
        docs.couchbase.com/server/current/rest-api/rest-initialize-node.html
        """
        end_point = '/nodes/self/controller/settings'
        url = self.base_url + end_point
        set_path = False

        data = HTTPHeaderDict()

        if data_path:
            set_path = True
            data.add('data', data_path)
        if index_path:
            set_path = True
            data.add('index_path', index_path)
        if eventing_path:
            set_path = True
            data.add('eventing_path', index_path)
        if cbas_path:
            set_path = True
            import ast
            cbas_path = ast.literal_eval(cbas_path)
            for cbas in cbas_path:
                data.add('cbas_path', cbas)
        if set_path:
            data = urllib.urlencode(data)
            status, content, header = self.http_request(url, 'POST', data)
            if status:
                self.test_log.debug("Setting paths: {0}: status {1}"
                                    .format(data, status))
            else:
                self.test_log.error("Unable to set data_path {0}: {1}"
                                    .format(data, content))
            return status

    def establish_credentials(self, username, password, port="SAME"):
        """
        POST /settings/web
        docs.couchbase.com/server/current/rest-api/rest-establish-credentials.html
        """
        end_point = '/settings/web'
        url = self.base_url + end_point
        set_path = False

        data = HTTPHeaderDict()

        if username is not None:
            set_path = True
            data.add("username", username)

        if password is not None:
            set_path = True
            data.add("password", password)

        data.add("port", port)

        if set_path:
            data = urllib.urlencode(data)
            status, content, header = self.http_request(url, 'POST', data)
            if status:
                self.test_log.debug("Setting paths: {0}: status {1}"
                                    .format(data, status))
            else:
                self.test_log.error("Unable to set data_path {0}: {1}"
                                    .format(data, content))
            return status

    def rename_node(self, hostname):
        """
        POST /node/controller/rename
        docs.couchbase.com/server/current/rest-api/rest-name-node.html
        """
        raise NotImplementedError()

    def configure_memory(self):
        """
        POST /pools/default
        docs.couchbase.com/server/current/rest-api/rest-configure-memory.html
        """
        raise NotImplementedError()

    def setup_services(self):
        """
        POST /node/controller/setupServices
        docs.couchbase.com/server/current/rest-api/rest-set-up-services.html
        """
        raise NotImplementedError()

    def naming_the_cluster(self):
        """
        POST /node/controller/setupServices
        docs.couchbase.com/server/current/rest-api/rest-name-cluster.html
        """
        raise NotImplementedError()
