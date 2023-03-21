'''
This Script is intended to convert datasets of synthetic sharks into yolo compatible datasets
'''
# Imports
import pandas as pd
import argparse
import re
import cv2 as cv
import os
from os import path
import shutil
from math import floor


# Defaults for use as a script

dimloc = "C:\\Users\\dylan\\Documents\\Data\\Shark_Spotting\\synthetic_batch_2_raw\\MacEditor\\"
dcsv = "C:\\Users\\dylan\\Documents\\Data\\Shark_Spotting\\synthetic_batch_2_raw\\MacEditor\\output.csv"
dsave_dir = "C:\\Users\\dylan\\Documents\\Data\\Shark_Spotting\\"
dname = "synthetic_batch_2_roboflow"
dformat = "roboflow" # 'local', 'roboflow'
SHARK_LABEL = 3
MAX_EXTRACTIONS = 1000

'''Function to add arguments'''
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ims', type=str, default=dimloc, help='Path to images')
    parser.add_argument('--csv', type=str, default=dcsv, help='Path to csv')
    parser.add_argument('--save_dir', type=str, default=dsave_dir, help='Save Path')
    parser.add_argument('--name', type=str, default=dname, help='Name of output folder')
    parser.add_argument('--format', type=str, default=dformat, help='Name of output folder')
    return parser

'''Main function'''
def main_func(args):
    # Read in csv data
    data = pd.read_csv(args.csv, header=None)

    # Read in only bbox data
    data = data.iloc[1]

    # Create file structure
    dest_path = path.join(args.save_dir, args.name)
    im_path = path.join(dest_path, "images")
    lb_path = path.join(dest_path, "labels")
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    if not path.exists(im_path):
        os.mkdir(im_path)
    if not path.exists(lb_path):
        os.mkdir(lb_path)


    # For each row, extract bounding box data and save data to text file
    for index, bbox_string in data.items():
        # Find Image Dimensions
        mat = cv.imread(path.join(args.ims, str(index)+".png"))
        im_h = mat.shape[0]
        im_w = mat.shape[1]

        # Extract bbox information
        nums = re.findall(r"\d+\.\d+", bbox_string)
        x1,y1,x2,y2 = (float(i) for i in nums)
        x1 = max(min(x1, im_w), 0)
        x2 = max(min(x2, im_w), 0)
        y1 = max(min(y1, im_h), 0)
        y2 = max(min(y2, im_h), 0)
        w = abs(x2-x1)
        h = abs(y2-y1)
        cx = max(x2,x1)-(w/2)
        cy = max(y2,y1)-(h/2)

        # Show Results with Box
        cv.rectangle(mat, (floor(x1), floor(y1)), (floor(x2), floor(y2)), (0, 255, 0), 2)
        cv.imshow("Bbox Check", mat)
        cv.waitKey(1)

        # Normalize values by im dimensions and save to file
        if (args.format == 'local'):
            with open(path.join(lb_path, str(index)+".txt"), 'w') as file:
                file.write(f"{str(SHARK_LABEL)} {str(x1/im_w)} {str(y1/im_h)} {str(w/im_w)} {str(h/im_h)}")
        elif (args.format == 'roboflow'):
            with open(path.join(lb_path, str(index)+".txt"), 'w') as file:
                file.write(f"{str(SHARK_LABEL)} {str(cx/im_w)} {str(cy/im_h)} {str(w/im_w)} {str(h/im_h)}")

        # Copy matching image to images folder
        shutil.copy(path.join(args.ims, str(index)+".png"), path.join(im_path, str(index)+".png"))

        print(f"Processed file {index}.png")
        if index==MAX_EXTRACTIONS:
            break

    print("Done!")


if __name__ == '__main__':
    args =  init_parser().parse_args()
    print(args)
    main_func(args)
