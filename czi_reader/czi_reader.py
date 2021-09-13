import numpy as np
from aicspylibczi import CziFile
from pathlib import Path
import matplotlib.pyplot as plt
from icecream import ic
from PIL import Image
from maxIP import maxIPstack

##overlap stitches is 10 pixels

image = "/media/tool/gabriele_data/1442_OB/170717_mBrain_schizo_1442-front_b1.czi"
czi=CziFile(image)
#dim_shape is a list, of which only the first element is useful.
dimension = czi.dims_shape()
ic(dimension)
# ic((dimension[0]['S'])[1])
img = czi.read_image(S=0, C=1, Z=1)
ic(img[0].shape)

def unwrapDimensions(czi):
    dim_dict = czi.dims_shape()[0]
    max_channel = dim_dict['C'][1]
    max_series = dim_dict['S'][1]
    max_zstack = dim_dict['Z'][1]
    return max_channel, max_series, max_zstack

max_channel, max_series , max_zstack= unwrapDimensions(czi)

# for i in range(0,max_channel):
#     image_zstack = [czi.read_image(S=0, C=i, Z=j) for j in range(0,max_zstack)]
#     maxIP_image = maxIPstack(image_zstack)
#     ic(maxIP_image.shape)
#     im = Image.fromarray(maxIP_image)
#     im.save(f"/media/tool/gabriele_data/1442_OB/170717_mBrain_schizo_1442-front_b2_maxIP_channel{i}.tif")


