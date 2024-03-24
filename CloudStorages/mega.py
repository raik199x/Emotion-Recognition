import mega

class MegaCloud:
  def __init__(self):
    self.mega = mega.Mega()
    self.account = None

  def LoginToAccount(self, email: str, password: str) -> str:
    try:
      self.account = self.mega.login(email, password)
    except Exception as e:
      return e

    return "success"

  def GetAccountInfo(self) -> dict():
    quota = self.account.get_quota()
    space = self.account.get_storage_space(giga=True)
    return {"quota": quota, "space": space}

  def GetFiles(self):
    files = self.account.get_files()
    return files

