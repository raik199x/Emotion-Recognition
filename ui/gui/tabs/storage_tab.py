from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.custom_widgets.abstract_storage_cloud import AbstractStorageWidget
from PySide6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from shared import assets_folder_path
from CloudStorages.mega import MegaCloud


class StorageTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    scroll_area = QScrollArea()
    main_layout.addWidget(scroll_area)
    scroll_area.setWidgetResizable(True)

    content_widget = QWidget()
    scroll_area.setWidget(content_widget)

    self.content_layout = QVBoxLayout(content_widget)

    self.status_label = QLabel()
    self.status_label.setText("Nothing to do now")
    self.status_label.setAlignment(Qt.AlignCenter)
    self.status_label.setStyleSheet("font-size: 16px; font-weight: bold")

    self.content_layout.addWidget(self.status_label)
    self.content_layout.addWidget(AbstractStorageWidget(assets_folder_path + "mega-icon-logo.png", MegaCloud()))
    verticalSpacer = QSpacerItem(1, self.height(), QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.content_layout.addSpacerItem(verticalSpacer)

  def UserSelectedTab(self) -> None:
    pass