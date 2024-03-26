from PySide6.QtCore import QRunnable, Slot


class StorageWorkerTasks:
  def __init__(self):
    # What can do
    self.task_push = "push"
    self.task_pull = "pull"


class StorageWorker(QRunnable):
  def __init__(self, abstract_storage_parent, action: str):
    super(StorageWorker, self).__init__(abstract_storage_parent, action)
    self.possible_tasks = StorageWorkerTasks()
    self.parent = abstract_storage_parent
    self.action = action

  @Slot()
  def run(self):
    self.parent.ParentClass.is_storage_busy = True
    self.parent.label_status.setText("Storage busy...")

    if self.action == self.possible_tasks.task_push:
      self.parent.cloud_storage.pushDataFolder()
    elif self.action == self.possible_tasks.task_pull:
      self.cloud_storage.pullDataFolder()

    self.parent.refreshPressed(force_check=True)
    self.parent.ParentClass.is_storage_busy = False
