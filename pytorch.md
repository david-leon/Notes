# Pytorch Note

* Pytorch and Chainer are in great resemblance, from architecture to API grammer.

* `x_cuda = x.cuda(device_id=0)` returns a new tensor on gpu0, meanwhile x is kept as it was; i.e., this is copy op. After this, change x has no effect on x_cuda and vice versa. Use `.cpu()` to copy the tensor from GPU to 

* Pytorch variable has no .zero_grad() function as Chainer, use `.data.zero_()` to do the job (In Pytorch, only nn.Module class has .zero_grad() attribute)

* Pytorch use Module.train() & Model.eval() calls with empty param to switch between training mode and evaluation mode

* torch.Tensor() is just an alias of torch.FloatTensor(), not what I expected as an universal constructer which would determine the dtype according to input ndarray. torch.from_numpy() does this job meanwhile.

* For RNN with multiple layers and dropout enabled, the pytorch implementation does not apply dropout for the last layer.

* The difference between `LSTM` and `LSTMCell` lies in the input shape: input of `LSTM` is 3D (B, T, D) whereas input of `LSTMCell` is 2D (B, D), i.e., `LSTMCell` is used for just one time step.

* The `LSTM` implementation of Pytorch has two problems: 1) no peepholes  2) two biases in `i_t, f_t, g_t, o_t`, which is nonsense (according to Facebook's comment, it's from CuDNN's convention)

* Pytorch does not support numpy-style broadcasting, so to do element-wise multiplication, for example `X` (3, 50)
and `y` (50), you need do `.unsqueeze` and then `.expand`:     `X * y.unsqueeze(0).expand_as(X)`

* Even with `batch_first=True`, the hiddens returned by LSTM(GRU, etc) are still of size  `(num_layers * num_directions, batch, hidden_size)`

* The `CNN` implementation of Pytorch does not do filter flipping by default; and its speed is comparable to Theano's `CNN`, produces exactly the same result, meanwhile `convolve2d()` of scipy is about 2 * times slower, and result slightly different (within 10 `eps`); source code of Pytorch's convolution resides in `pytorch/torch/csrc/autograd/functions/convolution.cpp`

* Pytorch does not do weight initialization automatically, you have to define a `reset_parameters()` function yourself, and call it at model initialization.

* `Tensor.numpy()` return a numpy array **sharing** the memory. In another word, it just returns the memory pointer. So we can use this mechanism to **MODIFY** the value of a tensor, though not intuitive.

* To set a model/module to switch between *train/predict* mode, call `nn.Module.train(True/False)`. This function will recursively set every child module's mode. **NEVER** use `self.training=True/False`, this only applies to the current module without effecting its children.



