# ND2 image reader

This directory contains a python script ("extract_nd2.py") that can be used as a command-line tool to extract specific (or all) images embedded in the raw .nd2 image file, which is the output of many NIKON microscopes.

It uses the python package *nd2reader* (https://github.com/rbnvrw/nd2reader) to open and slice the images.


## Usage


- Install nd2reader:
```bash
pip install nd2reader
```

- (optional) Read the input image first with the -r flag to verify everything works.
```bash
python extract_nd2.py path/to/input_image.nd2 -r
```

- Extract the target image slices.
```bash
python extract_nd2.py path/to/input_image.nd2   -o output/dir   \ 
                                                -c 0 1          \ 
                                                -v 0 1 2 3 4    \
                                                --maxIP         \
```

If you're not entirely certain how to use the different flags, consult the help entry:
```bash
python extract_nd2.py -h
```



