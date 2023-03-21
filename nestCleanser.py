'''
This Script is intended to remove nested directories that result from zipndownload
'''
# Imports
import os
import argparse

# Defaults for use as a script
dtgt = "C:\\Users\\dylan\\Documents\\Data\\YSP_Training_Results\\"

'''Function to add arguments'''
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tgt', type=str, default=dtgt, help='Path to dir to cleanse')
    return parser

'''Main function'''
def main_func(args):
    target_contents = os.listdir(args.tgt)
    for item in target_contents:
        if item != 'cleaned':
            end_path = os.path.join(args.tgt, item)
            if os.path.isdir(end_path):
                while(True):
                    dir_list = os.listdir(end_path)
                    if (len(dir_list) == 1):
                        if os.path.isdir(os.path.join(end_path, dir_list[0])):
                            inspected_folder = dir_list[0]
                            end_path = os.path.join(end_path, inspected_folder)
                    elif(len(dir_list) > 1 and item != 'zipped' and item != 'cleaned'):
                        if not os.path.exists(os.path.join(args.tgt, "cleaned", inspected_folder)):
                            os.rename(end_path, os.path.join(args.tgt, "cleaned", inspected_folder))
                        break
                        #os.remove(os.path.join(args.tgt, item))
                    else:
                        break
    print("Done!")

# ********************UNUSED***********************
def collapse_dir(dir_path):
    dir_list = os.listdir(dir_path)
    if (len(dir_list) == 1):
        if os.path.isdir(os.path.join(dir_path, dir_list[0])):
            # Move item to target dir
            gp = os.path.dirname(dir_path)
            os.rename(os.path.join(dir_path, dir_list[0]), os.path.join(gp, dir_list[0]))
            os.remove(dir_path)
            collapse_dir(os.path.join(gp, dir_list[0]))

if __name__ == '__main__':
    args = init_parser().parse_args()
    print(args)
    main_func(args)