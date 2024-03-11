import torch
import os
from pathlib import Path
from DeepLearning.settings import learning_rate


def conv_block(in_channels, out_channels, pool=False):
  layers = [
    torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
    torch.nn.BatchNorm2d(out_channels),
    torch.nn.ReLU(inplace=True),
  ]
  if pool:
    layers.append(torch.nn.MaxPool2d(2))
  return torch.nn.Sequential(*layers)


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()

    # Creating layers
    self.input = conv_block(1, 64)
    self.conv1 = conv_block(64, 64, pool=True)
    self.res1 = torch.nn.Sequential(conv_block(64, 32), conv_block(32, 64))
    self.drop1 = torch.nn.Dropout(0.5)

    self.conv2 = conv_block(64, 64, pool=True)
    self.res2 = torch.nn.Sequential(conv_block(64, 32), conv_block(32, 64))
    self.drop2 = torch.nn.Dropout(0.5)

    self.conv3 = conv_block(64, 64, pool=True)
    self.res3 = torch.nn.Sequential(conv_block(64, 32), conv_block(32, 64))
    self.drop3 = torch.nn.Dropout(0.5)

    self.classifier = torch.nn.Sequential(torch.nn.MaxPool2d(6), torch.nn.Flatten(), torch.nn.Linear(64, 7))

    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification, includes nn.LogSoftmax and nn.NLLLoss
    self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD
    # self.optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate)

  def TrainEpoch(self, tensor: torch.tensor, expected_tensor: torch.tensor) -> None:
    self.train()

    # 1. Forward pass
    classification_result = self(tensor)[0]

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
      classification_result = self(tensor)[0]
      # converted_result = (classification_result > 0.5).float()
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
    self.optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate)  # optimizer must be created after load

  def accuracy(self, expected_result: torch.Tensor, model_result: torch.Tensor) -> int:
    correct = torch.eq(expected_result, model_result).sum().item()
    acc = (correct / len(model_result)) * 100
    return acc

  def forward(self, x: torch.Tensor):  # must be redefined for any nn module
    x = x.unsqueeze(0).unsqueeze(0)

    out = self.input(x)

    out = self.conv1(out)
    out = self.res1(out) + out
    out = self.drop1(out)

    out = self.conv2(out)
    out = self.res2(out) + out
    out = self.drop2(out)

    out = self.conv3(out)
    out = self.res3(out) + out
    out = self.drop3(out)

    return self.classifier(out)
