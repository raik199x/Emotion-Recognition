# Emotion-Recognition

![Codacy Badge](https://api.codacy.com/project/badge/Grade/fa07a39a4cfe41d3a4c04a3d7e1dbde8)

Emotion recognition on python + pytorch. Made as diploma work for Belarusian State University of Informatics and Radioelectronics.

## WORK IN PROGRESS

This app in under development, everything described in this project might and WILL be changed.

## Requirements

### Cuda

This project uses cuda 11.8 (but you can try using newer version). You should install it on your own, but you might want to visit [cuda 11.8 toolkit download page](https://developer.nvidia.com/cuda-11-8-0-download-archive) and [cudann archive page](https://developer.nvidia.com/rdp/cudnn-archive).

If your os is ubuntu, you can use [this guide](https://medium.com/@gokul.a.krishnan/how-to-install-cuda-cudnn-and-tensorflow-on-ubuntu-22-04-2023-20fdfdb96907) to install cuda + cudann.

### Pytorch

Use the official install [guide](https://pytorch.org/get-started/locally/)

### Dlib

Requires for face detection and landmarks

Since we need to install dlib with cuda (note: installing with pip does not enabled cuda for me), visit [official dlib site](http://dlib.net/) and download dlib.

Enter downloaded directory and write ```sudo python3 setup.py install```

While installation is starting, look at the logs and find something like that:

```text
-- Looking for cuDNN install...
-- Found cuDNN: /usr/lib/x86_64-linux-gnu/libcudnn.so
-- Enabling CUDA support for dlib.  DLIB WILL USE CUDA, compute capabilities: 50
```

In that case you can continue installation, otherwise check your cuda and cudann installation.

After install is complete, write:

```bash
python3
import dlib
dlib.DLIB_USE_CUDA
```

Output must be ```True```

Try to run tests, in my case i got error

```text
Could not load library libcublasLt.so.12. Error: libcublasLt.so.12: cannot open shared object file: No such file or directory
Invalid handle. Cannot load symbol cublasLtCreate
```

If you also encounter this error, you need to install [libcublasLt.so.12](https://packages.debian.org/trixie/amd64/libcublaslt12/download).

### Required python packages

Just run the following command:

```pip3
pip3 install -r requirements.txt
```

***IMPORTANT:*** ```requirements.txt``` does not include **dlib** and **pytorch** package

### Dataset

TODO: explain dataset folder

## Running

pass

## Useful links

[Pytorch under a day](https://www.youtube.com/watch?v=Z_ikDlimN6A) -- nice introduction into pytorch, for me just required 19/24 hours under 1.5 speed.

[Dmitriy Pertsev](https://www.bsuir.by/ru/kaf-evm/pertsau) -- My coach and reviewer
