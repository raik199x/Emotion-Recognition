from shared import data_folder_path


class AbstractCloudStorage:
  def __init__(self):
    self.success_code = "success"
    self.not_supported_code = "not_supported"
    self.data_folder_name = data_folder_path[:-1]  # removing / on the end

  def checkDataFolderExistence(self) -> bool:
    raise NotImplementedError("checkProjectFolderExistence is not implemented for current class")

  def pushDataFolder(self) -> str:
    raise NotImplementedError("pushDataFolder is not implemented for current class")

  def pullDataFolder(self) -> str:
    raise NotImplementedError("pullDataFolder is not implemented for current class")

  def syncDataFolder(self) -> str:
    raise NotImplementedError("syncDataFolder is not implemented for current class")

  def loginViaCredentials(self, email: str, password: str) -> str:
    raise NotImplementedError("loginViaCredentials is not implemented for current class")

  def loginViaToken(self, token: str) -> str:
    raise NotImplementedError("loginViaToken is not implemented for current class")
