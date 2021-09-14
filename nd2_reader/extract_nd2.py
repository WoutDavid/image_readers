import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from nd2reader import ND2Reader


ap = argparse.ArgumentParser(description="Extract specific slices from a raw .nd2 image.")
# mandatory args
ap.add_argument('nd2_path',type=str,help="Path (relative or absolute) to target image")

# optional args
# file creation
ap.add_argument('-o', '--out_dir', type=str, help="Root directory where output should be stored, default is base dir of the input image")

# Indices
ap.add_argument('-c', '--c_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the channels that need to be extracted, default is all of them.")
ap.add_argument('-v', '--v_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the time series that need to be extracted, default is all of them.")
ap.add_argument('-z', '--z_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the z-stacks that need to be extracted, default is all of them.")

# Booleans
ap.add_argument('-r','--read', default=False, action="store_true", help="If true, the image will only be read and its dimensions will be printed out.")
ap.add_argument('-m','--maxIP', default=False, action="store_true", help="Boolean to indicate whether to take a maxIP of the z-stacks, default is False")

# parse args
args = ap.parse_args()

# Extracht basename of the filepath to create future filenames
nd2_filename_base = os.path.splitext(os.path.basename(args.nd2_path))[0]

# If no output dir was input, use the base directory of the input file
if not args.out_dir:
    args.out_dir =  os.path.dirname(args.nd2_path)

with ND2Reader(args.nd2_path) as images:
    # If read flag, merely read it's dimensions and exit the script
    if args.read:
        print(f"{nd2_filename_base} dimensions: {images.sizes}")
        sys.exit()
    # If no specific numbers were put in, default to the full range of the dimensions
    if args.z_numbers == -1:
        args.z_numbers = range(0,int(images.sizes['z']))
    if args.v_numbers == -1:
        args.v_numbers = range(0,int(images.sizes['v']))
    if args.c_numbers == -1:
        args.c_numbers = range(0,int(images.sizes['c']))

    # first loop over channels
    for c_num in args.c_numbers:
        # then for every channel, look at every tile
        for v_num in args.v_numbers:
            # Make a directory for this particular c-v combinations
            # ic(os.path.join(args.out_dir, nd2_filename_base, f"channel_{c_num+1}/",f"tile_{v_num+1}/"))
            os.makedirs(os.path.join(args.out_dir, nd2_filename_base, f"channel_{c_num+1}/",f"tile_{v_num+1}/"),exist_ok=True)

            # then for each tile, either take maxip:
            if args.maxIP:
                # Take all z-stacks into a list of images
                temp_image_stack = [images.get_frame_2D(c=c_num, v=v_num, z=j) for j in args.z_numbers]
                temp_image = np.maximum.reduce(temp_image_stack)
                io.imsave(os.path.join(args.out_dir, nd2_filename_base, f"channel_{c_num+1}/",f"tile_{v_num+1}/",f"{nd2_filename_base}_extracted_c{c_num+1}_tile{v_num+1}_maxIP.tif"), temp_image)

            # If no maxIP, then save all z-stacks seperately in yet another loop
            else:
                for z_num in args.z_numbers:
                    temp_image = images.get_frame_2D(c=c_num, v=v_num, z=z_num)
                    io.imsave(os.path.join(args.out_dir, nd2_filename_base, f"channel_{c_num+1}/",f"tile_{v_num+1}/",f"{nd2_filename_base}_extracted_c{c_num+1}_tile{v_num+1}_z{z_num+1}.tif"), temp_image)
