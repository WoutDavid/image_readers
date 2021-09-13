import sys
import os
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from skimage import io
from nd2reader import ND2Reader
from nd2reader import parser


nd2_filename =  sys.argv[1] if len(sys.argv) != 1 else '/home/nacho/Downloads/to_delete/210317_201_dg1.nd2' # this was just for testing purposes
print(f"Processing {nd2_filename}")

nd2_filename_prefix = os.path.splitext(nd2_filename)[0]
nd2_filename_base = os.path.splitext(os.path.basename(nd2_filename))[0]

c_number = int(sys.argv[2]) if len(sys.argv) == 3 else 0
print(f"c_number = {c_number}")

z_number = int(sys.argv[3]) if len(sys.argv) == 4 else 0
print(f"z_number = {z_number}")

parent_dir = os.path.dirname(nd2_filename)

# take_maxip = True if len(sys.argv) == 5 else False
take_maxip = False


with ND2Reader(nd2_filename) as images:
    n_zstacks = int(images.sizes['z'])
    n_tiles = int(images.sizes['v'])



    for z_num in range(0, n_zstacks):
        os.makedirs(os.path.join(parent_dir, nd2_filename_prefix, f"z_stack_{z_num+1}"), exist_ok=True)
        for i in range(0, n_tiles):
            if take_maxip:
                n_zstacks = int(images.sizes['z'])
                ic(n_zstacks)
                # Take all z-stacks into a list of images
                temp_image_stack = [images.get_frame_2D(c=0, v=i, z=j) for j in range(0, n_zstacks)]
                temp_image = np.maximum.reduce(temp_image_stack)
            else:
                temp_image = images.get_frame_2D(c=c_number, v=i, z=z_num)
            io.imsave(os.path.join(parent_dir, nd2_filename_prefix, f"z_stack_{z_num+1}",f"{nd2_filename_base}_extracted_c{c_number}_z{z_num+1}_tile{i+1}.tif"), temp_image)
