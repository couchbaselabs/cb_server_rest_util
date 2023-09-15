import base64
import json
import logging
import socket
import traceback

import requests
import time

from Cb_constants import CbServer, ClusterRun, constants
from cb_server_rest_util import httplib2
from common_lib import sleep
from custom_exceptions.exception import ServerUnavailableException


class CBRestConnection(object):
    DELETE = "DELETE"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"

    @staticmethod
    def get_auth(headers):
        key = 'Authorization'
        if key in headers:
            val = headers[key]
            if val.startswith("Basic "):
                return "auth: " + base64.decodestring(val[6:])
        return ""

    def set_server_values(self, server):
        self.ip = server.ip
        self.port = server.port
        self.username = server.rest_username
        self.password = server.rest_password
        self.type = "default"

    def set_endpoint_urls(self, server):
        index_port = constants.index_port
        fts_port = constants.fts_port
        query_port = constants.n1ql_port
        eventing_port = constants.eventing_port
        backup_port = constants.backup_port
        hostname = None

        if hasattr(server, 'index_port') and server.index_port:
            index_port = server.index_port
        if hasattr(server, 'query_port') and server.query_port:
            query_port = server.query_port
        if hasattr(server, 'fts_port') and server.fts_port:
            fts_port = server.fts_port
        if hasattr(server, 'eventing_port') and server.eventing_port:
            eventing_port = server.eventing_port
        if hasattr(server, 'hostname') and server.hostname \
                and server.hostname.find(self.ip) == -1:
            hostname = server.hostname
        if hasattr(server, 'services'):
            self.services = server.services

        if CbServer.use_https:
            if ClusterRun.is_enabled:
                if int(self.port) < ClusterRun.ssl_port:
                    self.port = int(self.port) + 10000
            else:
                self.port = CbServer.ssl_port
                index_port = CbServer.ssl_index_port
                query_port = CbServer.ssl_n1ql_port
                fts_port = CbServer.ssl_fts_port
                eventing_port = CbServer.ssl_eventing_port
                backup_port = CbServer.ssl_backup_port

        http_url = "http://{0}:{1}/"
        https_url = "https://{0}:{1}/"
        generic_url = http_url
        if CbServer.use_https:
            generic_url = https_url
        url_host = "{0}".format(self.ip)
        if hostname:
            url_host = "{0}".format(hostname)

        self.base_url = generic_url.format(url_host, self.port)
        self.index_url = generic_url.format(url_host, index_port)
        self.query_url = generic_url.format(url_host, query_port)
        self.fts_url = generic_url.format(url_host, fts_port)
        self.eventing_url = generic_url.format(url_host, eventing_port)
        self.backup_url = generic_url.format(url_host, backup_port)
        if hasattr(server, "type"):
            self.type = server.type

    @staticmethod
    def check_if_couchbase_is_active(rest, max_retry=5):
        api = rest.base_url + 'nodes/self'
        if rest.type != "default" or rest.type == "nebula":
            api = rest.base_url + "pools/default"
        # for Node is unknown to this cluster error
        node_unknown_msg = "Node is unknown to this cluster"
        unexpected_server_err_msg = "Unexpected server error, request logged"
        headers = rest.create_headers(rest.username, rest.password,
                                      'application/json')
        for iteration in xrange(max_retry):
            http_res = None
            success = False
            try:
                status, content, header = rest.http_request(
                    api, CBRestConnection.GET, headers=headers, timeout=30)
                http_res = json.loads(content)
                if status:
                    success = True
                else:
                    rest.log.debug("{0} with status {1}: {2}".format(api, status, http_res))
            except ValueError as e:
                rest.log.critical(e)
            if not success and type(http_res) == unicode \
                    and (http_res.find(node_unknown_msg) > -1
                         or http_res.find(unexpected_server_err_msg) > -1):
                rest.log.error("Error {0}, 5 seconds sleep before retry"
                               .format(http_res))
                sleep(5, log_type="infra")
                if iteration == 2:
                    rest.log.error("Node {0}:{1} is in a broken state!"
                                   .format(rest.ip, rest.port))
                    raise ServerUnavailableException(rest.ip)
                continue
            else:
                break

    def __init__(self):
        """
        Contains the place-holders. Need to be initialized by the
        implementing *_api.py file / module
        """
        # Basic info about the server
        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        self.type = None
        self.services = None

        # Valid URL endpoints for reusing
        self.base_url = None
        self.index_url = None
        self.query_url = None
        self.fts_url = None
        self.eventing_url = None
        self.backup_url = None

        # For tracking sessions (if any)
        self.session = None

        self.log = logging.getLogger("cb_server_rest_util")

    def create_headers(self, username=None, password=None,
                       content_type='application/x-www-form-urlencoded'):
        username = username or self.username
        password = password or self.password
        authorization = base64.b64encode(
            '{}:{}'.format(username, password).encode()).decode()
        return {'Content-Type': content_type,
                'Authorization': 'Basic %s' % authorization,
                'Connection': 'close',
                'Accept': '*/*'}

    def get_headers_for_content_type_json(self):
        authorization = base64.b64encode(
            '{}:{}'.format(self.username, self.password).encode()).decode()
        return {'Content-type': 'application/json',
                'Authorization': 'Basic %s' % authorization}

    def _urllib_request(self, api, method='GET', params='', headers=None,
                        timeout=300, verify=False, session=None):
        if session is None:
            session = requests.Session()
        end_time = time.time() + timeout
        while True:
            try:
                if method == "GET":
                    response = session.get(api, params=params, headers=headers,
                                           timeout=timeout, verify=verify)
                elif method == "POST":
                    response = session.post(api, data=params, headers=headers,
                                            timeout=timeout, verify=verify)
                elif method == "DELETE":
                    response = session.delete(api, data=params, headers=headers,
                                              timeout=timeout, verify=verify)
                elif method == "PUT":
                    response = session.put(api, data=params, headers=headers,
                                           timeout=timeout, verify=verify)
                elif method == "PATCH":
                    response = session.patch(api, data=params, headers=headers,
                                             timeout=timeout, verify=verify)
                else:
                    raise NotImplemented("Unsupported method {}".format(method))

                if 200 <= response.status_code < 300:
                    return True, response.content, response
                else:
                    try:
                        json_parsed = json.loads(response.content)
                    except ValueError:
                        json_parsed = dict()
                        json_parsed["error"] = "status: {0}, content: {1}".format(
                            response.status_code, response.content)
                    reason = "unknown"
                    if "error" in json_parsed:
                        reason = json_parsed["error"]
                    elif "errors" in json_parsed:
                        reason = json_parsed["errors"]
                    if ("accesskey" in params.lower()) or (
                            "secretaccesskey" in params.lower()) or (
                            "password" in params.lower()) or (
                            "secretkey" in params.lower()):
                        message = '{0} {1} body: {2} headers: {3} ' \
                                  'error: {4} reason: {5} {6} {7}'. \
                            format(method, api,
                                   "Body is being redacted because it contains sensitive info",
                                   headers, response.status_code, reason,
                                   response.content.rstrip('\n'),
                                   self.get_auth(headers))
                    else:
                        message = '{0} {1} body: {2} headers: {3} ' \
                                  'error: {4} reason: {5} {6} {7}'. \
                            format(method, api, params, headers,
                                   response.status_code, reason,
                                   response.content.rstrip('\n'),
                                   self.get_auth(headers))
                    self.log.debug(message)
                    self.log.debug(''.join(traceback.format_stack()))
                    return False, response.content, response
            except requests.exceptions.HTTPError as errh:
                self.log.error("HTTP Error {0}".format(errh))
            except requests.exceptions.ConnectionError as errc:
                if "Illegal state exception" in str(errc):
                    # Known ssl bug, retry
                    pass
                else:
                    self.log.debug("Error Connecting {0}".format(errc))
                if time.time() > end_time:
                    raise ServerUnavailableException(ip=self.ip)
            except requests.exceptions.Timeout as errt:
                self.log.error("Timeout Error: {0}".format(errt))
                if time.time() > end_time:
                    raise ServerUnavailableException(ip=self.ip)
            except requests.exceptions.RequestException as err:
                self.log.error("Something else: {0}".format(err))
                if time.time() > end_time:
                    raise ServerUnavailableException(ip=self.ip)
            sleep(3, log_type="infra")

    def http_request(self, api, method='GET', params='', headers=None, timeout=300):
        if not headers:
            headers = self.create_headers()
        if CbServer.use_https:
            status, content, response = \
                self._urllib_request(api, method=method, params=params, headers=headers,
                                     timeout=timeout, verify=False)
            return status, content, response
        end_time = time.time() + timeout
        while True:
            try:
                response, content = httplib2.Http(timeout=timeout).request(
                    api, method, params, headers)
                if response.status in [200, 201, 202, 204]:
                    return True, content, response
                else:
                    try:
                        json_parsed = json.loads(content)
                    except ValueError:
                        json_parsed = dict()
                        json_parsed["error"] = "status: {0}, content: {1}" \
                            .format(response['status'], content)
                    reason = "unknown"
                    if "error" in json_parsed:
                        reason = json_parsed["error"]
                    if ("accesskey" in params.lower()) or ("secretaccesskey" in params.lower()) or (
                            "password" in params.lower()) or ("secretkey" in params.lower()):
                        message = '{0} {1} body: {2} headers: {3} ' \
                                  'error: {4} reason: {5} {6} {7}'. \
                            format(method, api, "Body is being redacted because it contains sensitive info", headers,
                                   response['status'], reason,
                                   content.rstrip('\n'),
                                   self.get_auth(headers))
                    else:
                        message = '{0} {1} body: {2} headers: {3} ' \
                                  'error: {4} reason: {5} {6} {7}'. \
                            format(method, api, params, headers,
                                   response['status'], reason,
                                   content.rstrip('\n'),
                                   self.get_auth(headers))
                    self.log.debug(message)
                    self.log.debug(''.join(traceback.format_stack()))
                    return False, content, response
            except socket.error as e:
                self.log.error("Socket error while connecting to {0}. "
                               "Error {1}".format(api, e))
                if time.time() > end_time:
                    raise ServerUnavailableException(ip=self.ip)
            except httplib2.ServerNotFoundError as e:
                self.log.error("ServerNotFoundError while connecting to {0}. "
                               "Error {1}".format(api, e))
                if time.time() > end_time:
                    raise ServerUnavailableException(ip=self.ip)
            sleep(3, log_type="infra")
