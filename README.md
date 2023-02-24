# Shark_Spotting_w_YOLOv8
This repo contains scripts and tools for the training and use of YOLOv8 for detecting sharks in ariel drone footage.

## How To Run Training on a Remote Machine
### SSH into your desired computer 
```
ssh [USERNAME]@[HOST]
```
For example: if you are supposed to be here, 
USERNAME:calpoly_username HOST: 127x[2 digit computer number 01-11]

Enter 'yes' and your password when prompted

### Understand Local Storage
There are 2 locations on 127 machines that allow for local file storage:
- /mpac/      [True local storage, roughtly 2TB]
- /datasets/  [Shared by mpac machines, 1TB]
Navigate to one of these folders 
```
cd /mpac/
```
### Download the Repo
Now that you are in local storage, you can start downloading this repo!
Clone it and get in there!
```
git clone https://github.com/dylanjaybaxter/Shark_Spotting_w_YOLOv8.git
cd Shark_Spotting_w_YOLOv8
```

### Check Configuration
Before beginning, you may want to take a glance at config.yaml
It contains variable definitions for setup, training, and testing.
If you are running trainings, this is the file you will modify to change
hyperparameters between runs.
You can edit these paramters with:
```
vim config.yaml
```
or with your text editor of choice.

### Run user setup
In the main directory, source user_setup.sh using the following command:
```
. user_setup.sh [USERNAME]
```
Where username is you cal poly username. This script should download both the 
dependencies in the *python_dir* directory in config.yaml for training as well as 
the roboflow dataset defined by *roboflow_url* in the config.yaml file. 
PLEASE VERIFY THAT PYTHON_DIR IS IN MPAC. IF PACKAGES END UP IN USER STORAGE,
YOU MAY BE TEMPORARILY LOCKED OUT OF YOUR ACCOUNT. If this happens to you, request help
from Cal Poly ITS here: 
https://calpoly.atlassian.net/servicedesk/customer/user/login?destination=portals
They should reply fairly quickly during business hours.

### Run Training
Double check that your training parameters in config.yaml are what you expect. If you are
downloading this repo from master these settings should be the default for ultralytics at 1 epoch.
TODO: Add parameter description
Now that your configs are sorted, just run the training script!
```
sh train.sh
```
This should train for the specified number of epochs and output a final evaluation of the validation
data. Once this is done, the results can be found in the {Project}/{experiment} folder in this
repo defined by the project and experiment names in the config.yaml

### Test a Model on The Test Set
To test a model, make sure that the project and experiment to be tested are correctly outlined
in config.yaml. There are a few other parameters for this step too: 
TODO: Test Parameter Descriptions
to test, simply run test.sh.
```
sh test.sh
```

### Download the Model 
Now you have evaluated you model and are ready to download it to you local machine. To do this,
you can use the zip_n_download.sh. As a first step, clone this entire repo to your local machine
as well. Then from your LOCAL MACHINE, ssh into your desired remote computer with:
```
ssh [USERNAME]@[HOST]
```
Do this repeatedly until you are no longer prompted to accept a fingerprint.
Then modify config_dl.yaml for your specific user:
remote_host: [USERNAME]@[HOST]
remote_pass: [YOUR PASSWORD]
remote_folder: [THE FULL PATH TO THE PROJECT FOLDER ON REMOTE]
remote_exp: [REMOTE EXPERIMENT NAME]
local_folder: [LOCAL PATH TO SAVE THE FILE]
Then Run zip_n_download.sh and your folder should be downloaded as a zip archive to your local machine!
```
sh zip_n_download.sh
```
