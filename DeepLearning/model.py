import torch
from pathlib import Path
from shared import pretrained_emotion_recognition_model, data_folder, GetRelativePath
from setting import learning_rate, pytorch_device


class EmotionClassificationModel(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.backup_path = GetRelativePath(data_folder + pretrained_emotion_recognition_model)

    # Creating layers
    self.input_layer = torch.nn.Linear(
      in_features=136, out_features=128
    )  # 68 points * 2 = 136 x and y coordinates as input layer
    self.hidden_layer_1 = torch.nn.Linear(in_features=128, out_features=64)
    self.hidden_layer_2 = torch.nn.Linear(in_features=64, out_features=128)
    self.output_layer = torch.nn.Linear(in_features=128, out_features=7)  # 7 emotions

    self.loss_fn = torch.nn.CrossEntropyLoss()  # Multi class classification
    self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)  # Most effective Adam and SGD

  def TrainEpoch(self, data: list[[int, int], ...], expected_result: list[int, int, ...]) -> None:
    self.train()

    # 0. Converting function input into tensors
    expected_tensor = torch.from_numpy(expected_result)
    tensor = torch.from_numpy(data).to(pytorch_device)
    tensor = tensor.float().flatten()

    # 1. Forward pass
    classification_result = self(data)

    # 2. Calculate the loss
    loss_coefficient = self.loss_fn(classification_result, expected_tensor)

    # 3. Use optimizer
    self.optimizer.zero_grad()

    # 4. Perform backpropogation
    loss_coefficient.backward()

    # 5. Optimizer step
    self.optimizer.step()

  def TestingEpoch(self, data):
    self.eval()
    with torch.inference_mode:
      classification_result = self(data)

      # loss_coefficient = self.loss_fn(classification_result, real_answer)

  def BackupModel(self):
    MODEL_PATH = Path(self.backup_path)
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    # torch.save(model.state_dict(), PATH)

  def LoadModel():
    # model = TheModelClass(*args, **kwargs)
    # model.load_state_dict(torch.load(PATH))
    # model.eval()
    pass

  def forward(self, x):  # must be redefined for any nn module
    return self.output_layer(self.hidden_layer_2(self.hidden_layer_1(self.input_layer(x))))
