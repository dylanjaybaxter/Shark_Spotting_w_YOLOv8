# !/bin/bash

# Argument Setup: https://stackoverflow.com/questions/5014632/how-can-i-parse-a-yaml-file-from-a-linux-shell-script
parse_yaml() {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

eval $(parse_yaml config.yaml)
echo $model

# Download the dataset

if [ ! -d "./datasets" ]; then
    mkdir datasets/
    cd datasets/
    curl -L "https://app.roboflow.com/ds/WXhb7XSaNb?key=B7P99J5E8P" > roboflow.zip
    unzip roboflow.zip
    rm roboflow.zip
    cd ../
else
  # Command(s) to run if the directory exists
  echo "Directory ./datasets already exists."
fi

# Download Python dependencies
check_python_package() {
  local package_name=$1
  python3 -c "import $package_name" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "The package '$package_name' is not installed."
    python3 pip install -m $package_name
  else
    echo "The package '$package_name' is installed."
  fi
}

check_python_package "ultralytics"
check_python_package "roboflow"
check_python_package "utils" 

# Run the Training Script
yolo task=detect \
  mode=train \
  model=$model \
  project=$project \
  name=$experiment_name \
  data=$data_dir \
  epochs=$epochs \
  imgsz=$im_size \
  batch=$batch \
  patience=$patience \
  device=$device