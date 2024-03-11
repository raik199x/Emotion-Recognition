from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from ui.gui.tabs.learning_tab import LearningTab
from ui.gui.tabs.settings_tab import SettingsTab
from ui.gui.tabs.camera_tab import CameraTab
from DeepLearning.model import EmotionClassificationModel
from DeepLearning.settings import pytorch_device


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

    # shared variables between windows
    self.is_model_loaded = False  # Shows if model file was selected
    self.is_model_learning = False  # Forbids changing model settings

    # Tabs
    self.list_of_tabs = [SettingsTab(self, "Settings"), LearningTab(self, "Learning"), CameraTab(self, "Camera")]
    for tab in self.list_of_tabs:
      self.mainTabWidget.addTab(tab, tab.tab_name)

  def TabChanged(self, index):
    self.list_of_tabs[index].UserSelectedTab()


def ShowWindow():
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()
