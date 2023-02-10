# -*- coding: utf-8 -*-
"""YOLOv8_4_Sharks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XMcxB0KUiUA1XCJcjvUZyA3m917I1IBC

# CSC 487 - Training And Evalutating Shark Detection and Localization with YOLOv8
This notebook contains code for training and evaluation of YOLOv8 on the Marine Science dataset. This notebook is meant to be run IN ORDER. If you run it in some reasonable sequence and a variable is missing, please leave a comment so the notebook can be made comprehensive.

## Environment Setup
First, lets install the ultralytics python package and it's requirements for training. As well as the roboflow api for getting our data.
"""

!pip install ultralytics
!pip install roboflow
!pip install utils
!pip install wandb

"""## Checking The Environment has a GPU
We're gonna need a GPU to do training. Let's make sure that it's avaliable
"""

import torch #For Checking the Card
from IPython.display import Image  # for displaying images
import utils # for downloading models/datasets
# Show Card
print('torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

"""## Download the Dataset
Next we'll download our dataset from the roboflow api
"""

# Commented out IPython magic to ensure Python compatibility.
from roboflow import Roboflow
# Create a datasets folder and move to it
# %cd /content/
# %mkdir datasets/
# %cd /content/datasets/

# Download the dataset from the roboflow api
rf = Roboflow(api_key="33STfIOAKtux13HpH7Tf")
project = rf.workspace("d4ms").project("marinescience")
dataset = project.version(2).download("yolov8")

# Navigate to the dataset directory itself
# %cd /content/datasets/marinescience-2/

"""## Training the Model
Now that we have the dataset, lets get started training. First, we need to load a pretrained model from the ultralytics API.
"""

from ultralytics import YOLO
pretrained = True #@param {type:"boolean"}
model = "yolov8n" #@param ["yolov8s", "yolov8m", "yolov8l", "yolov8x", "yolov8n"]
print("Loading {}...".format(model))
# Load a model
model = YOLO(model+".pt")  # load a pretrained model

"""Now we can use the ultralytics CLI for model training to fine tune the model with the downloaded dataset."""

# Commented out IPython magic to ensure Python compatibility.
# %cp /content/datasets/marinescience-2/data.yaml ./

#@title Hyperparameters & Training
project = "YSP"#@param {type:"string"}
experiment_name = "TPU_Run"#@param {type:"string"}
data_dir = "/content/datasets/data.yaml"#@param {type:"string"}
batch =  16#@param {type:"integer"}
epochs =  50#@param {type:"integer"}
patience =  25#@param {type:"integer"}
im_size = 640 #@param ["416", "640", "1280"] {type:"raw"}

# Print the command for debugging
!echo task=detect \
  mode=train \
  model=yolov8n.pt \
  project={project} \
  name={experiment_name} \
  data={data_dir} \
  epochs={epochs} \
  imgsz={im_size} \
  batch={batch} \
  patience={patience}

# Execute the command
!yolo task=detect \
  mode=train \
  model=yolov8n.pt \
  project={project} \
  name={experiment_name} \
  data={data_dir} \
  epochs={epochs} \
  imgsz={im_size} \
  batch={batch} \
  patience={patience}

"""Save the training results"""

# Mount your google drive to the colab notebook
from google.colab import drive
drive.mount('/content/drive')

# Zip and Download results to 
# Zip Training Results
import os
results_path = os.path.join("/content/datasets/marinescience-2/",project,experiment_name)
zip_path = "/content/"+experiment_name+".zip"
!echo -r {zip_path} {results_path}
!zip -r {zip_path} {results_path}

#Download Results
from google.colab import files
files.download(zip_path)

"""# Visualize Training Results in TensorBoard"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir {project}/

"""# Visualize Training Results and Data"""

import glob
from IPython.display import Image, display

#@title Metrics 
file_inspect = "results.png" #@param ["results.png", "F1_curve.png","PR_curve.png","P_Curve.png","R_Curve.png","confusion_matrix.png", "results.png"] {type:"string"}
Image(filename=os.path.join(results_path, file_inspect), width=1000)

#@title Training Image Output
file_inspect = "train_batch0.jpg" #@param ["train_batch0.jpg","train_batch1.jpg","train_batch2.jpg"] {type:"string"}
Image(filename=os.path.join(results_path, file_inspect), width=1000)

#@title Validation Image Output
file_inspect = "val_batch0" #@param ["val_batch0","val_batch1","val_batch2"] {type:"string"}
print("1. PREDICTION")
im_pred = Image(filename=os.path.join(results_path, file_inspect+"_pred.jpg"), width=1000)
print("2. LABEL")
im_label = Image(filename=os.path.join(results_path, file_inspect+"_labels.jpg"), width=1000)
display(im_pred, im_label)

"""# Evaluate Model on Test Set"""

#@title Create a Trick dataset 
#@markdown This will create a new data.yaml file that will allow for the extraction of evaluation metrics on the test set 
import yaml
datafile = "/content/datasets/marinescience-2/data.yaml"
dataTest = "/content/datasets/marinescience-2/dataTest.yaml"

with open(datafile, "r") as stream:
    data = yaml.safe_load(stream)

print(data)
data["val"] = "marinescience-2/test/images"

with open(dataTest, "w") as stream:
    yaml.dump(data, stream)

#@title Evaluate the Model on the Test Set
confidence = 0.001 #@param {type:"number"}
iou = 0.6 #@param {type:"number"}
save_json = True #@param {type:"boolean"}

model_path = os.path.join(results_path,"weights/best.pt")
project_test = project+"_test"
exp_name_test = experiment_name+"_test"

!yolo task=detect \
  mode=val \
  project = {project_test} \
  name = {exp_name_test} \
  model={model_path} \
  data={dataset.location}/dataTest.yaml \
  save_json=True \
  iou={iou}

"""# Visualize Test Set Results"""

#@title Test Metrics 
test_path = os.path.join("/content/datasets/marinescience-2/", project_test, exp_name_test)
file_inspect = "confusion_matrix.png" #@param ["F1_curve.png","PR_curve.png","P_Curve.png","R_Curve.png","confusion_matrix.png"] {type:"string"}
Image(filename=os.path.join(test_path, file_inspect), width=1000)

#@title Test Image Output
file_inspect = "val_batch0" #@param ["val_batch0","val_batch1","val_batch2"] {type:"string"}
print("1. PREDICTION")
im_pred = Image(filename=os.path.join(test_path, file_inspect+"_pred.jpg"), width=1000)
print("2. LABEL")
im_label = Image(filename=os.path.join(test_path, file_inspect+"_labels.jpg"), width=1000)
display(im_pred, im_label)

"""# Evaluating the Resulting Model on Validation Set
After training, we'll evaluate the model on our validation set using the ultralytics CLI to get a more detailed 
"""

confidence = 0.001 #@param {type:"number"}
iou = 0.6 #@param {type:"number"}
save_json = True #@param {type:"boolean"}

model_path = os.path.join(results_path,"weights/best.pt")
val_path = os.path.join("/content/datasets/marinescience-2/", project+"_val", experiment_name+"_val")

!yolo task=detect \
  mode=val \
  model={model_path} \
  data={dataset.location}/data.yaml \
  save_json=True \
  iou={iou}