'''
This Script is intended to convert datasets of synthetic sharks into yolo compatible datasets
'''
# Imports
from ultralytics import YOLO
import torch
import argparse


# Defaults for use as a script
dsrc = "C:\\Users\\dylan\\Documents\\Data\\YSP_Training_Results\\default_100_epochs\\YSP\\default_100_epochs\\weights\\best.pt"
ddest = "C:\\Users\\dylan\\Documents\\Data\\YSP_Training_Results\\onnx\\shark.onnx"

'''Function to add arguments'''
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, default=dsrc, help='Path to pytorch')
    parser.add_argument('--dest', type=str, default=ddest, help='Path to save')
    return parser

'''Main function'''
def main_func(args):
    model = torch.load(args.src)
    model.export(format="onnx", imgsz=[640,640])
    # Export the model
    '''x = torch.randn(1, 3, 640, 640, requires_grad=True)
    model = model(x)
    torch.onnx.export(model,  # model being run
                      x,  # model input (or a tuple for multiple inputs)
                      "super_resolution.onnx",  # where to save the model (can be a file or file-like object)
                      export_params=True,  # store the trained parameter weights inside the model file
                      opset_version=10,  # the ONNX version to export the model to
                      do_constant_folding=True,  # whether to execute constant folding for optimization
                      input_names=['input'],  # the model's input names
                      output_names=['numDet'],  # the model's output names
                      dynamic_axes={'input': {0: 'batch_size'},  # variable length axes
                                    'output': {0: 'batch_size'}})'''
    print("Done!")


if __name__ == '__main__':
    args =  init_parser().parse_args()
    print(args)
    main_func(args)
