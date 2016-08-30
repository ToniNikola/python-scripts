#!/usr/bin/env python3

import subprocess
import time
import shutil
import errno
import os
import datetime

drivename_folders = [("DIKTAFON", "RECORDER/FOLDER_A/")]

def get_mountedlist():
    return [item[item.find("/"):] for item in subprocess.check_output(
            ["/bin/bash", "-c", "lsblk"]).decode("utf-8").split("\n") if "/" in item]


done = []

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

flag = True
while flag:
    mounted = get_mountedlist()
    new_paths = [dev for dev in mounted if not dev in done]
    valid = sum([[(drive, drive+"/"+item[1], item[0]) for drive in new_paths \
                  if item[0] in drive] for item in drivename_folders], [])

    
    
    if valid:

        src = valid[0][1]
        dst = '/home/lynx/Desktop/Diktafon'

    
        now = datetime.datetime.now()
        newDirName = now.strftime("%Y_%m_%d-%H%M")
            
        new_dst =  os.path.join(dst, newDirName)

        os.mkdir(new_dst)

        for file in os.listdir(src):
        
            src_file = os.path.join(src, file)
            dst_file = os.path.join(new_dst, file)
            shutil.move(src_file, dst_file)
        

        #shutil.move(new_src,new_dst)
        print("Moved")
        flag = False    
    else:
        print('No Mount points...')
        flag = False
    time.sleep(2)
