from torch import nn
from pathlib import Path
from settings import model_backup_folder


class EmotionClassificationModel(nn.Module):
  def __init__(self):
    super().__init__()
    # define parameters, layers, etc
    pass

  def train(self, data):
    # code for one epoch
    pass

  def BackupModel():
    MODEL_PATH = Path(model_backup_folder)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    # torch.save(model.state_dict(), PATH)

  def LoadModel():
    # model = TheModelClass(*args, **kwargs)
    # model.load_state_dict(torch.load(PATH))
    # model.eval()
    pass

  def forward(self, x):  # must be redefined for any nn module
    # Use activate function
    pass
