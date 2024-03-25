import configparser
import os
import codes
from CloudStorages.cloud_storage_interface import CloudStorageInterface


class ProjectConfig(codes.ReturnCodes):
  def __init__(self):
    super().__init__()
    self.config = configparser.ConfigParser()
    self.config_name = ".project_config.ini"

    if os.path.exists(self.config_name):
      self.config.read(self.config_name)

    self.delimiter = "."
    self.storage_index = "storage"

  def saveConfig(self):
    with open(self.config_name, "w") as config_file:
      self.config.write(config_file)

  def deleteStorageEntry(self, provider_name: str, storage_name: str):
    section_name = self.storage_index + self.delimiter + provider_name + self.delimiter + storage_name
    self.config.remove_section(section_name)
    self.saveConfig()

  def addStorageEntry(self, provider_name: str, storage_name: str, key_value_pairs: dict) -> str:
    section_name = self.storage_index + self.delimiter + provider_name + self.delimiter + storage_name

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

  def getStorageEntrees(self) -> list[list]:
    result_list = list()
    cloud_interface = CloudStorageInterface()

    for each_section in self.config.sections():
      # Checking if entry is a storage type
      splitted_section_name = each_section.split(self.delimiter)
      if not splitted_section_name[0] == self.storage_index:
        continue

      cloud_instance = cloud_interface.getStorageInstance(splitted_section_name[1])
      if cloud_instance == cloud_interface.unknown_code:
        continue

      if cloud_instance.isAuthViaCredentials:
        result = cloud_instance.loginViaCredentials(
          self.config[each_section]["email"], self.config[each_section]["password"]
        )
      elif cloud_instance.isAuthViaToken:
        result = cloud_instance.loginViaToken(each_section["token"])

      if result == cloud_instance.success_code:
        result_list.append([cloud_instance, splitted_section_name[2]])

    return result_list
