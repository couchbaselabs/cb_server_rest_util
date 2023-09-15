import json

from cb_server_rest_util.connection import CBRestConnection


class AuthorizationAPI(CBRestConnection):
    '''
    Authorization by means of Role-Based Access Control can be manage with the REST API.
    https://docs.couchbase.com/server/current/rest-api/rest-security.html#authorization
    '''

    def __init__(self):
        super(AuthorizationAPI).__init__()

    def add_set_builtin_user(self, user_id, payload):
        url = "settings/rbac/users/local/" + user_id
        api = self.base_url + url
        status, content, header = self.http_request(api, 'PUT', payload)
        if not status:
            raise Exception(content)
        return json.loads(content)

    def delete_builtin_user(self, user_id):
        url = "settings/rbac/users/local/" + user_id
        api = self.base_url + url
        status, content, header = self.http_request(api, 'DELETE')
        if not status:
            self.log.error("%s - %s" % (user_id, content))
        return json.loads(content)


