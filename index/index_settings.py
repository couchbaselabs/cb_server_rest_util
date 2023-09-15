"""
https://docs.couchbase.com/server/current/rest-api/rest-index-service.html
"""

from cb_server_rest_util.connection import CBRestConnection


class IndexSettings(CBRestConnection):
    def __init__(self):
        super(IndexSettings).__init__()

    def get_gsi_settings(self):
        """
        GET :: /settings/indexes
        docs.couchbase.com/server/current/rest-api/get-settings-indexes.html
        """

    def set_gsi_settings(self):
        """
        POST :: /settings/indexes
        """

    def get_node_statistics(self):
        """
        GET :: /api/v1/stats
        """

    def get_keyspace_statistics(self, key_space):
        """
        GET :: /api/v1/stats/{keyspace}
        """

    def get_index_statistics(self, key_space, index_name):
        """
        GET :: /api/v1/stats/{keyspace}/{index}
        """
