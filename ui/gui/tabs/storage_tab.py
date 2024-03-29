from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.custom_widgets.abstract_storage_cloud import AbstractStorageWidget
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from ui.gui.custom_widgets.add_storage_dialog import AddStorageDialog
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtCore import Slot
from shared import assets_folder_path
from CloudStorages.cloud_storage_interface import CloudStorageInterface
from config_parser import ProjectConfig


class StorageTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)

    # Decided to put it here, since those assets really needed only here
    self.assets_dict = {CloudStorageInterface().mega_cloud_name: "mega-icon-logo.png"}

    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    scroll_area = QScrollArea()
    main_layout.addWidget(scroll_area)
    scroll_area.setWidgetResizable(True)

    content_widget = QWidget()
    scroll_area.setWidget(content_widget)

    self.content_layout = QVBoxLayout(content_widget)

    upper_layout = QHBoxLayout()  # start of upper_layout

    self.button_add_storage = DarkStyleButton("Add storage")
    self.button_add_storage.clicked.connect(self.addStoragePressed)

    self.button_refresh_storage = DarkStyleButton("Refresh storages")
    self.button_refresh_storage.clicked.connect(self.refreshStorages)

    upper_layout.addWidget(self.button_add_storage)
    upper_layout.addWidget(self.button_refresh_storage)
    self.content_layout.addLayout(upper_layout)  # end of upper_layout

    self.storage_widgets_layout = QVBoxLayout()  # This layout will store all storage widgets
    self.content_layout.addLayout(self.storage_widgets_layout)
    self.refreshStorages()
    verticalSpacer = QSpacerItem(1, self.height(), QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.content_layout.addSpacerItem(verticalSpacer)

  def clearLayout(self, layout):
    while layout.count():
      item = layout.takeAt(0)
      widget = item.widget()
      if widget is not None:
        widget.deleteLater()

  def addCloudWidget(self, cloud_class, storage_name: str):
    path_to_icon = assets_folder_path + self.assets_dict[cloud_class.cloud_storage_name]
    cloud_widget = AbstractStorageWidget(self.ParentClass, storage_name, path_to_icon, cloud_class)
    cloud_widget.signals.delete_widget.connect(self.removeStorage)
    self.storage_widgets_layout.addWidget(cloud_widget)

  def refreshStorages(self):
    self.clearLayout(self.storage_widgets_layout)
    # Getting storages
    config = ProjectConfig()
    entrees = config.getStorageEntrees()
    for entry in entrees:
      self.addCloudWidget(entry[0], entry[1])

  @Slot()
  def removeStorage(self, provider_name: str, storage_name: str):
    config = ProjectConfig()
    config.deleteStorageEntry(provider_name, storage_name)
    self.refreshStorages()

  def addStoragePressed(self) -> None:
    window = AddStorageDialog()
    window.exec()
    if window.return_instance is not None:
      self.addCloudWidget(window.return_instance, window.return_storage_name)

  def UserSelectedTab(self) -> None:
    pass
