#  一个Conv算子的生命历程



##  概述

我们将尝试用一个简单的卷积算子的调用过程为例，探究在Pytorch中Python前端调用后端算子完整流程。



##  Python端代码



假设我们使用Pytorch定义了如下模型：

```python
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2))
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(32, 64, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
        self.dense = torch.nn.Sequential(
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 10)
        )

    def forward(self, x):
        conv1_out = self.conv1(x)
        conv2_out = self.conv2(conv1_out)
        conv3_out = self.conv3(conv2_out)
        # 自适应池化， w，h都输出为1 得到全局平均池化
        res = torch.nn.functional.adaptive_avg_pool2d(conv3_out, (1, 1))
        # 扁平化
        res = res.view(res.size(0), -1)
        out = self.dense(res)
        return out
```

这是一个非常常见使用



Pytorch是如何实现torch.nn.conv2d这个卷积算子的呢？

在路径 **torch/nn/module/conv.py**这个文件中给出了卷积算子在Python









