import configparser
import os
import codes


class ProjectConfig(codes.ReturnCodes):
  def __init__(self):
    super().__init__()
    self.config = configparser.ConfigParser()
    self.config_name = ".project_config.ini"

    if os.path.exists(self.config_name):
      self.config.read(self.config_name)

  def saveConfig(self):
    with open(self.config_name, "w") as config_file:
      self.config.write(config_file)

  def addStorageEntry(self, cloud_provider_name: str, storage_name: str, key_value_pairs: dict) -> str:
    section_name = "storage." + cloud_provider_name + "." + storage_name

    isExist = True
    try:
      self.config[section_name]
    except KeyError:
      isExist = False
    if isExist:
      return self.storage_exist_code

    # iterating through data
    self.config[section_name] = {}
    for item in key_value_pairs.items():
      self.config[section_name][item[0]] = item[1]

    self.saveConfig()
    return self.success_code
