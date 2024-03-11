from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout
from PySide6.QtCore import QThreadPool, Slot, Qt
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.workers.learning_worker import LearningWorker
from DeepLearning.dataset_parser import DatasetParser
from shared import dataset_folder

import pyqtgraph as pg


class LearningTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)

    # Worker connection (statistics)
    self.threadpool = QThreadPool()
    self.update_after_num_epochs = 5000

    self.label_current_epoch = QLabel("None")
    self.label_current_emotion = QLabel("None")
    self.label_full_dataset_iteration = QLabel("None")

    # Learning status
    self.label_model_train_status = QLabel("Model is not loaded. Check settings tab.")
    self.label_model_train_status.setAlignment(Qt.AlignCenter)
    self.label_model_train_status.setStyleSheet("font-weight: bold; font-size: 16px")

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

    # Statistics
    self.parser = DatasetParser(dataset_folder)
    if not self.parser.LoadDatasetIntoRam() == 0:
      print("UNHANDLED ERROR")  # TODO
    layout_statistics = QHBoxLayout()

    basic_stats_layout = QFormLayout()
    basic_stats_layout.addRow(QLabel("Epoch num (from the start): "), self.label_current_epoch)
    basic_stats_layout.addRow(QLabel("Emotion (last triggered): "), self.label_current_emotion)
    basic_stats_layout.addRow(QLabel("Full dataset iterations num: "), self.label_full_dataset_iteration)
    layout_statistics.addLayout(basic_stats_layout)

    # Amount of successfully identified emotions
    classification_stats_layout = QFormLayout()
    self.classification_results_listOfLabels = list()
    for num, emotion in enumerate(self.parser.emotion_list):
      self.classification_results_listOfLabels.append(QLabel("0/0"))
      classification_stats_layout.addRow(QLabel(emotion + ": "), self.classification_results_listOfLabels[num])
    layout_statistics.addLayout(classification_stats_layout)

    self.main_vertical_layout.addLayout(layout_statistics)

    # Plots
    plot_styles = {"color": "red", "font-size": "20px"}
    self.loss_coef_pen = pg.mkPen(color="red", width=3)
    self.accuracy_coef_pen = pg.mkPen(color="blue", width=3)

    self.statistics_plot = pg.PlotWidget()
    self.statistics_plot.setTitle("Testing stats", color="b", size="20pt")
    self.statistics_plot.setLabel("left", "Coefficient", **plot_styles)
    self.statistics_plot.setLabel("bottom", "Epoch", **plot_styles)
    self.statistics_plot.showGrid(x=True, y=True)
    self.statistics_plot.addLegend()

    # self.accuracy_plot = pg.PlotWidget()
    # self.accuracy_plot.setTitle("Testing stats", color="b", size="20pt")
    # self.accuracy_plot.setLabel("left", "Coefficient", **plot_styles)
    # self.accuracy_plot.setLabel("bottom", "Epoch", **plot_styles)
    # self.accuracy_plot.showGrid(x=True, y=True)

    # self.loss_fn_plot = pg.PlotWidget()
    # self.loss_fn_plot.setTitle("Loss function rate", color="b", size="20pt")
    # self.loss_fn_plot.setLabel("left", "Loss", **plot_styles)
    # self.loss_fn_plot.setLabel("bottom", "Epoch", **plot_styles)
    # self.loss_fn_plot.showGrid(x=True, y=True)

    # layout_plots = QHBoxLayout()
    # layout_plots.addWidget(self.accuracy_plot)
    # layout_plots.addWidget(self.loss_fn_plot)
    # self.main_vertical_layout.addLayout(layout_plots)
    self.main_vertical_layout.addWidget(self.statistics_plot)

  def UserPressedStartButton(self) -> None:
    self.button_start_model_train.setEnabled(False)
    self.button_stop_model_train.setEnabled(True)
    self.ParentClass.is_model_learning = True

    # Resetting stats
    self.current_epoch = 0
    self.current_emotion = "Angry"
    self.full_dataset_iteration = 0

    # Setting up worker
    worker = LearningWorker(self.ParentClass, self.update_after_num_epochs, self.parser)
    worker.signals.redo_plots_signal.connect(self.UpdatePlots)
    worker.signals.update_epoch_stats_signal.connect(self.UpdateEpochStat)
    worker.signals.update_emotion_classification_result_signal.connect(self.UpdateClassificationResults)
    self.threadpool.start(worker)

    self.label_model_train_status.setText("Model is running")

  def UserPressedStopButton(self) -> None:
    self.button_start_model_train.setEnabled(True)
    self.button_stop_model_train.setEnabled(False)
    self.ParentClass.is_model_learning = False
    self.threadpool.waitForDone()  # Waiting until model successfully saves itself
    self.label_model_train_status.setText("Ready for training")

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

  @Slot()
  def UpdatePlots(self, loss_results: list[float, ...], accuracy_results: list[float, ...]) -> None:
    # self.loss_fn_plot.clear()
    self.statistics_plot.clear()

    self.statistics_plot.plot(
      range(0, len(accuracy_results)), accuracy_results, name="Accuracy", pen=self.accuracy_coef_pen
    )
    self.statistics_plot.plot(range(0, len(loss_results)), loss_results, name="Loss", pen=self.loss_coef_pen)

  @Slot()
  def UpdateEpochStat(self, current_epoch: int, current_emotion: str, full_dataset_iteration: int):
    self.label_current_epoch.setText(str(current_epoch))
    self.label_current_emotion.setText(current_emotion)
    self.label_full_dataset_iteration.setText(str(full_dataset_iteration))

  @Slot()
  def UpdateClassificationResults(self, classification_result: list):
    for num, emotion in enumerate(self.parser.emotion_list):
      self.classification_results_listOfLabels[num].setText(
        str(classification_result[num]) + "/" + str(len(self.parser.testing_set_dict[emotion]))
      )
