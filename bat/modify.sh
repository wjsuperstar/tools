#!/bin/sh

MYROOT_PATH=$(pwd)

for dir_name in $(ls ${MYROOT_PATH});
do
    
    if [ -d $dir_name ];then
        echo $dir_name
        sed -i '/s/FotonAppPub FotonAdk\"/ant\"' 30*/list.env
        
    fi
done

