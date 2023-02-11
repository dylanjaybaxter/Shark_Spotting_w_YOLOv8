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

# Run the Training Script
yolo task=detect \
  mode=train \
  model=$model \
  project=$project_train \
  name=$experiment_train \
  data=$data_dir \
  epochs=$epochs \
  imgsz=$im_size \
  batch=$batch \
  patience=$patience \
  device=$device 2>&1 


# Zip the Training Data For Later
echo "Zipping up..."
zip -r ./${project_train}/${experiment_train}.zip ./${project_train}/${experiment_train}/