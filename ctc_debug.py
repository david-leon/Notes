# This cost me days
# It's astonishing that with exactly the same input, CTC-pytorch produces slightly different result from CTC-theano at the first glance
# After a second thought, it's reasonable because of theano's computing graph optimization
# May I reach a conclusion that for thoese less-precise data types like 'float32', theano is superior than pytorch?
# 5-31-2017, by David Leon (Dawei Leng)

# coding: utf-8
import os
os.environ['THEANO_FLAGS'] = "floatX=float32, mode=FAST_RUN, lib.cnmem=0, warn_float64='raise'"
import torch
import numpy as np
import torch
from torch.autograd import Variable
from lasagne_ext.utils import gpickle

inf = 1E12
eps = 1E-12


import theano
from theano import tensor
from theano.ifelse import ifelse

floatX = theano.config.floatX
floatX
theano.config.floatX = 'float32'
theano.config.floatX

def torch_epslog(x):
    return torch.log(torch.clamp(x, eps, inf))

def torch_log_add(a, b):
    max_ = torch.max(a, b)
    return max_ + torch.log1p(torch.exp(a + b - 2 * max_))

def torch_log_dot_matrix(x, z):
    log_dot = torch.mm(x, z)  # (m,n)
    zeros_to_minus_inf = (z.max(0)[0] - 1.0) * inf  # (n,)
    return log_dot + zeros_to_minus_inf.expand(log_dot.size())

def torch_log_dot_tensor(x, z):
    log_dot = (x.transpose(0, 1).unsqueeze(1).expand_as(z) * z).sum(0).squeeze().t()  # (B, 2L+1)
    zeros_to_minus_inf = (z.max(0)[0] - 1).squeeze().t() * inf  # (B, 2L+1)
    return log_dot + zeros_to_minus_inf

p_prev, r2, r3, p_curr, qmp, p2, p3, p123, p_prev2 = gpickle.load('/data2/David/workspace/Code/ctc_debug.gpkl')
p2_t = torch_log_dot_matrix(torch.Tensor(p_prev), torch.Tensor(r2))
p2_t
p2_t.numpy()
p2
p2 == p2_t.numpy().all()
(p2 == p2_t.numpy()).all()
p3_t = torch_log_dot_tensor(torch.Tensor(p_prev), torch.Tensor(r3))
(p3_t.numpy() == p3).all()
p123_t = torch_log_add(p3_t, torch_log_add(torch.Tensor(p_prev), p2_t))
(p123_t.numpy() == p123).all()
p_prev2_t = torch.Tensor(p_curr) + p123_t + torch_epslog(torch.Tensor(qmp))
(p_prev2_t.numpy() == p_prev2).all()
p_prev2_t.numpy()

def _epslog(x):
    return tensor.cast(tensor.log(tensor.clip(x, 1E-12, 1E12)),
                       theano.config.floatX)


def _log_add(a, b):
    max_ = tensor.maximum(a, b)
    return max_ + tensor.log1p(tensor.exp(a + b - 2 * max_))


def _log_dot_matrix(x, z):
    inf = 1E12
    log_dot = tensor.dot(x, z)
    zeros_to_minus_inf = (z.max(axis=0) - 1) * inf
    return log_dot + zeros_to_minus_inf


def _log_dot_tensor(x, z):
    inf = 1E12
    log_dot = (x.dimshuffle(1, 'x', 0) * z).sum(axis=0).T
    zeros_to_minus_inf = (z.max(axis=0) - 1) * inf
    return log_dot + zeros_to_minus_inf.T
p_prev_tt = tensor.fmatrix()
r2_tt = tensor.fmatrix()
r3_tt = tenfor.tensor3(dtype='float32')
r3_tt = tensor.tensor3(dtype='float32')
qmp_tt = tensor.fmatrix()
p1 = p_prev_tt
p2_tt = _log_dot_matrix(p1, r2_tt)
p3_tt = _log_dot_tensor(p1, r3_tt)
p123_tt = _log_add(p3_tt, _log_add(p1, p2_tt))
p_prev2_tt = p_curr + p123_tt + _epslog(qmp_tt)
f = theano.function([p_prev_tt, r2_tt, r3_tt, qmp_tt])
f = theano.function([p_prev_tt, r2_tt, r3_tt, qmp_tt], p_prev2_tt)
p_prev2_tt_result = f(p_prev, r2, r3, qmp)
p_prev2_tt_result 
f2 = theano.function([p_prev_tt, r2_tt, r3_tt], p123_tt)
p123_tt_result = f2(p_prev, r2, r3)
p123_tt_result
(p123_tt_result == p123).all()
f3 = theano.function([qmp_tt], _epslog(qmp_tt))
elog_tt_result = f3(qmp)
elog_torch = torch_epslog(qmp)
elog_torch = torch_epslog(qmp_t)
elog_torch_result = elog_torch.numpy()
(elog_tt_result == elog_torch_result).all()
