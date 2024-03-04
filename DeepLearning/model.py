import torch
import os
from pathlib import Path
from DeepLearning.settings import learning_rate


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()

    # Creating layers
    self.input_layer = torch.nn.Linear(in_features=48 * 48, out_features=512)
    self.hidden_layer_1 = torch.nn.Linear(in_features=512, out_features=128)
    self.hidden_layer_2 = torch.nn.Linear(in_features=128, out_features=64)
    self.output_layer = torch.nn.Linear(in_features=64, out_features=7)  # 7 emotions

    self.act = torch.nn.ReLU()
    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification, includes nn.LogSoftmax and nn.NLLLoss
    self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD

  def TrainEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> None:
    self.train()

    # 1. Forward pass
    classification_result = self(tensor)

    # 2. Calculate the loss
    loss_coefficient = self.loss_fn(classification_result, expected_tensor)

    # 3. Zero gradients of the optimizer
    self.optimizer.zero_grad()

    # 4. Perform backpropogation
    loss_coefficient.backward()

    # 5. Optimizer step
    self.optimizer.step()

  def TestingEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> dict[str:int, str:int]:
    self.eval()
    with torch.inference_mode():
      classification_result = self(tensor)
      return {
        "Accuracy": self.accuracy(expected_tensor, classification_result),
        "Loss": self.loss_fn(classification_result, expected_tensor).item(),
        "Prediction": classification_result,
        "IsPredictedRight": torch.all(torch.eq(torch.round(classification_result), expected_tensor)),
      }

  def BackupModel(self, folder_path: str, file_name: str) -> None:
    MODEL_PATH = Path(folder_path)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    torch.save(self.state_dict(), os.path.join(folder_path, file_name))

  def LoadModel(self, path_to_model: str) -> None:
    self.load_state_dict(torch.load(path_to_model))
    self.eval()
    self.optimizer = torch.optim.Adam(
      self.parameters(), lr=learning_rate
    )  # ? If :attr:assign is True the optimizer must be created after the call to :attr:load_state_dict.

  def accuracy(self, expected_result: torch.Tensor, model_result: torch.Tensor) -> int:
    correct = torch.eq(expected_result, model_result).sum().item()
    acc = (correct / len(model_result)) * 100
    return acc

  def forward(self, x: torch.Tensor):  # must be redefined for any nn module
    x = self.act(self.input_layer(x))
    x = self.act(self.hidden_layer_1(x))
    x = self.act(self.hidden_layer_2(x))
    return self.output_layer(x)
