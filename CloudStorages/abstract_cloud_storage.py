from shared import data_folder_path

import codes
import shutil


class AbstractCloudStorage(codes.ReturnCodes):
  def __init__(self):
    super().__init__()
    # Folder to search and save in cloud
    self.data_folder_name = data_folder_path[:-1]  # removing / on the end
    self.zipped_folder_name = self.data_folder_name + ".zip"

    # Vars
    self.cloud_storage_name = str()

    # Flags (only one of 2  must be set to true in child class)
    self.isAuthViaToken = False
    self.isAuthViaCredentials = False

  def checkDataFolderExistence(self) -> bool:
    raise NotImplementedError("checkProjectFolderExistence is not implemented for current class")

  def pushDataFolder(self) -> str:
    raise NotImplementedError("pushDataFolder is not implemented for current class")

  def pullDataFolder(self) -> str:
    raise NotImplementedError("pullDataFolder is not implemented for current class")

  def removeDataFolder(self) -> str:
    raise NotImplementedError("removeDataFolder is not implemented for current class")

  def loginViaCredentials(self, email: str, password: str) -> str:
    raise NotImplementedError("loginViaCredentials is not implemented for current class")

  def loginViaToken(self, token: str) -> str:
    raise NotImplementedError("loginViaToken is not implemented for current class")

  def zipFolder(self):
    shutil.make_archive(self.data_folder_name, format="zip", root_dir=".", base_dir=self.data_folder_name)

  def unzipFolder(self):
    shutil.unpack_archive(self.zipped_folder_name)
