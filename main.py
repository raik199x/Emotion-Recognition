from torch import __version__ as pytorch_version
from DeepLearning import dataset_parser, model, settings
from torch import from_numpy

if __name__ == "__main__":
  print(pytorch_version)
  print(settings.pytorch_device)

  parser = dataset_parser.DatasetParser()
  generator = parser.EmotionNpPointGenerator(parser.forLearning, parser.angry)
  values = next(generator)

  tensor = from_numpy(values).to(settings.pytorch_device)
  tensor = tensor.float().flatten()

  emotion_recognition_model = model.EmotionClassificationModel().to(settings.pytorch_device)
  print(emotion_recognition_model(tensor))
