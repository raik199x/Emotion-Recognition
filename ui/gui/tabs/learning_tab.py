from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout
from PySide6.QtCore import QThreadPool
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.workers.learning_worker import LearningWorker

# import pyqtgraph


class LearningTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)

    # Worker connection (statistics)
    self.threadpool = QThreadPool()
    self.current_epoch = int()
    self.current_emotion = str
    self.full_dataset_iteration = int()
    self.update_after_num_epochs = 5000

    self.label_current_epoch = QLabel("None")
    self.label_current_emotion = QLabel("None")
    self.label_full_dataset_iteration = QLabel("None")

    self.stats_layout = QFormLayout()
    self.stats_layout.addRow(QLabel("Epoch num (from the start): "), self.label_current_epoch)
    self.stats_layout.addRow(QLabel("Emotion (last triggered): "), self.label_current_emotion)
    self.stats_layout.addRow(QLabel("Full dataset iterations num: "), self.label_full_dataset_iteration)
    self.main_vertical_layout.addLayout(self.stats_layout)

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

  def UserPressedStartButton(self) -> None:
    self.button_start_model_train.setEnabled(False)
    self.button_stop_model_train.setEnabled(True)
    self.ParentClass.is_model_learning = True

    # Resetting stats
    self.current_epoch = 0
    self.current_emotion = "Angry"
    self.full_dataset_iteration = 0

    worker = LearningWorker(self.ParentClass, self)
    self.threadpool.start(worker)

  def UserPressedStopButton(self) -> None:
    self.button_start_model_train.setEnabled(True)
    self.button_stop_model_train.setEnabled(False)
    self.ParentClass.is_model_learning = False
    self.threadpool.waitForDone()  # Waiting until model successfully saves itself

  def UserSelectedTab(self) -> None:
    if self.ParentClass.is_model_learning:
      return
    elif self.ParentClass.is_model_loaded:
      self.label_model_train_status.setText("Ready for training")
      self.button_start_model_train.setEnabled(True)
    else:
      self.label_model_train_status.setText("Model is not loaded. Check settings tab.")
      self.button_start_model_train.setEnabled(False)
      self.button_stop_model_train.setEnabled(False)
