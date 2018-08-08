"""
2D Residual Unet Example
================================

This example should illustrate how to a Residual Unet 
as a layer

"""
import torch
import inferno.extensions.layers.unet as unet

from inferno.extensions.layers.convolutional import ConvELU2D,ConvELU3D,ConvSigmoid2D
















# a 2D data with 10 input channels
x = torch.rand(1, 10, 64,64)
x = torch.autograd.Variable(x)
b
# a unet with resiudal blocks
model = unet.ResBlockUNet(in_channels=10, out_channels=20, dim=2)

# pass x trough unet 
out = model(x)

print(out.size())



"""
Chained 3D Residual Unets
================================

This example should illustrate how chain
multiple residual unets
"""



# 3D data with 5 input channels
x = torch.rand(1, 5, 32,32, 32)
x = torch.autograd.Variable(x)

# a unet with resiudal blocks
model_a = unet.ResBlockUNet(in_channels=5, out_channels=12, dim=3, 
                            unet_kwargs=dict(depth=3))

# if the last layer in the second unet
# shall be non-activated  we set 
# activated to False, this will only affect the
# very last convolution of the net
model_b = unet.ResBlockUNet(in_channels=12, out_channels=2,  dim=3,
                            activated=False,
                            unet_kwargs=dict(depth=3))

# chain models
model = torch.nn.Sequential(model_a, model_b)

# and use the model
out = model(x)
print(out.size())




"""
A Custom UNet
================================

This example should illustrate how create
a custom UNet by deriving from UNetBase
"""

class MySimple2DUnet(unet.UNetBase):
    def __init__(self, **kwargs):
        super(MySimple2DUnet, self).__init__(dim=2, **kwargs)


    def conv_op_factory(self, in_channels, out_channels, part, index):

        # are we in the very last block?
        if  part=='up' and index + 1 == self.depth:
            return torch.nn.Sequential(
                ConvELU2D(in_channels=in_channels,  out_channels=out_channels, kernel_size=3),
                ConvELU2D(in_channels=out_channels, out_channels=out_channels, kernel_size=3),
                ConvSigmoid2D(in_channels=out_channels, out_channels=out_channels, kernel_size=3)
            )
        else:
            return torch.nn.Sequential(
                ConvELU2D(in_channels=in_channels,  out_channels=out_channels, kernel_size=3),
                ConvELU2D(in_channels=out_channels, out_channels=out_channels, kernel_size=3),
                ConvELU2D(in_channels=out_channels, out_channels=out_channels, kernel_size=3)
            )





# 2D data with 5 input channels
x = torch.rand(1, 5, 32, 32)
x = torch.autograd.Variable(x)
my_custom_unet = MySimple2DUnet(in_channels=5, out_channels=12, depth=3)


# and use the model
out = my_custom_unet(x)
print(out.size())
