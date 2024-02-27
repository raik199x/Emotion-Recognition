import torch
import os
import numpy as np
from pathlib import Path
from DeepLearning.settings import learning_rate, pytorch_device


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()

    # Creating layers
    self.input_layer = torch.nn.Linear(in_features=48 * 48, out_features=128)
    self.hidden_layer_1 = torch.nn.Linear(in_features=128, out_features=64)
    self.hidden_layer_2 = torch.nn.Linear(in_features=64, out_features=128)
    self.output_layer = torch.nn.Linear(in_features=128, out_features=7)  # 7 emotions

    self.act = torch.nn.ReLU()
    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification, includes nn.LogSoftmax and nn.NLLLoss
    self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD

  def TrainEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> None:
    self.train()

    # 1. Forward pass
    classification_result = self(tensor)

    # 2. Calculate the loss
    loss_coefficient = self.loss_fn(classification_result, expected_tensor)

    # 3. Use optimizer
    self.optimizer.zero_grad()

    # 4. Perform backpropogation
    loss_coefficient.backward()

    # 5. Optimizer step
    self.optimizer.step()

  def TestingEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor):
    self.eval()
    with torch.inference_mode():
      classification_result = self(tensor)

    print(expected_tensor)
    print(classification_result)
    print(self.accuracy(expected_tensor, classification_result))
    print(self.loss_fn(classification_result, expected_tensor).item())

  def BackupModel(self, folder_path: str, file_name: str):
    MODEL_PATH = Path(folder_path)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    torch.save(self.state_dict(), os.path.join(folder_path, file_name))

  def LoadModel(self, path_to_model: str):
    self.load_state_dict(torch.load(path_to_model))
    self.eval()

  def accuracy(self, expected_result: torch.Tensor, model_result: torch.Tensor) -> int:
    correct = torch.eq(expected_result, model_result).sum().item()
    acc = (correct / len(model_result)) * 100
    return acc

  def forward(self, x: torch.Tensor):  # must be redefined for any nn module
    X = self.act(self.input_layer(x))
    X = self.act(self.hidden_layer_1(X))
    X = self.act(self.hidden_layer_2(X))
    return self.output_layer(X)
