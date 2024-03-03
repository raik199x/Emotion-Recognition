from PySide6.QtCore import QRunnable, Slot


class LearningWorker(QRunnable):
  """
  Worker thread that runs learning function
  """

  @Slot()
  def run(self):
    pass
