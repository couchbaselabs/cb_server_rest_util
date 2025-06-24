from cb_server_rest_util.connection import CBRestConnection

class FusionFunctions(CBRestConnection):
    def __init__(self):
        super(FusionFunctions).__init__()

    def get_active_guest_volumes(self):
        """
        GET :: /fusion/activeGuestVolumes
        """
        api = self.base_url + "/fusion/activeGuestVolumes"
        status, content, _ = self.request(api)
        return status, content