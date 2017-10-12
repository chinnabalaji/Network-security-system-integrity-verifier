# -*- coding: utf-8 -*-

import sys
from time import sleep
import os
import grp
import pwd
import time
import hashlib
import time

start_time = time.time()
try:                               #creates history.txt file if not exists
  f=open("history.txt","r")
  f.close()
except:
  f=open("history.txt","w")
  f.close()

f=open("history.txt","r")         #finding no.of lines in the file to write monitored directories in an order
lines=f.readlines()
lastid=len(lines)+1
f.close()

def directory_exists(directory):  #checks if directory exists or not?
    if(os.path.isdir(directory)):
      return True
    else:
      return False
def inputfile_directory(user_file): #checks if the directory of report or verification file exists or not?
    file_split=user_file.split('/')
    length=len(file_split)
    last=length-1
    filedir=""
    for i in range(1,last):
        filedir=filedir+"/"+file_split[i]
    filedir=filedir+"/"
    if(os.path.isdir(filedir)):
      return True
    else:
      return False
