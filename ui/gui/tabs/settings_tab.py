from PySide6.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import QThreadPool
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from torch import __version__ as pytorch_version
from DeepLearning.settings import pytorch_device
from shared import pretrained_emotion_recognition_model, dataset_folder_path, data_folder_path

import os
import shutil


class SettingsTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)
    self.threadpool = QThreadPool()  # Just for stats

    self.label_model_load_status = QLabel()

    # Checking default model path
    self.SetLoadModelStatus(False)
    if os.path.exists(pretrained_emotion_recognition_model):
      self.ParentClass.emotion_classification_model.LoadModel(pretrained_emotion_recognition_model)
      self.SetLoadModelStatus(True)

    self.button_set_model_path = DarkStyleButton("Load pretrained model")
    self.button_set_model_path.clicked.connect(self.OnLoadModelButtonClicked)
    self.button_create_new_model = DarkStyleButton("Create new model")
    self.button_create_new_model.clicked.connect(self.OnCreateModelButtonClicked)

    layout_model_status = QHBoxLayout()
    layout_model_status.addWidget(self.label_model_load_status)
    layout_model_status.addWidget(self.button_set_model_path)
    layout_model_status.addWidget(self.button_create_new_model)
    self.main_vertical_layout.addLayout(layout_model_status)

    layout_parser_status = QHBoxLayout()  # start of layout_parser_status

    self.label_parser_status = QLabel()
    self.button_load_parser = DarkStyleButton("Load dataset")
    self.button_load_parser.clicked.connect(self.loadDatasetPressed)
    self.button_unload_parser = DarkStyleButton("Unload dataset")
    self.button_unload_parser.clicked.connect(self.unloadDatasetPressed)
    self.SetLoadParserStatus()

    layout_parser_status.addWidget(self.label_parser_status)
    layout_parser_status.addWidget(self.button_load_parser)
    layout_parser_status.addWidget(self.button_unload_parser)
    self.main_vertical_layout.addLayout(layout_parser_status)  # end of layout_parser_status

    layout_data_folder_status = QHBoxLayout()  # start of layout_data_folder_status
    layout_data_folder_status.addWidget(QLabel("Local folder options"))

    button_delete_local_folder = DarkStyleButton("Delete local folder")
    button_delete_local_folder.clicked.connect(self.deleteLocalDataFolderPressed)
    layout_data_folder_status.addWidget(button_delete_local_folder)

    button_create_local_folder = DarkStyleButton("Create empty local folder")
    button_create_local_folder.clicked.connect(self.createLocalDataFolderPressed)
    layout_data_folder_status.addWidget(button_create_local_folder)
    self.main_vertical_layout.addLayout(layout_data_folder_status)  # end of layout_data_folder_status

    # outputting info
    self.textBrowser_current_run_info = QTextBrowser()
    self.textBrowser_current_run_info.setText(
      "Pytorch version:\t"
      + pytorch_version
      + "\n"
      + "Model is running on:\t"
      + pytorch_device
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
    if os.path.exists(pretrained_emotion_recognition_model):
      result = QMessageBox.question(
        self,
        "Confirmation",
        "One copy of model is already exists, are you sure you want to delete previous and create new?\nOperation cannot be undone",
        QMessageBox.Yes | QMessageBox.No,
      )

      if result == QMessageBox.No:  # Operation canceled
        return
      os.remove(pretrained_emotion_recognition_model)

    self.ParentClass.emotion_classification_model.BackupModel("", pretrained_emotion_recognition_model)
    self.ParentClass.emotion_classification_model.LoadModel(pretrained_emotion_recognition_model)
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

  def SetLoadParserStatus(self) -> None:
    if self.ParentClass.parser.isParserLoaded:
      self.label_parser_status.setText("Parser is loaded")
      self.label_parser_status.setStyleSheet("color: green")
      self.button_load_parser.setEnabled(False)
      self.button_unload_parser.setEnabled(True)
    else:
      self.label_parser_status.setText("Parser is unloaded")
      self.label_parser_status.setStyleSheet("color: yellow")
      self.button_load_parser.setEnabled(True)
      self.button_unload_parser.setEnabled(False)

  def loadDatasetPressed(self) -> None:
    if not os.path.exists(dataset_folder_path):
      QMessageBox.warning(self, "warning", f"Cannot load since dataset folder cannot be found {dataset_folder_path}")
      return
    self.ParentClass.parser.LoadDatasetIntoRam()
    self.SetLoadParserStatus()

  def unloadDatasetPressed(self) -> None:
    self.ParentClass.parser = self.ParentClass.reloadParser()
    self.SetLoadParserStatus()

  def deleteLocalDataFolderPressed(self) -> None:
    if not os.path.exists(data_folder_path):
      QMessageBox.info(self, "Fail", "Folder is not exist")
      return
    if self.ParentClass.is_model_learning:
      QMessageBox.warning(self, "Fail", "Cannot delete local folder while model is learning")
      return
    result = QMessageBox.question(
      self,
      "Last change",
      "Do you really want to delete local folder?\nThis operation cannot be undone.\nMake sure that you have backups",
      QMessageBox.Yes | QMessageBox.No,
    )
    if result == QMessageBox.No:  # Operation canceled
      return
    self.ParentClass.parser = self.ParentClass.reloadParser()
    self.SetLoadParserStatus()
    shutil.rmtree(data_folder_path)

  def createLocalDataFolderPressed(self) -> None:
    if os.path.exists(data_folder_path):
      QMessageBox.warning(self, "warning", "Local folder already exists")
      return
    os.mkdir(data_folder_path)

  def UserSelectedTab(self) -> None:
    pass
