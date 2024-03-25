import mega
import os
from CloudStorages.abstract_cloud_storage import AbstractCloudStorage


class MegaCloud(AbstractCloudStorage):
  def __init__(self):
    super().__init__()
    self.mega = mega.Mega()
    self.account = None

    # Setting up vars
    self.isAuthViaCredentials = True
    self.cloud_storage_name = "Mega"

  def loginViaToken(self, token) -> str:
    return self.not_supported_code

  def loginViaCredentials(self, email: str, password: str) -> str:
    try:
      self.account = self.mega.login(email, password)
    except Exception as error_message:
      return error_message

    return self.success_code

  def removeDataFolder(self) -> str:
    archive = self.account.find(self.zipped_folder_name)
    if not archive:
      return self.folder_not_found

    self.account.delete(archive[0])
    return self.success_code

  def pushDataFolder(self) -> str:
    if self.checkDataFolderExistence():
      return self.folder_exist
    self.zipFolder()
    self.account.upload(self.zipped_folder_name)
    os.remove(self.zipped_folder_name)
    return self.success_code

  def pullDataFolder(self) -> str:
    if os.path.exists(self.data_folder_name):
      return self.folder_exist
    archive = self.account.find(self.zipped_folder_name)
    if not archive:
      return self.folder_not_found
    self.account.download(archive)
    self.unzipFolder()
    os.remove(self.zipped_folder_name)

  def checkDataFolderExistence(self) -> str:
    file = self.account.find(self.zipped_folder_name)
    return True if file is not None else False

  # def GetAccountInfo(self) -> dict():
  #   quota = self.account.get_quota()
  #   space = self.account.get_storage_space(giga=True)
  #   return {"quota": quota, "space": space}
