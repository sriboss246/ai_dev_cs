

import torch

ts1 = torch.tensor([[2,2],[3,4]])
print(ts1)
ts2 = torch.tensor([[1,1],[5,6]])
print(ts2)

print(ts1+ts2)
print(ts1-ts2)
print(ts1*ts2)
print(ts1/ts2)