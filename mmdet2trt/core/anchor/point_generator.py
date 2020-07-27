from mmdet2trt.models.builder import register_warper, build_warper
# import mmdet2trt.ops.util_ops as mm2trt_util
import mmdet2trt
import torch
from torch import nn


@register_warper("mmdet.core.anchor.point_generator.PointGenerator")
class PointGeneratorWarper(nn.Module):
    def __init__(self, module):
        super(PointGeneratorWarper, self).__init__()

    def forward(self, featmap, stride):
        shift_yy, shift_xx = mmdet2trt.ops.arange_gridmesh(featmap, strides=[stride, stride])

        shift_yy = shift_yy.flatten()
        shift_xx = shift_xx.flatten()
        stride = shift_yy*0.+stride
        shifts = torch.stack([shift_xx, shift_yy, stride], dim=-1)
        return shifts