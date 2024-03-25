from CloudStorages.mega import MegaCloud

import codes


class CloudStorageInterface(codes.ReturnCodes):
  def __init__(self):
    super().__init__()
    self.mega_cloud_name = MegaCloud().cloud_storage_name
    # self.yandex_cloud_name = "Yandex disk" # (dropped support of yandex disk due to lack of time)
    self.list_supported_cloud = [self.mega_cloud_name]

  def checkAuthFields(self, cloud_class, email: str, password: str, token: str) -> str:
    return_result = str()
    if cloud_class.isAuthViaCredentials:
      return_result = return_result + "Empty email field\n" if len(email) == 0 else ""
      return_result = return_result + "Empty password field\n" if len(password) == 0 else ""
      return_result = (
        return_result + "Ambiguous email format, multiple @\n"
        if email.count("@") != 1 and email.count("@") != 0
        else ""
      )
      return_result = return_result + "Ambiguous email format, no @ symbol\n" if email.find("@") == -1 else ""
    if cloud_class.isAuthViaToken:
      return_result = return_result + "Empty token\n" if len(token) == 0 else ""

    if len(return_result) == 0:
      return_result = "success"

    return return_result

  def tryLogin(self, cloud_class, email: str, password: str, token: str) -> str:
    if cloud_class.isAuthViaCredentials:
      return cloud_class.loginViaCredentials(email, password)
    if cloud_class.isAuthViaToken:
      return cloud_class.loginViaToken(token)

  def getAuthFields(self, cloud_class, email: str, password: str, token: str) -> dict:
    if cloud_class.isAuthViaCredentials:
      return {"email": email, "password": password}
    if cloud_class.isAuthViaToken:
      return {"token": token}
    return self.fail_code

  def getStorageInstance(self, cloud_provider: str):
    if cloud_provider == self.mega_cloud_name:
      return MegaCloud()
    return self.unknown_code
