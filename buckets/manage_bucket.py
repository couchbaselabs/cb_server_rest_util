from requests.utils import quote

from cb_server_rest_util.connection import CBRestConnection


class BucketManageAPI(CBRestConnection):
    def __init__(self):
        super(BucketManageAPI, self).__init__()

    def get_available_sample_buckets(self):
        """
        GET :: /sampleBuckets
        """
        api = f"{self.base_url}/sampleBuckets"
        status, content, _ = self.request(api)
        return status, content

    def load_sample_bucket(self, bucket_name_list):
        """
        POST :: /sampleBuckets/install
        """
        api = f"{self.base_url}/sampleBuckets/install"
        status, content, _ = self.request(api, self.POST,
                                          params=str(bucket_name_list))
        return status, content

    def create_bucket(self, bucket_params):
        """
        POST :: /pools/default/buckets
        https://docs.couchbase.com/server/current/rest-api/rest-bucket-create.html
        """
        api = f"{self.base_url}/pools/default/buckets"
        status, _, response = self.request(api, self.POST,
                                           params=bucket_params)
        return status, response

    def edit_bucket(self, bucket_name, bucket_params):
        """
        POST :: /pools/default/buckets/<bucket_name>
        https://docs.couchbase.com/server/current/rest-api/rest-bucket-create.html
        """

    def delete_bucket(self, bucket_name):
        """
        DELETE :: /pools/default/buckets/<bucket_name>
        https://docs.couchbase.com/server/current/rest-api/rest-bucket-delete.html
        """
        bucket_name = quote(bucket_name)
        api = self.base_url + f"/pools/default/buckets/{bucket_name}"
        status, content, _ = self.request(api, self.DELETE)
        return status, content

    def flush_bucket(self, bucket_name):

        """
        POST :: /pools/default/buckets/<bucket_name>/controller/doFlush
        """
        bucket_name = quote(bucket_name)
        api = self.base_url \
              + f"/pools/default/buckets/{bucket_name}/controller/doFlush"
        status, content, _ = self.request(api, self.POST)
        return status, content
