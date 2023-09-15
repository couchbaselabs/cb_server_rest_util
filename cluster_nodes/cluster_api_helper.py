from Cb_constants import CbServer, constants
from testconstants import IS_CONTAINER


class MembaseServerVersion:
    def __init__(self, implementationVersion='', componentsVersion=''):
        self.implementationVersion = implementationVersion
        self.componentsVersion = componentsVersion


# this class will also contain more node related info
class OtpNode(object):
    def __init__(self, id='', status=''):
        self.id = id
        self.ip = ''
        self.replication = ''
        self.port = constants.port
        self.gracefulFailoverPossible = 'true'
        # extract ns ip from the otpNode string
        # its normally ns_1@10.20.30.40
        if id.find('@') >= 0:
            self.ip = id[id.index('@') + 1:]
            if self.ip.count(':') > 0:
                # raw ipv6? enclose in square brackets
                self.ip = '[' + self.ip + ']'
        self.status = status


class NodeInfo(object):
    def __init__(self):
        self.availableStorage = None  # list
        self.memoryQuota = None


class NodeDataStorage(object):
    def __init__(self):
        self.type = ''  # hdd or ssd
        self.path = ''
        self.index_path = ''
        self.cbas_path = ''
        self.data_path = ''
        self.quotaMb = ''
        self.state = ''  # ok

    def __str__(self):
        return '{0}'.format({'type': self.type,
                             'path': self.path,
                             'index_path': self.index_path,
                             'quotaMb': self.quotaMb,
                             'state': self.state})

    def get_data_path(self):
        return self.path

    def get_index_path(self):
        return self.index_path


class NodeDiskStorage(object):
    def __init__(self):
        self.type = 0
        self.path = ''
        self.sizeKBytes = 0
        self.usagePercent = 0


class Node(object):
    def __init__(self):
        self.uptime = 0
        self.memoryTotal = 0
        self.memoryFree = 0
        self.mcdMemoryReserved = 0
        self.mcdMemoryAllocated = 0
        self.status = ""
        self.hostname = ""
        self.clusterCompatibility = ""
        self.clusterMembership = ""
        self.version = ""
        self.os = ""
        self.ports = []
        self.availableStorage = []
        self.storage = []
        self.memoryQuota = 0
        self.memcached = constants.memcached_port
        self.id = ""
        self.ip = ""
        self.rest_username = ""
        self.rest_password = ""
        self.port = constants.port
        self.services = []
        self.storageTotalRam = 0
        self.server_group = ""
        self.limits = None
        self.utilization = None
        self.cpuCount = 0

    def __str__(self):
        ip_str = "ip:{0} port:{1}".format(self.ip, self.port)
        return ip_str

    def __repr__(self):
        ip_str = "ip:{0} port:{1}".format(self.ip, self.port)
        return ip_str


class AutoFailoverSettings(object):
    def __init__(self):
        self.enabled = True
        self.timeout = 0
        self.count = 0
        self.failoverOnDataDiskIssuesEnabled = False
        self.failoverOnDataDiskIssuesTimeout = 0
        self.maxCount = 1
        self.failoverServerGroup = False


class AutoReprovisionSettings(object):
    def __init__(self):
        self.enabled = True
        self.max_nodes = 0
        self.count = 0


class RestParser(object):
    def __init__(self, server_type="dedicated"):
        self.server_type = server_type

    def parse_index_status_response(self, parsed):
        index_map = dict()
        for index_map in parsed["indexes"]:
            bucket_name = index_map['bucket'].encode('ascii', 'ignore')
            if bucket_name not in index_map.keys():
                index_map[bucket_name] = {}
            index_name = index_map['index'].encode('ascii', 'ignore')
            index_map[bucket_name][index_name] = {}
            index_map[bucket_name][index_name]['status'] = \
                index_map['status'].encode('ascii', 'ignore')
            index_map[bucket_name][index_name]['progress'] = \
                str(index_map['progress']).encode('ascii', 'ignore')
            index_map[bucket_name][index_name]['definition'] = \
                index_map['definition'].encode('ascii', 'ignore')
            index_map[bucket_name][index_name]['hosts'] = \
                index_map['hosts'][0].encode('ascii', 'ignore')
            index_map[bucket_name][index_name]['id'] = index_map['id']
        return index_map

    def parse_get_nodes_response(self, parsed):
        node = Node()
        node.uptime = parsed['uptime']
        node.memoryFree = parsed['memoryFree']
        node.memoryTotal = parsed['memoryTotal']
        node.mcdMemoryAllocated = parsed['mcdMemoryAllocated']
        node.mcdMemoryReserved = parsed['mcdMemoryReserved']
        node.cpuCount = parsed["cpuCount"]

        if CbServer.Settings.INDEX_MEM_QUOTA in parsed:
            node.indexMemoryQuota = parsed[CbServer.Settings.INDEX_MEM_QUOTA]
        if CbServer.Settings.FTS_MEM_QUOTA in parsed:
            node.ftsMemoryQuota = parsed[CbServer.Settings.FTS_MEM_QUOTA]
        if CbServer.Settings.CBAS_MEM_QUOTA in parsed:
            node.cbasMemoryQuota = parsed[CbServer.Settings.CBAS_MEM_QUOTA]
        if CbServer.Settings.EVENTING_MEM_QUOTA in parsed:
            node.eventingMemoryQuota = parsed[CbServer.Settings.EVENTING_MEM_QUOTA]

        node.status = parsed['status']
        node.hostname = parsed['hostname']
        node.clusterCompatibility = parsed['clusterCompatibility']
        node.clusterMembership = parsed['clusterMembership']
        node.version = parsed['version']
        node.curr_items = 0
        if 'interestingStats' in parsed \
                and 'curr_items' in parsed['interestingStats']:
            node.curr_items = parsed['interestingStats']['curr_items']
        node.port = parsed["hostname"][parsed["hostname"].rfind(":") + 1:]
        node.os = parsed['os']

        if "serverGroup" in parsed:
            node.server_group = parsed["serverGroup"]
        if "services" in parsed:
            node.services = parsed["services"]
        if "otpNode" in parsed:
            node.id = parsed["otpNode"]
        if "hostname" in parsed:
            # should work for both: ipv4 and ipv6
            node.ip, node.port = parsed["hostname"].rsplit(":", 1)
            if CbServer.use_https and self.server_type != "serverless" \
                    and self.server_type != "nebula":
                node.port = int(node.port) + 10000

        # memoryQuota
        if CbServer.Settings.KV_MEM_QUOTA in parsed:
            node.memoryQuota = parsed[CbServer.Settings.KV_MEM_QUOTA]
        if 'availableStorage' in parsed:
            available_storage = parsed['availableStorage']
            for key in available_storage:
                # let's assume there is only one disk in each node
                storage_list = available_storage[key]
                for dict_parsed in storage_list:
                    if 'path' in dict_parsed and 'sizeKBytes' in dict_parsed \
                            and 'usagePercent' in dict_parsed:
                        disk_storage = NodeDiskStorage()
                        disk_storage.path = dict_parsed['path']
                        disk_storage.sizeKBytes = dict_parsed['sizeKBytes']
                        disk_storage.type = key
                        disk_storage.usagePercent = dict_parsed['usagePercent']
                        node.availableStorage.append(disk_storage)

        if 'storage' in parsed:
            storage = parsed['storage']
            for key in storage:
                disk_storage_list = storage[key]
                for dict_parsed in disk_storage_list:
                    if 'path' in dict_parsed and 'state' in dict_parsed \
                            and 'quotaMb' in dict_parsed:
                        data_storage = NodeDataStorage()
                        data_storage.path = dict_parsed['path']
                        data_storage.index_path = dict_parsed.get('index_path',
                                                                  '')
                        data_storage.quotaMb = dict_parsed['quotaMb']
                        data_storage.state = dict_parsed['state']
                        data_storage.type = key
                        node.storage.append(data_storage)

        # Format: ports={"proxy":11211,"direct":11210}
        if "ports" in parsed:
            ports = parsed["ports"]
            if "direct" in ports:
                node.memcached = ports["direct"]

        if "storageTotals" in parsed:
            storage_totals = parsed["storageTotals"]
            if storage_totals.get("hdd"):
                if storage_totals["hdd"].get("total"):
                    hdd_bytes = storage_totals["hdd"]["total"]
                    node.storageTotalDisk = hdd_bytes / (1024 * 1024)
                if storage_totals["hdd"].get("used"):
                    hdd_bytes = storage_totals["hdd"]["used"]
                    node.storageUsedDisk = hdd_bytes / (1024 * 1024)

            if storage_totals.get("ram"):
                if storage_totals["ram"].get("total"):
                    ram_kb = storage_totals["ram"]["total"]
                    node.storageTotalRam = ram_kb / (1024 * 1024)

                    if IS_CONTAINER:
                        # the storage total values are more accurate than
                        # mcdMemoryReserved - which is container host memory
                        node.mcdMemoryReserved = node.storageTotalRam * 0.70

        # Serverless specific stat
        if "limits" in parsed:
            node.limits = dict()
            node.utilization = dict()
            for service in node.services:
                node.limits[service] = dict()
                node.utilization[service] = dict()

                if service == CbServer.Services.KV:
                    limits = parsed["limits"][service]
                    utilised = parsed["utilization"][service]
                    for field in ["buckets", "memory", "weight"]:
                        node.limits[service][field] = limits[field]
                        node.utilization[service][field] = utilised[field]

        return node
