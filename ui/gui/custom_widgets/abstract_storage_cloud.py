from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal, QObject
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from ui.gui.workers.storage_worker import StorageWorker, StorageWorkerTasks
from shared import icon_size, assets_folder_path


class AbstractStorageSignals(QObject):
  delete_widget = Signal(str, str)  # storage provider, Name of storage


class AbstractStorageWidget(QWidget):
  def __init__(self, ParentClass, storage_name: str, icon_path: str, storage_class):
    super().__init__()
    self.ParentClass = ParentClass
    self.signals = AbstractStorageSignals()
    self.storage_name = storage_name
    self.cloud_storage = storage_class

    # Statuses
    self.no_info = "Refresh required"
    self.folder_not_found = "Storage does not have emotion recognition data"
    self.folder_found = "Storage was found"

    main_layout = QVBoxLayout()
    self.setLayout(main_layout)
    self.setFixedHeight(110)

    container_widget = QFrame()
    container_widget.setStyleSheet("background-color: #272727; border-radius: 10px;")

    # Layouts
    container_layout = QVBoxLayout(container_widget)
    label_storage_name = QLabel(storage_name)
    label_storage_name.setAlignment(Qt.AlignCenter)
    label_storage_name.setStyleSheet("font-size: 16px; font-weight: solid;")
    container_layout.addWidget(label_storage_name)

    basic_info = QHBoxLayout()
    container_layout.addLayout(basic_info)

    cloud_storage_icon = QLabel()
    cloud_storage_icon.setPixmap(QPixmap(icon_path).scaled(icon_size))
    cloud_storage_icon.setAlignment(Qt.AlignCenter)

    overview_layout = QVBoxLayout()
    self.label_status = QLabel(self.no_info)
    self.label_status.setAlignment(Qt.AlignRight)

    buttons_layout = QHBoxLayout()  # start buttons layout

    button_refresh = DarkStyleButton("Refresh")
    button_refresh.clicked.connect(self.refreshPressed)

    button_pull = DarkStyleButton("Pull")
    button_pull.clicked.connect(self.pullPressed)

    button_push = DarkStyleButton("Push")
    button_push.clicked.connect(self.pushPressed)

    button_remove = DarkStyleButton("Remove")
    button_remove.setToolTip("Remove folder from cloud")
    button_remove.clicked.connect(self.removePressed)

    button_logout = DarkStyleButton("Logout")
    button_logout.clicked.connect(self.logoutPressed)

    buttons_layout.addWidget(button_refresh)
    buttons_layout.addWidget(button_pull)
    buttons_layout.addWidget(button_push)
    buttons_layout.addWidget(button_remove)
    buttons_layout.addWidget(button_logout)  # end buttons layout

    overview_layout.addWidget(self.label_status)
    overview_layout.addLayout(buttons_layout)

    self.current_status_icon = QLabel()
    self.current_status_icon.setPixmap(QPixmap(assets_folder_path + "information.png").scaled(icon_size))  #! IMPLEMENT
    self.current_status_icon.setAlignment(Qt.AlignCenter)

    basic_info.addWidget(cloud_storage_icon)
    basic_info.addLayout(overview_layout)
    basic_info.addWidget(self.current_status_icon)

    # Finalize
    main_layout.addWidget(container_widget)
    self.refreshPressed()

  def isStorageBusy(self):
    if self.ParentClass.is_storage_busy:
      QMessageBox.warning(self, "Warning", "Storage is currently busy")
      return True
    return False

  def removePressed(self):
    if self.isStorageBusy():
      return
    self.cloud_storage.removeDataFolder()
    self.refreshPressed()

  def pullPressed(self):
    if self.isStorageBusy():
      return
    worker = StorageWorker(self, StorageWorkerTasks().task_pull)
    self.ParentClass.threadpool.start(worker)

  def pushPressed(self):
    if self.isStorageBusy():
      return
    worker = StorageWorker(self, StorageWorkerTasks().task_push)
    self.ParentClass.threadpool.start(worker)

  def refreshPressed(self, force_check=False):
    if self.isStorageBusy() and not force_check:
      return
    result = self.cloud_storage.checkDataFolderExistence()
    self.label_status.setText(self.folder_found if result else self.folder_not_found)

  def logoutPressed(self):
    if self.isStorageBusy():
      return
    self.signals.delete_widget.emit(self.cloud_storage.cloud_storage_name, self.storage_name)
