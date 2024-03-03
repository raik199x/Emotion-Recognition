from PySide6.QtWidgets import QWidget


class AbstractTabWidget(QWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__()
    self.ParentClass = ParentClass
    self.tab_name = tab_name

  def UserSelectedTab(self):
    raise NotImplementedError("Please Implement this method")
