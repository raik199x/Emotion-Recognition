from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PySide6.QtCore import QThreadPool
from ui.gui.tabs.learning_tab import LearningTab
from ui.gui.tabs.settings_tab import SettingsTab
from ui.gui.tabs.camera_tab import CameraTab
from ui.gui.tabs.storage_tab import StorageTab
from DeepLearning.model import EmotionClassificationModel
from DeepLearning.settings import pytorch_device
from ImageProcessing.face_detection import FaceDetector
from shared import pretrained_face_detector
from DeepLearning.dataset_parser import DatasetParser
from shared import dataset_folder_path


class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    # Ui part
    self.setWindowTitle("Emotion classification app @raik199x")
    self.setStyleSheet("background-color: #303030; color: white")

    self.mainTabWidget = QTabWidget(self)
    self.mainTabWidget.currentChanged.connect(self.TabChanged)
    self.setMinimumWidth(500)
    self.setCentralWidget(self.mainTabWidget)

    # Pytorch part (must be loaded before tabs)
    self.emotion_classification_model = EmotionClassificationModel()
    self.emotion_classification_model.to(pytorch_device)

    # flags
    self.is_model_loaded = False  # Shows if model file was selected
    self.is_storage_busy = False  # Forbids using commands in storage tab
    self.is_model_learning = False  # Forbids changing model settings

    self.FaceDetector = FaceDetector(pretrained_face_detector, 0)  # dlib face detector
    self.parser = self.reloadParser()  # dataset parser
    self.threadpool = QThreadPool()  # Configurable threads

    # Tabs
    self.list_of_tabs = [
      SettingsTab(self, "Settings"),
      StorageTab(self, "Storages"),
      LearningTab(self, "Learning"),
      CameraTab(self, "Camera"),
    ]

    for index, _ in enumerate(self.list_of_tabs):
      if self.list_of_tabs[index].tab_name == "Camera":
        self.camera_tab_index = index
        break
    # moved to another for since triggers changedTab signals and throws error of missing var
    for tab in self.list_of_tabs:
      self.mainTabWidget.addTab(tab, tab.tab_name)

  def TabChanged(self, index):
    if self.list_of_tabs[index].tab_name != "Camera":
      if self.list_of_tabs[self.camera_tab_index].capture.isOpened():
        self.list_of_tabs[self.camera_tab_index].capture.release()

    self.list_of_tabs[index].UserSelectedTab()

  def reloadParser(self) -> DatasetParser:
    return DatasetParser(dataset_folder_path)


def ShowWindow():
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()
