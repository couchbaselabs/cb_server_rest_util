from cb_constants import CbServer
from cb_server_rest_util.analytics.analytics_api import AnalyticsRestAPI
from cb_server_rest_util.cluster_nodes.cluster_nodes_api import ClusterRestAPI
from cb_server_rest_util.index.index_api import IndexRestAPI
from cb_server_rest_util.query.query_api import QueryRestAPI


class RestConnection(object):
    def __init__(self, server):
        self.server = server

        self.cluster = ClusterRestAPI(self.server)
        self.index = None
        self.query = None
        self.analytics = None
        self.eventing = None
        self.fts = None
        self.backup = None

    def activate_service_api(self, service_list):
        if CbServer.Services.INDEX in service_list:
            self.index = IndexRestAPI(self.server)
        if CbServer.Services.N1QL in service_list:
            self.query = QueryRestAPI(self.server)
        if CbServer.Services.CBAS in service_list:
            self.analytics = AnalyticsRestAPI(self.server)
        if CbServer.Services.EVENTING in service_list:
            pass
        if CbServer.Services.FTS in service_list:
            pass
        if CbServer.Services.BACKUP in service_list:
            pass
