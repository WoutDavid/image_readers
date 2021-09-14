import sys
import os
import argparse
import numpy as np
import aicspylibczi
from PIL import Image
from skimage import io


ap = argparse.ArgumentParser(description="Extract specific slices from a raw .czi image.")
# mandatory args
ap.add_argument('czi_path',type=str,help="Path (relative or absolute) to target image")

# optional args
# file creation
ap.add_argument('-o', '--out_dir', type=str, help="Root directory where output should be stored, default is base dir of the input image")

# Indices
ap.add_argument('-c', '--c_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the channels that need to be extracted, default is all of them.")
ap.add_argument('-t', '--t_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the time series that need to be extracted, default is all of them.")
ap.add_argument('-z', '--z_numbers', default=-1, type=int, nargs='+', help="Indexes (start at 0) of the z-stacks that need to be extracted, default is all of them.")

# Booleans
ap.add_argument('-r','--read', default=False, action="store_true", help="If true, the image will only be read and its dimensions will be printed out.")
ap.add_argument('-m','--maxIP', default=False, action="store_true", help="Boolean to indicate whether to take a maxIP of the z-stacks, default is False")

# parse args
args = ap.parse_args()

# Extracht basename of the filepath to create future filenames
czi_filename_base = os.path.splitext(os.path.basename(args.czi_path))[0]

# If no output dir was input, use the base directory of the input file
if not args.out_dir:
    args.out_dir =  os.path.dirname(args.czi_path)


# Read in filename
czi = aicspylibczi.CziFile(args.czi_path)

# error parsing
if not czi.is_mosaic():
    print("Given file is not a mosaic file.")
    sys.exit()

# If read flag, merely read it's dimensions and exit the script
if args.read:
    print(f"{czi_filename_base} dimensions: {czi.dims_shape()[0]}")
    sys.exit()
# If no specific numbers were put in, default to the full range of the dimensions

if args.z_numbers == -1:
    z_min, z_max = czi.dims_shape()[0]['Z']
    args.z_numbers = range(z_min,z_max)
if args.t_numbers == -1:
    t_min, t_max = czi.dims_shape()[0]['T']
    args.v_numbers = range(v_min,v_max)
if args.c_numbers == -1:
    c_min, c_max = czi.dims_shape()[0]['C']
    args.c_numbers = range(c_min,c_max)

# Helper function for taking maxIP
def maxIPstack(img_list):
    parsed_list = img_list
    parsed_list = [img if isinstance(img, np.ndarray) else io.imread(img) for img in img_list]
    # now all elements in parsed_list are ndarrays
    maxIP = np.maximum.reduce(parsed_list)
    return maxIP

# first loop over channels
for c_num in args.c_numbers:
    # then for every channel, look at every tile
    for t_num in args.t_numbers:
        # Make a directory for this particular c-v combinations
        # ic(os.path.join(args.out_dir, nd2_filename_base, f"channel_{c_num+1}/",f"tile_{v_num+1}/"))
        os.makedirs(os.path.join(args.out_dir, czi_filename_base, f"channel_{c_num+1}/",f"tile_{t_num+1}/"),exist_ok=True)

        # then for each tile, either take maxip:
        if args.maxIP:
            image_list = []
            for z_num in args.z_numbers:
                mosaic_data = czi.read_mosaic(C=c_num, Z=z_num, scale_factor=1)
                mosaic_data = mosaic_data[0,0,:,:].astype(np.uint16)
                image_list.append(mosaic_data)

            maxIP = maxIPstack(image_list)
            output_filename= os.path.join(args.out_dir, czi_filename_base, f"channel_{c_num+1}/",f"tile_{t_num+1}/", f"{czi_filename_base}_extracted_c{c_num+1}_tile{t_num+1}_maxIP.tif")
            io.imsave(output_filename, maxIP, check_contrast=False)

        # If no maxIP, then save all z-stacks seperately in yet another loop
        else:
            for z_num in args.z_numbers:
                mosaic_data = czi.read_mosaic(C=c_num, Z=z_num, scale_factor=1)
                mosaic_data = mosaic_data[0,0,:,:].astype(np.uint16)
                img = Image.fromarray(mosaic_data)
                output_filename= os.path.join(args.out_dir, czi_filename_base, f"channel_{c_num+1}/", f"tile_{t_num+1}/", f"{czi_filename_base}_extracted_c{c_num+1}_t{t_num+1}_z{z_num+1}.tif")
                img.save(output_filename)
