import sys
import os
import numpy as np
from glob import glob
from skimage import io
from nd2reader import ND2Reader

def parseND2toISS(nd2_path: str, out_dir: str, round_nr: int, read = False, maxIP=True):
    # Extracht basename of the filepath to create future filenames
    nd2_filename_base = os.path.splitext(os.path.basename(nd2_path))[0]

    # If no output dir was input, use the base directory of the input file
    if not out_dir:
        out_dir =  os.path.dirname(nd2_path)

    out_dir = os.path.join(out_dir, f"Round{round_nr}/")
    os.makedirs(out_dir, exist_ok=True)

    with ND2Reader(nd2_path) as images:
        # If read flag, merely read it's dimensions and exit the script
        if read:
            print(f"{nd2_filename_base} dimensions: {images.sizes}")
            sys.exit()

        # Try is for when it only has one z stack, then it's not going to be a correct key
        try:
            z_numbers = range(0,int(images.sizes['z']))
        except:
            z_numbers =[0]
        # If no specific numbers were put in, default to the full range of the dimensions
        try:
            v_numbers = range(0,int(images.sizes['v']))
        except:
            v_numbers =[0]
        c_numbers = range(0,int(images.sizes['c']))

        # first loop over channels
        for c_num in c_numbers:
            # then for every channel, look at every tile
            for v_num in v_numbers:
                # Make a directory for this particular c-v combinations
                # then for each tile, either take maxip:
                if maxIP:
                    # Take all z-stacks into a list of images
                    temp_image_stack = [images.get_frame_2D(c=c_num, v=v_num, z=j) for j in z_numbers]
                    temp_image = np.maximum.reduce(temp_image_stack)
                    io.imsave(os.path.join(out_dir, f"{nd2_filename_base}_channel{c_num+1}_tile{v_num+1}_maxIP.tif"), temp_image)
                # If no maxIP, then save all z-stacks seperately in yet another loop
                else:
                    for z_num in z_numbers:
                        temp_image = images.get_frame_2D(c=c_num, v=v_num, z=z_num)
                        io.imsave(os.path.join(out_dir, f"{nd2_filename_base}_channel{c_num+1}_tile{v_num+1}_z{z_num+1}.tif"), temp_image)
if __name__ == "__main__":
    filenames = glob("/media/sda1/thesis_data/spatial2/raw/*.nd2")
    out_dir = "/media/sda1/thesis_data/spatial2/raw/parsed/"
    for i, file in enumerate(filenames):
        parseND2toISS(file,out_dir, i, maxIP=False)

    
