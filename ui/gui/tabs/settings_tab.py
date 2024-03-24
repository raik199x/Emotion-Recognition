from PySide6.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import QThreadPool
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from torch import __version__ as pytorch_version
from DeepLearning.settings import pytorch_device
from shared import pretrained_emotion_recognition_model, GetRelativePath

import os

PretrainedModelRelativePath = GetRelativePath(pretrained_emotion_recognition_model)


class SettingsTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)
    self.threadpool = QThreadPool()  # Just for stats

    self.label_model_load_status = QLabel()

    # Checking default model path
    self.SetLoadModelStatus(False)
    if os.path.exists(PretrainedModelRelativePath):
      self.ParentClass.emotion_classification_model.LoadModel(PretrainedModelRelativePath)
      self.SetLoadModelStatus(True)

    self.button_set_model_path = DarkStyleButton("Load pretrained model")
    self.button_set_model_path.clicked.connect(self.OnLoadModelButtonClicked)
    self.button_create_new_model = DarkStyleButton("Create new model")
    self.button_create_new_model.clicked.connect(self.OnCreateModelButtonClicked)

    layout_model_statue = QHBoxLayout()
    layout_model_statue.addWidget(self.label_model_load_status)
    layout_model_statue.addWidget(self.button_set_model_path)
    layout_model_statue.addWidget(self.button_create_new_model)
    self.main_vertical_layout.addLayout(layout_model_statue)

    # outputting info
    self.textBrowser_current_run_info = QTextBrowser()
    self.textBrowser_current_run_info.setText(
      "Pytorch version:\t"
      + pytorch_version
      + "\n"
      + "Model is running on:\t"
      + pytorch_device
      + "\n"
      + "Maximum threads:\t"
      + str(self.threadpool.maxThreadCount())
    )
    self.main_vertical_layout.addWidget(self.textBrowser_current_run_info)

  def OnLoadModelButtonClicked(self) -> None:
    if self.ParentClass.is_model_learning:
      QMessageBox.warning(self, "Model is busy learning now")
      return

    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(self, "Select pretrained model file")

    if len(file_path) == 0:  # User closed file dialog, operation canceled
      return

    if not os.path.exists(file_path):  # Operation canceled
      QMessageBox.warning(self, "Selected path cannot be found")
      return

    self.SetLoadModelStatus(False)  # Unloading model, so if any error occurs it wont be usable
    self.ParentClass.emotion_classification_model.LoadModel(file_path)  # Trying to load model
    self.SetLoadModelStatus(True)  # If success, function will continue and this command will run

  def OnCreateModelButtonClicked(self) -> None:
    if os.path.exists(PretrainedModelRelativePath):
      result = QMessageBox.question(
        self,
        "Confirmation",
        "One copy of model is already exists, are you sure you want to delete previous and create new?\nOperation cannot be undone",
        QMessageBox.Yes | QMessageBox.No,
      )

      if result == QMessageBox.No:  # Operation canceled
        return
      os.remove(PretrainedModelRelativePath)

    self.ParentClass.emotion_classification_model.BackupModel("", PretrainedModelRelativePath)
    self.ParentClass.emotion_classification_model.LoadModel(PretrainedModelRelativePath)
    self.SetLoadModelStatus(True)

  def SetLoadModelStatus(self, status: bool) -> None:
    if status:
      self.label_model_load_status.setText("Model is loaded")
      self.label_model_load_status.setStyleSheet("color: green")
      self.ParentClass.is_model_loaded = True
    else:
      self.label_model_load_status.setText("Model is not loaded")
      self.label_model_load_status.setStyleSheet("color: yellow")
      self.ParentClass.is_model_loaded = False

  def UserSelectedTab(self) -> None:
    pass
