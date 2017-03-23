# Pytorch Note

* Pytorch and Chainer are in great resemblance, from architecture to API grammer.
* x_cuda = x.cuda(device_id=0) returns a new tensor on gpu0, meanwhile x is kept as it was; i.e., this is copy op. After this, change x has no effect on x_cuda and vice versa. Use .cpu() to copy the tensor from GPU to CPU
* Pytorch variable has no .zero_grad() function as Chainer, use .data.zero_() to do the job (In Pytorch, only nn.Module class has .zero_grad() attribute)
* Pytorch use Module.train() & Model.eval() calls with empty param to switch between training mode and evaluation mode
* torch.Tensor() is just an alias of torch.FloatTensor(), not what I expected as an universal constructer which would determine the dtype according to input ndarray. torch.from_numpy() does this job meanwhile.




