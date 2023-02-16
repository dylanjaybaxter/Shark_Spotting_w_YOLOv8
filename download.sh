#!/bin/bash/

# This file is to be run on a local machine to zip and download a folder from a host

# Read parameters from config
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

eval $(parse_yaml dl_config.yaml)

echo "sshpass -p ${remote_pass} scp ${remote_user}@${remote_host}:${remote_folder}/${remote_exp}.zip ${local_folder}"

# SSH into the host machine
sshpass -p ${remote_pass} scp ${remote_user}@${remote_host}:${remote_folder}/${remote_exp}.zip ${local_folder}
