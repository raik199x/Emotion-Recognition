import torch
import os
from pathlib import Path
from DeepLearning.settings import learning_rate


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()

    # Creating layers
    self.input = torch.nn.Linear(in_features=48 * 48, out_features=512)

    self.hidden1 = torch.nn.Linear(in_features=512, out_features=512)
    self.drop1 = torch.nn.Dropout(0.3)

    self.hidden2 = torch.nn.Linear(in_features=512, out_features=512)
    self.drop2 = torch.nn.Dropout(0.2)

    self.hidden3 = torch.nn.Linear(in_features=512, out_features=512)
    self.drop3 = torch.nn.Dropout(0.15)

    self.output = torch.nn.Linear(in_features=512, out_features=7)

    self.act = torch.nn.ReLU(inplace=True)
    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification, includes nn.LogSoftmax and nn.NLLLoss
    self.optimizer = self.CreateOptimizer()

  def CreateOptimizer(self):  # To stop messing optimizers after load and creation
    return torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD
    # or torch.optim.SGD(self.parameters(), lr=learning_rate)

  def TrainEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> torch.Tensor:
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

    return classification_result

  def TestingEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> dict[str:int, str:int]:
    self.eval()
    with torch.inference_mode():
      classification_result = self(tensor)

      return {
        "Accuracy": self.accuracy(expected_tensor, classification_result),
        "Loss": self.loss_fn(classification_result, expected_tensor).item(),
        "Prediction": classification_result,
        # "IsPredictedRight": torch.all(torch.eq(converted_result, expected_tensor)),
        "IsPredictedRight": torch.argmax(classification_result) == torch.argmax(expected_tensor),
      }

  def BackupModel(self, folder_path: str, file_name: str) -> None:
    MODEL_PATH = Path(folder_path)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    torch.save(self.state_dict(), os.path.join(folder_path, file_name))

  def LoadModel(self, path_to_model: str) -> None:
    self.load_state_dict(torch.load(path_to_model))
    self.eval()
    self.optimizer = self.CreateOptimizer()  # optimizer must be recreated after load

  def accuracy(self, expected_result: torch.Tensor, model_result: torch.Tensor) -> int:
    correct = torch.eq(expected_result, model_result).sum().item()
    acc = (correct / len(model_result)) * 100
    return acc

  def forward(self, x: torch.Tensor):  # must be redefined for any nn module
    out = self.input(x)

    out = self.hidden1(out)
    out = self.act(out)
    out = self.drop1(out)

    out = self.hidden2(out)
    out = self.act(out)
    out = self.drop2(out)

    out = self.hidden3(out)
    out = self.act(out)
    out = self.drop3(out)

    return self.output(out)
