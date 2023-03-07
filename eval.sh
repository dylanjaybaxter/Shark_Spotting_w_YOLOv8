#!/bash/bin/

# Get evaluation parameters
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

pwd
eval $(parse_yaml config.yaml)

# Create a Copy of data.yaml for evaluating the test data
cd ${test_data_dir}
data_path=$(pwd)
newfile="data_test.yaml"
if [ -e $newfile ]; then
    echo "Test Data Found."
fi
field="val"
new_value="${data_path}/test/images"
file_contents=$(cat data.yaml)

# Replace the old value with the new value
new_contents="$(echo "$file_contents" | sed -e "s@^${field}:.*@${field}: ${new_value}@")"

echo "$new_contents"
# Write the new contents back to the file
echo "$new_contents" > $newfile
cd ..

# Create file paths for model and project
exp_test_folder="${experiment_test}_test"
project_test_folder="${project_test}_test"
model_path="./${project_test}/${experiment_test}/weights/best.pt"


# Run the evaluation with parameters
yolo task=detect \
  mode=val \
  project=${project_test_folder} \
  name=${exp_test_folder} \
  model=${model_path} \
  data="datasets/${newfile}" \
  save_json=${save_json} \
  iou=${iou} \
  conf=${confidence} 2>&1 | tee output.txt

  mv output.txt ${project_test_folder}/${exp_test_folder}/


