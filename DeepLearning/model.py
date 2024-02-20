import torch
from pathlib import Path
from settings import model_backup_folder, pytorch_device


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.to(device=pytorch_device)  # Determine where model should run

    # Pick loss function
    self.loss_fn  # = ?
    # Pick optimizer
    self.optimizer  # = ?

    # define parameters, layers, etc
    self.input_layer = torch.input_layer()
    pass

  def TrainEpoch(self, data):
    self.train()

    # 1. Forward pass
    # classification_result = self(data)

    # 2. Calculate the loss
    # loss_coefficient = self.loss_fn(classification_result, real_answer)

    # 3. Use optimizer
    # self.optimizer.?

    # 4. Perform backpropogation
    # loss_coefficient.backward()

    # 5. Optimizer step
    # self.optimizer.step()

    pass

  def TestingEpoch(self, data):
    self.eval()
    with torch.inference_mode:
      classification_result = self(data)

      # loss_coefficient = self.loss_fn(classification_result, real_answer)

  def BackupModel():
    MODEL_PATH = Path(model_backup_folder)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    # torch.save(model.state_dict(), PATH)

  def LoadModel():
    # model = TheModelClass(*args, **kwargs)
    # model.load_state_dict(torch.load(PATH))
    # model.eval()
    pass

  def forward(self, x: torch.Tensor) -> torch.Tensors:  # must be redefined for any nn module
    # Use activate function
    pass
