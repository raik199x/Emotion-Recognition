# Emotion-Recognition

Emotion recognition on python + pytorch. Made as diploma work for Belarusian State University of Informatics and Radioelectronics.

## WORK IN PROGRESS

This app in under development, everything described in this project might and WILL be changed.

### TODO

- [ ] Parse dataset
  - [ ] Using program parse dataset to find all images where faces are identified.
  - [ ] By hand seek and delete images that is failed to properly set 68 point landmarks.
- [x] Face detection module
- [x] Face landmark module
- [ ] Emotion recognition module
  - [ ] Steps are in progress
- [ ] Ui module (qt)
- [ ] Camera module (using cv2)
- [ ] Base of pre-trained ML models module
  - [x] Downloaded face detection and landmark detection models
- [ ] Analysis and stats module
- [ ] LLM module (?)
- [ ] Web server learning module (?)
- [ ] Dlib, set up for using cuda

## Requirements

### Cuda

This project uses cuda 11.8. You should install it on your own, but you might want to visit [cuda 11.8 toolkit download page](https://developer.nvidia.com/cuda-11-8-0-download-archive) and [cudann archive page](https://developer.nvidia.com/rdp/cudnn-archive).

If your os is ubuntu, you can use [this guide](https://medium.com/@gokul.a.krishnan/how-to-install-cuda-cudnn-and-tensorflow-on-ubuntu-22-04-2023-20fdfdb96907) to install cuda + cudann.

### Pytorch

Use the official install [guide](https://pytorch.org/get-started/locally/)

### Dlib

Requires for face detection and landmarks

Since we need to use cuda, do not install Dlib if cuda is not available

First visit [official dlib site](http://dlib.net/) and download dlib.

~~Installation via pip: ```pip3 install dlib```~~

TODO: Install with cuda

### opencv

```pip3 install cv2```

### Dataset

TODO: explain dataset folder

## Running

pass

## Useful links

[Pytorch under a day](https://www.youtube.com/watch?v=Z_ikDlimN6A) -- nice introduction into pytorch, for me just required 19/24 hours under 1.5 speed.
