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
try:                                         #creates history.txt file if not exists
  f=open("history.txt","r")
  f.close()
except:
  f=open("history.txt","w")
  f.close()

f=open("history.txt","r")                   #finding no.of lines in the file to write monitored directories in an order
lines=f.readlines()
lastid=len(lines)+1
f.close()

def directory_exists(directory):            #checks if directory exists or not?
    if(os.path.isdir(directory)):
      return True
    else:
      return False
def inputfile_directory(user_file):         #checks if the directory of report or verification file exists or not?
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
    
    def fileout_mondir(user_file,mon_dir):    #checks if report or verification file is outside monitored directory or not?
    if mon_dir in user_file:
      return False
    else:
      return True
    
def file_exists(filename):                    #checks if report or verification file already exists or not?
    if(os.path.isfile(filename)):
      return True
    else:
      return False

def userowner(path):                          #returns owner of the file or directory
  stat_info = os.stat(path)
  uid = stat_info.st_uid
  user = pwd.getpwuid(uid)[0]
  return user

def groupowner(path):                        #returns group owner of the file or directory
  stat_info = os.stat(path)
  gid = stat_info.st_gid
  group = grp.getgrgid(gid)[0]
  return group

def getFileSize(name):                         #returns file size
   path_size=os.path.getsize(name)
   return path_size

def getFolderSize(folder):                    #returns directory size
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if(os.path.isfile(itempath)):
            total_size += os.path.getsize(itempath)
        elif(os.path.isdir(itempath)):
            total_size += getFolderSize(itempath)
        else:
          pass
       
    return total_size
  
  def modifiedtime(path): #returns last modified time for files or directories
    mtime=time.ctime(os.path.getmtime(path))
    return mtime

def permissions(path): #returns octet permissions for files or directories
    file_permissions=(os.stat(path).st_mode) 
    return file_permissions

def hashoutput(fname,hash_value): # returns hash values of files only, hash doesn't exists for directories 
    if(hash_value=="sha1"):
      hash_sha1 = hashlib.sha1()
      with open(fname, "rb") as f:
         for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
      return hash_sha1.hexdigest()
    elif(hash_value=="md5"):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
           for chunk in iter(lambda: f.read(4096), b""):
              hash_md5.update(chunk)
        return hash_md5.hexdigest()
    else:
       pass

def history_mon_dir(mon_dir): #checks if initialization mode is done for a directory or not?
   h=open("history.txt","r")
   num=[]
   for line in h:
      if mon_dir in line:
         line_split=line.split('.')
         mon_dir_num=line_split[0]
         num.append(mon_dir_num)
   h.close()
   if(len(num)!=0):
     return True  ##### some things exists if not equal to zero
   else:
     return False ##### nothing exists in num because it is equal to zero
 
def max_mon_dir(mon_dir): #returns the latest details of initialization mode for a monitored directory!
   h=open("history.txt","r")
   num=[]
   for line in h:
     if mon_dir in line:
        line_split=line.split('.')
        mon_dir_num=line_split[0]
        num.append(mon_dir_num)
   h.close()
   return max(num)
     
def check_vfiles(verify_vfile,init_vfile):#checks if v_file entered in i_mode is same as that entered in v_mode for a monitored_d?
   if(verify_vfile==init_vfile):
     return True
   else:
     return False
