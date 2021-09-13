import numpy as np
import aicspylibczi
import pathlib
import os
from PIL import Image
from icecream import ic
from skimage import io

mosaic_file_list = [pathlib.Path(f"/media/tool/gabriele_data/170315_161220_hippo_4_1/170315_161220_hippo_b{i}.czi") for i in range(1,6)]
# order = nuclei, DO, T, G, C, A
def maxIPstack(img_list):
    parsed_list = img_list
    parsed_list = [img if isinstance(img, np.ndarray) else io.imread(img) for img in img_list]
    # now all elements in parsed_list are ndarrays
    maxIP = np.maximum.reduce(parsed_list)
    return maxIP

def writeMozaicImages(filePath="", channel_nr=None, z_stack_nr=None, czi_image=None, output_dir=""):
    # Checking if args were filledi n correctly
    if not filePath and czi_image is None:
        print("No filepath or czi image was supplied, so the function cannot perform anything.")
        return
    if filePath and czi_image is not None:
        print("Filepath and czi image cannot both be supplied as arguments.")
        return
    
    if filePath:
        czi = aicspylibczi.CziFile(filePath)
        if not czi.is_mosaic():
            print("Given file is not a mosaic file.")
            return
        if z_stack_nr is not None and channel_nr is not None:
            mosaic_data = czi.read_mosaic(C=channel_nr, Z=z_stack_nr, scale_factor=1)
    
    else:
        if not czi_image.is_mosaic():
            print("Given file is not a mosaic file.")
            return
        if z_stack_nr is not None and channel_nr is not None:
            
            channel_index = channel_nr-1
            z_stack_index = z_stack_nr-1
            mosaic_data = czi_image.read_mosaic(C=channel_index, Z=z_stack_index, scale_factor=1)
            mosaic_data = mosaic_data[0,0,:,:].astype(np.uint16)
            img = Image.fromarray(mosaic_data)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            output_filename= os.path.join(output_dir, f"channel{channel_nr}_z-stack{z_stack_nr}.tif")
            img.save(output_filename)
            print(f"Extracted channel {channel_nr}: z-stack {z_stack_nr} from original image to {output_filename}.")
        elif channel_nr is not None:
             # Here we want maxIP of a certain channel

            channel_index = channel_nr-1 # Indexing in czi api is 0 based, but user will be thinking in 1 based indexing.
           
            z_stack_min, z_stack_max = czi_image.dims_shape()[0]['Z'] #unpack the necessary 
            image_list = []
            for i in range(z_stack_min, z_stack_max):
                mosaic_data = czi_image.read_mosaic(C=channel_index, Z=i, scale_factor=1)
                mosaic_data = mosaic_data[0,0,:,:].astype(np.uint16)

                image_list.append(mosaic_data)
            maxIP = maxIPstack(image_list)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            output_filename= os.path.join(output_dir, f"channel_{channel_nr}_maxIP.tif")
            io.imsave(output_filename, maxIP, check_contrast=False)
            print(f"Wrote z-stack-maxIP of channel {channel_nr} to {output_filename}")


czi = aicspylibczi.CziFile("/media/tool/gabriele_data/170315_161220_hippo_4_1/170315_161220_hippo_b5.czi/")
c_stack_min, c_stack_max = czi.dims_shape()[0]['C']
for i in range(c_stack_min+1, c_stack_max+1): # I want them named starting at 1, not at 0
    writeMozaicImages(czi_image = czi, channel_nr=i, output_dir=f"/media/tool/gabriele_data/170315_161220_hippo_4_1/maxIP_seperate_channels/Round5/")
# for index, round_img in enumerate(mosaic_file_list):
#     czi = aicspylibczi.CziFile(round_img)
#     c_stack_min, c_stack_max = czi.dims_shape()[0]['C']
#     for i in range(c_stack_min+1, c_stack_max+1): # I want them named starting at 1, not at 0
#         writeMozaicImages(czi_image=czi, channel_nr=i, output_dir=f"/media/tool/gabriele_data/170315_161220_hippo_4_1/maxIP_seperate_channels/Round{index+1}/")

