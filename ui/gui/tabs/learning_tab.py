from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QSizePolicy, QHeaderView, QAbstractItemView
from PySide6.QtCore import Slot, Qt
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ui.gui.workers.learning_worker import LearningWorker
from ui.gui.custom_widgets.learning_statistics_table import LearningStatisticsTable
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
import pyqtgraph as pg


class LearningTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)
    self.main_vertical_layout = QVBoxLayout(self)

    # Worker connection (statistics)
    self.update_after_num_epochs = 100  # TODO: is this even needed now?

    # Learning status
    self.label_model_train_status = QLabel("Model is not loaded. Check settings tab.")
    self.label_model_train_status.setAlignment(Qt.AlignCenter)
    self.label_model_train_status.setStyleSheet("font-weight: bold; font-size: 16px")

    self.button_start_model_train = DarkStyleButton("Start training")
    self.button_start_model_train.setEnabled(False)
    self.button_start_model_train.clicked.connect(self.UserPressedStartButton)

    self.button_stop_model_train = DarkStyleButton("Stop training")
    self.button_stop_model_train.setEnabled(False)
    self.button_stop_model_train.clicked.connect(self.UserPressedStopButton)

    buttons_start_stop_layout = QHBoxLayout()
    buttons_start_stop_layout.addWidget(self.button_start_model_train)
    buttons_start_stop_layout.addWidget(self.button_stop_model_train)

    self.main_vertical_layout.addWidget(self.label_model_train_status)
    self.main_vertical_layout.addLayout(buttons_start_stop_layout)

    layout_statistics = QHBoxLayout()
    # Left side of layout_statistics
    basic_stats_layout = QFormLayout()
    self.label_epoch_num = QLabel("None")
    self.label_last_triggered_emotion = QLabel("None")
    basic_stats_layout.addRow(QLabel("Epoch: "), self.label_epoch_num)
    basic_stats_layout.addRow(QLabel("Last triggered emotion: "), self.label_last_triggered_emotion)
    layout_statistics.addLayout(basic_stats_layout)
    # Right side of layout_statistics
    self.label_last_tensor = QLabel("None")
    self.label_last_expected = QLabel("None")
    iterations_results_layout = QFormLayout()
    iterations_results_layout.addRow(QLabel("Latest iteration result: "), self.label_last_tensor)
    iterations_results_layout.addRow(QLabel("Latest expected result: "), self.label_last_expected)
    layout_statistics.addLayout(iterations_results_layout)
    self.main_vertical_layout.addLayout(layout_statistics)

    # Statistics table
    self.table_statistics = LearningStatisticsTable(self.ParentClass.parser)
    self.table_statistics.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.table_statistics.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table_statistics.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.main_vertical_layout.addWidget(self.table_statistics)

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
    self.main_vertical_layout.addWidget(self.statistics_plot)

  def UserPressedStartButton(self) -> None:
    self.button_start_model_train.setEnabled(False)
    self.button_stop_model_train.setEnabled(True)
    self.ParentClass.is_model_learning = True
    self.table_statistics.reloadTable(self.ParentClass.parser)

    # Resetting stats
    self.current_epoch = 0
    self.current_emotion = "None"

    # Setting up worker
    worker = LearningWorker(self.ParentClass, self.update_after_num_epochs, self.ParentClass.parser)
    worker.signals.redo_plots_signal.connect(self.UpdatePlots)
    worker.signals.update_epoch_stats_signal.connect(self.UpdateEpochStat)
    worker.signals.update_emotion_classification_result_signal.connect(self.UpdateClassificationResults)
    self.ParentClass.threadpool.start(worker)

    self.label_model_train_status.setText("Model is running")

  def UserPressedStopButton(self) -> None:
    self.button_start_model_train.setEnabled(True)
    self.button_stop_model_train.setEnabled(False)
    self.ParentClass.is_model_learning = False
    self.ParentClass.threadpool.waitForDone()  # Waiting until model successfully saves itself
    self.label_model_train_status.setText("Ready for training")

  def UserSelectedTab(self) -> None:
    if self.ParentClass.is_model_learning:
      return

    error_message = "Model is not loaded. Check settings tab."
    if self.ParentClass.is_model_loaded:
      error_message = "Dataset is not loaded. Check settings tab."
      if self.ParentClass.parser.isParserLoaded:
        self.label_model_train_status.setText("Ready for training")
        self.button_start_model_train.setEnabled(True)
        return

    self.label_model_train_status.setText(error_message)
    self.button_start_model_train.setEnabled(False)
    self.button_stop_model_train.setEnabled(False)

  @Slot()
  def UpdatePlots(self, loss_results: list[float, ...], accuracy_results: list[float, ...]) -> None:
    self.statistics_plot.clear()

    self.statistics_plot.plot(
      range(0, len(accuracy_results)), accuracy_results, name="Accuracy", pen=self.accuracy_coef_pen
    )
    self.statistics_plot.plot(range(0, len(loss_results)), loss_results, name="Loss", pen=self.loss_coef_pen)

  @Slot()
  def UpdateEpochStat(
    self, current_epoch: int, current_emotion: str, last_expected: list[float, ...], last_tensor: list[int, ...]
  ) -> None:
    self.label_epoch_num.setText(str(current_epoch))
    self.label_last_triggered_emotion.setText(current_emotion)
    self.label_last_expected.setText(str(last_expected))
    self.label_last_tensor.setText(str(last_tensor))

  @Slot()
  def UpdateClassificationResults(self, guessed_right: list[int, ...], emotions_average_loss: list[float, ...]) -> None:
    self.table_statistics.set_data(guessed_right, emotions_average_loss)
