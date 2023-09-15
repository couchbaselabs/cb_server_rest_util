"""
https://docs.couchbase.com/server/current/rest-api/rest-index-service.html
"""

from cb_server_rest_util.connection import CBRestConnection


class QueryFunctions(CBRestConnection):
    def __init__(self):
        super(QueryFunctions).__init__()
