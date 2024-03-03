from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from ui.gui.tabs.abstract_tab import AbstractTabWidget
# import pyqtgraph


class LearningTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)

    # Head: status of model
    self.label_model_train_status = QLabel("Model is not loaded. Check settings tab.")

    self.button_start_model_train = QPushButton("Start training")
    self.button_start_model_train.setEnabled(False)
    self.button_start_model_train.clicked.connect(self.UserPressedStartButton)

    self.button_stop_model_train = QPushButton("Stop training")
    self.button_stop_model_train.setEnabled(False)
    self.button_stop_model_train.clicked.connect(self.UserPressedStopButton)

    buttons_start_stop_layout = QHBoxLayout()
    buttons_start_stop_layout.addWidget(self.button_start_model_train)
    buttons_start_stop_layout.addWidget(self.button_stop_model_train)

    self.main_vertical_layout.addWidget(self.label_model_train_status)
    self.main_vertical_layout.addLayout(buttons_start_stop_layout)

  def UserPressedStartButton(self):
    print("DEBUG CLICKED START BUTTON")
    self.button_start_model_train.setEnabled(False)
    self.button_stop_model_train.setEnabled(True)
    self.ParentClass.is_model_learning = True

  def UserPressedStopButton(self):
    pass

  def UserSelectedTab(self):
    if self.ParentClass.is_model_learning:
      return
    elif self.ParentClass.is_model_loaded:
      self.label_model_train_status.setText("Ready for training")
      self.button_start_model_train.setEnabled(True)
    else:
      self.label_model_train_status.setText("Model is not loaded. Check settings tab.")
      self.button_start_model_train.setEnabled(False)
      self.button_stop_model_train.setEnabled(False)
