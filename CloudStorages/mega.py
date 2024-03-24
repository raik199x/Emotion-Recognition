import mega
from CloudStorages.abstract_cloud_storage import AbstractCloudStorage


class MegaCloud(AbstractCloudStorage):
  def __init__(self):
    super().__init__()
    self.mega = mega.Mega()
    self.account = None
    self.isAuthViaCredentials = True

  def loginViaToken(self, token) -> str:
    return self.not_supported_code

  def loginViaCredentials(self, email: str, password: str) -> str:
    try:
      self.account = self.mega.login(email, password)
    except Exception as error_message:
      return error_message

    return self.success_code

  def checkDataFolderExistence(self) -> str:
    file = self.account.find(self.data_folder_name)
    return True if len(file) != 0 else False

  def GetAccountInfo(self) -> dict():
    quota = self.account.get_quota()
    space = self.account.get_storage_space(giga=True)
    return {"quota": quota, "space": space}
