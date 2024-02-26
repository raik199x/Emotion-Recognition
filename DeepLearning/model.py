import torch
import os
from pathlib import Path
from shared import pretrained_emotion_recognition_model, GetRelativePath
from DeepLearning.settings import learning_rate, pytorch_device


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.backup_path = GetRelativePath(pretrained_emotion_recognition_model)

    # Creating layers
    self.input_layer = torch.nn.Linear(in_features=68 * 2, out_features=128)
    self.hidden_layer_1 = torch.nn.Linear(in_features=128, out_features=64)
    self.hidden_layer_2 = torch.nn.Linear(in_features=64, out_features=128)
    self.output_layer = torch.nn.Linear(in_features=128, out_features=7)  # 7 emotions

    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification, includes nn.LogSoftmax and nn.NLLLoss
    self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD

  def TrainEpoch(self, data: list[[int, int], ...], expected_result: list[int, int, ...]) -> None:
    self.train()

    # 0. Converting function input into tensors
    expected_tensor = torch.from_numpy(expected_result)
    expected_tensor = expected_tensor.float().to(pytorch_device)
    tensor = torch.from_numpy(data).to(pytorch_device)
    tensor = tensor.float().flatten()

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

  def TestingEpoch(self, data, expected_result):
    self.eval()
    with torch.inference_mode:
      classification_result = self(data)
    return self.accuracy(expected_result, classification_result)

  def BackupModel(self, folder_path: str, file_name: str):
    MODEL_PATH = Path(folder_path)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    torch.save(self.state_dict(), os.path.join(folder_path, file_name))

  def LoadModel(self, path_to_model):
    self.load_state_dict(torch.load(path_to_model))
    self.eval()

  def accuracy(self, expected_result, model_result):
    correct = torch.eq(expected_result, model_result).sum().item()
    acc = (correct / len(model_result)) * 100
    return acc

  def forward(self, x):  # must be redefined for any nn module
    return self.output_layer(self.hidden_layer_2(self.hidden_layer_1(self.input_layer(x))))
