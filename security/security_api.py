from cb_server_rest_util.security.authorization_api import AuthorizationAPI


class SecurityAPI(AuthorizationAPI):
    def __init__(self, server):
        """
        The Security REST API provides the endpoints for general security, for authentication, and for authorization. For a list of the endpoints, see the tables below.
        """
        super(SecurityAPI, self).__init__()
        self.set_server_values(server)
        self.set_endpoint_urls(server)
