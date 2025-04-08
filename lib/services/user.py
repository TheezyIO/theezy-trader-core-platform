from lib.common import constants
from lib.services import service


class UserService(service.Service):

    def create_user(self, user_request):
        return self.post(constants.urls.user, user_request)

    def delete_user(self, user_id):
        return self.delete()
