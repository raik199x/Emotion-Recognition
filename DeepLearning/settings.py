from torch.cuda import is_available as pytorch_is_cuda_working


pytorch_device = "cuda" if pytorch_is_cuda_working else "cpu"
