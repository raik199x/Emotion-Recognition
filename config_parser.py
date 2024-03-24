import configparser
import os


class ProjectConfig:
  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config_name = ".project_config.ini"
    # Codes
    self.success_code = "success"
    self.already_exist_code = "storage name already exists"

    if os.path.exists(self.config_name):
      self.config.read(self.config_name)

  def saveConfig(self):
    with open(self.config_name, "w") as config_file:
      self.config.write(config_file)

  def addMegaStorage(self, storage_name: str, email: str, password: str) -> str:
    if self.config.has_option("mega." + storage_name, "email"):
      return self.already_exist_code

    self.config["mega." + storage_name] = {"email": email, "password": password}
    self.saveConfig()

    return self.success_code
