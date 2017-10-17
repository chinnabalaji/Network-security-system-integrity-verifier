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
  
  def modifiedtime(path):                      #returns last modified time for files or directories
    mtime=time.ctime(os.path.getmtime(path))
    return mtime

def permissions(path):                         #returns octet permissions for files or directories
    file_permissions=(os.stat(path).st_mode) 
    return file_permissions

def hashoutput(fname,hash_value):              # returns hash values of files only, hash doesn't exists for directories 
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

def history_mon_dir(mon_dir):                  #checks if initialization mode is done for a directory or not?
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
 
def max_mon_dir(mon_dir):                  #returns the latest details of initialization mode for a monitored directory!
   h=open("history.txt","r")
   num=[]
   for line in h:
     if mon_dir in line:
        line_split=line.split('.')
        mon_dir_num=line_split[0]
        num.append(mon_dir_num)
   h.close()
   return max(num)
     
def check_vfiles(verify_vfile,init_vfile):   #checks if v_file entered in i_mode is same as that entered in v_mode for a monitored_d?
   if(verify_vfile==init_vfile):
     return True
   else:
     return False

  
  sleep(1)
length_arguments=len(sys.argv)

if(sys.argv[1]=='-h' or sys.argv[1]=='--h'):
  print "\tEnter the input as follows ..."
  sleep(1)
  print "\tpython siv.py <-i|-v|-h> –D <monitored_directory> -V <verification_file> -R <report_file> -H <hash_function>"
  sleep(1)
  print "\tHash functions supported are md5 and sha1 ..."
  sys.exit()

elif(sys.argv[1]=='-i'):
    if(length_arguments==10):
      if(sys.argv[1]=='-i' and sys.argv[2]=='-D' and sys.argv[4]=='-V' and sys.argv[6]=='-R' and sys.argv[8]=='-H'):
        print "\tInitialization mode running ..."
        sleep(1)
        
        mon_dir=sys.argv[3]
        while not(directory_exists(mon_dir)): #loops untill user enters a valid directory
             mon_dir=raw_input("\tPlease enter a valid directory:")
        else:
          print "\tMonitored directory exists!"
          sleep(1)
        
        init_vfile=sys.argv[5]
        init_rfile=sys.argv[7]
        hash_value=sys.argv[9]
 
        init_rfile=init_rfile+".txt"  ## report file will be converted to text format here

        
        dir_count=0
        file_count=0
        
        w=open("history.txt","a")
        w.write('%s.%s:%s,%s,%s'%(lastid,mon_dir,hash_value,init_rfile,init_vfile)+"\n")
        w.close()
        
        ########################################### checks the directory of verification file
        
        while not(inputfile_directory(init_vfile)):
            init_vfile=raw_input("\tVerification file's directory is not valid, please enter the file path again:")
        else:
           pass
        
        ############################################## checks if ther verification file is outside monitored directory?
        
        while not(fileout_mondir(init_vfile,mon_dir)):
            init_vfile=raw_input("\tPlease enter verification file outside monitored directory:")
        else:
          print "\tVerification file is outside monitored directory ..."
          sleep(1)
        
        ########################################### checks the directory of report file?
        
        while not(inputfile_directory(init_rfile)):
            init_rfile=raw_input("\tReport file's directory is not valid, please enter the path again:")
        else:
           pass
        
        ############################################## checks if the report file is outside monitored directory?
        
        while not(fileout_mondir(init_rfile,mon_dir)):
            init_rfile=raw_input("\tPlease enter report file outside monitored directory:")
        else:
          print "\tReport file is outside monitored directory ..."
          sleep(1)
        
        ############################ checks if the verification file exists or not?
        
        if(file_exists(init_vfile)):
          answer=raw_input("\tVerification file exists already, do you want to overwrite it? y/n ")
          answer=answer.lower()
          while not(answer=='y' or answer=='n'):
             answer=raw_input("\tVerification file exists already, do you want to overwrite it? y/n ")
             answer=answer.lower()
          else:
            if(answer=='y'):
              i=open(init_vfile,"w")
              i.close()
            else:
              sleep(1)
              print"\tProgram is terminated ..."
              sys.exit()
        
        ############################ checks if the report file exists or not?
        
        if(file_exists(init_rfile)):
          answer=raw_input("\tReport file exists already, do you want to overwrite it? y/n ")
          answer=answer.lower()
          while not(answer=='y' or answer=='n'):
             answer=raw_input("Report file exists already, do you want to overwrite it? y/n ")
             answer=answer.lower()
          else:
            if(answer=='y'):
              r=open(init_rfile,"w")
              r.close()
            else:
              sleep(1)
              print"\tProgram is terminated ..."
              sys.exit()
        
        #################################################### code for the values of the files/directories
        
        for dirname, dirnames, filenames in os.walk(mon_dir):
           for subdirname in dirnames:
              dir_count=dir_count+1
              directory_name=(os.path.join(dirname, subdirname))
              with open(init_vfile, "a") as myfile:
                   myfile.write('%s,%s,%s,%s,%s,%s'%(directory_name,getFolderSize(directory_name),userowner(directory_name),groupowner(directory_name),permissions(directory_name),modifiedtime(directory_name))+"\n")
           for filename in filenames:
              file_count=file_count+1
              file_name=(os.path.join(dirname, filename))
              with open(init_vfile, "a") as myfile:
                   myfile.write('%s,%s,%s,%s,%s,%s,%s'%(file_name,getFileSize(file_name),userowner(file_name),groupowner(file_name),permissions(file_name),modifiedtime(file_name),hashoutput(file_name,hash_value))+"\n")

                  
                  ################################################## writing to report file initialization mode
        
        r=open(init_rfile,"a")
        r.write('Full pathname to monitored directory:%s'%(mon_dir)+"\n")
        r.write('Full pathname to verification file:%s'%(init_vfile)+"\n")
        r.write('Number of directories parsed:%s'%(dir_count)+"\n")
        r.write('Number of files parsed:%s'%(file_count)+"\n")
        print "\tInitialization mode completed successfully!"
        sleep(1)
        r.write('Time to complete initialization mode:%s'%(time.time()-start_time)+"\n")
        r.close()
         
      else: #this else is to check if elements -i -D -V -H are correct or not
        print "Enter \'python siv.py -h\' for help ... "
    else: #this else is to check if length_arguments!=10
      print "Enter \'python siv.py -h\' for help ... "
      sleep(1)
      
###############################################################################################################################################

elif(sys.argv[1]=='-v'):
    if(length_arguments==8): ######## no need of hash function
      if(sys.argv[1]=='-v' and sys.argv[2]=='-D' and sys.argv[4]=='-V' and sys.argv[6]=='-R'):
         print "\tVerification mode running ..." #verfication mode
         sleep(1)
         
         mon_dir=sys.argv[3]

         while not (history_mon_dir(mon_dir)):  #checks history.txt file to see if mon_dir exists or not
            mon_dir=raw_input("\tPlease enter the directory in which initialization mode is completed:")
         else:
           while not(directory_exists(mon_dir)):    ########### bug, in the history file original directory will be as it is, but after that if user deletes that directory it asks for another valid directory, it won't check if it exists in the history or not
              mon_dir=raw_input("\tPlease enter a valid directory:")
           else:
             print "\tMonitored directory exists!"
             sleep(1)

         verify_vfile=sys.argv[5]
         verify_rfile=sys.argv[7] 
         verify_rfile=verify_rfile+".txt"

         num=int(max_mon_dir(mon_dir))-1
         h=open("history.txt")
         updated_dir=h.readlines()[num]
         updated_dir_split=updated_dir.split(':')
         all_init_values_split=updated_dir_split[1].split('\n')
         all_init_values=all_init_values_split[0]
         all_init_values_final_split=all_init_values.split(',')
         hash_value=all_init_values_final_split[0]
         init_vfile=all_init_values_final_split[2]
         init_rfile=all_init_values_final_split[1] 
         h.close()         
         
         ################################################# checks history and tells if you entered correct verification file or not 
         
         while not (check_vfiles(verify_vfile,init_vfile)):
            verify_vfile=raw_input("\tEnter correct verification file for the corresponding monitored directory:")
         else:
           pass
         
         ############################## checking if the verification file exists or not

         if(file_exists(verify_vfile)):
           print "\tVerification file exists, parsing the file ..."
           sleep(1)
         else:
           print "\tVerification file does not exist, please run the initialization mode again!"
           sleep(1)
           print "\tVerification mode is terminating ..."
           sleep(1)
           sys.exit()
           
         ############################################## checks if the verification file is outside monitored directory?
         
         while not(fileout_mondir(verify_vfile,mon_dir)):
             verify_vfile=raw_input("\tPlease enter verification file outside monitored directory:")
         else:
           print "\tVerification file is outside monitored directory ..."
           sleep(1)

         ############################################# checks the directory of report file?
         
         while not(inputfile_directory(verify_rfile)):
            verify_rfile=raw_input("\tReport file's directory is not valid, please enter the path again:")
         else:
           pass

         ################################################ checks if the report file is outside monitored directory?
         
         while not(fileout_mondir(verify_rfile,mon_dir)):
            verify_rfile=raw_input("\tPlease enter report file outside monitored directory:")
         else:
           print "\tReport file is outside monitored directory ..."
           sleep(1)
         
         ################################## checks if the report file exists or not
         if(file_exists(verify_rfile)):
           answer=raw_input("\tReport file exists already, do you want to overwrite it? y/n ")
           answer=answer.lower()
           while not(answer=='y' or answer=='n'):
             answer=raw_input("\tReport file exists already, do you want to overwrite it? y/n ")
             answer=answer.lower()
           else:
             if(answer=='y'):
               r=open(verify_rfile,"w")
               r.close()
             else:
               sleep(1)
               print"\tProgram is terminated ..."
               sys.exit()
         
         #################################################### code for the values of the files/directories
         
         v=open("secret.txt","w")
         v.close()
         
         dir_count_v=0
         file_count_v=0

         for dirname, dirnames, filenames in os.walk(mon_dir):
            for subdirname in dirnames:
               dir_count_v=dir_count_v+1
               directory_name=(os.path.join(dirname, subdirname))
               with open("secret.txt", "a") as myfile:
                    myfile.write('%s,%s,%s,%s,%s,%s'%(directory_name,getFolderSize(directory_name),userowner(directory_name),groupowner(directory_name),permissions(directory_name),modifiedtime(directory_name))+"\n")
            for filename in filenames:
               file_count_v=file_count_v+1
               file_name=(os.path.join(dirname, filename))
               with open("secret.txt", "a") as myfile:
                    myfile.write('%s,%s,%s,%s,%s,%s,%s'%(file_name,getFileSize(file_name),userowner(file_name),groupowner(file_name),permissions(file_name),modifiedtime(file_name),hashoutput(file_name,hash_value))+"\n")  
         
 #################### 1(a) Newfiles ####################
         new_count_dir=0
         new_count_file=0
         v=open("secret.txt","r")
         newdir=[]
         newfiles=[]
         intialization_data=[]
         i=open(verify_vfile,"r")
         for line in i:
            line_split_i=line.split(',')
            pathname_i=line_split_i[0]
            intialization_data.append(pathname_i)
         i.close()
         for line in v:
            line_split_v=line.split(',')
            pathname_v=line_split_v[0]
            if pathname_v not in intialization_data:
               if(directory_exists(pathname_v)):
                 new_count_dir=new_count_dir+1
                 newdir.append(pathname_v)
               elif(file_exists(pathname_v)):
                   new_count_file=new_count_file+1
                   newfiles.append(pathname_v)
               else:
                  pass
         v.close() 
         
         #################### 1(a) Newfiles ####################
            
         #################### 1(b) Oldfiles ####################
         old_count=0
         i=open(verify_vfile,"r")
         verification_data=[]
         oldfiles=[]
         v=open("secret.txt","r")
         for line in v:
            line_split_v=line.split(',')
            pathname_v=line_split_v[0]
            verification_data.append(pathname_v)
         v.close()
         for line in i:
            line_split_i=line.split(',')
            pathname_i=line_split_i[0]
            if pathname_i not in verification_data:
               oldfiles.append(pathname_i)
               old_count=old_count+1
         i.close()
         
         #################### 1(b) Oldfiles ####################
         
         #################### 2) Sizefiles ####################
         v=open("secret.txt","r")
         size_count_dir=0
         size_count_file=0
         Sizechangesdir=[]
         Sizechangesfiles=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           size_v=line_split_v[1] 
           i=open(verify_vfile,"r")
           for line in i:
              line_split_i=line.split(',')
              pathname_i=line_split_i[0]
              size_i=line_split_i[1]
              if(pathname_v==pathname_i):
                if(size_v!=size_i):  
                  if(directory_exists(pathname_v)):
                    size_count_dir=size_count_dir+1
                    Sizechangesdir.append(pathname_v)
                  elif(file_exists(pathname_v)):
                      size_count_file=size_count_file+1
                      Sizechangesfiles.append(pathname_v)
                  else:
                    pass
           i.close()
         v.close()
              
         #################### 2) Sizefiles ####################

         ##################### 3) Hashval #####################
         v=open("secret.txt","r")
         hash_changes=0
         Hashchanges=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           if(file_exists(pathname_v)):
             hash_v=line_split_v[6] 
             i=open(verify_vfile,"r")
             for line in i:
              line_split_i=line.split(',')
              pathname_i=line_split_i[0]
              if(file_exists(pathname_i)):
                hash_i=line_split_i[6]
                if(pathname_v==pathname_i):
                  if(hash_v!=hash_i):
                    Hashchanges.append(pathname_v)
                    hash_changes=hash_changes+1
           i.close()
         v.close()

         ##################### 3) Hashval #####################

         ###################### 4(a) User #######################
         v=open("secret.txt","r")
         user_changes=0
         Userchanges=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           user_v=line_split_v[2] 
           i=open(verify_vfile,"r")
           for line in i:
             line_split_i=line.split(',')
             pathname_i=line_split_i[0]
             user_i=line_split_i[2]
             if(pathname_v==pathname_i):
               if(user_v!=user_i):
                 Userchanges.append(pathname_v)
                 user_changes=user_changes+1
           i.close()
         v.close()

         ###################### 4(a) User #######################

         ###################### 4(b) Group ######################
         v=open("secret.txt","r")
         group_changes=0
         Groupchanges=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           group_v=line_split_v[3]
           i=open(verify_vfile,"r") 
           for line in i:
             line_split_i=line.split(',')
             pathname_i=line_split_i[0]
             group_i=line_split_i[3]
             if(pathname_v==pathname_i):
               if(group_v!=group_i):
                 Groupchanges.append(pathname_v)
                 group_changes=group_changes+1
           i.close()
         v.close()

         ##################### 4(b) Group #######################
         
         ##################### 5) A rights #####################
         v=open("secret.txt","r")
         access_rights_dir=0
         access_rights_file=0
         Accessrightsdir=[]
         Accessrightsfiles=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           arights_v=line_split_v[4] 
           i=open(verify_vfile,"r")
           for line in i:
             line_split_i=line.split(',')
             pathname_i=line_split_i[0]
             arights_i=line_split_i[4]
             if(pathname_v==pathname_i):
               if(arights_v!=arights_i):
                 if(directory_exists(pathname_v)):
                   access_rights_dir=access_rights_dir+1
                   Accessrightsdir.append(pathname_v)
                 elif(file_exists(pathname_v)):
                     access_rights_file=access_rights_file+1
                     Accessrightsfiles.append(pathname_v)
                 else:
                    pass
           i.close()
         v.close()

         ##################### 5) A rights #####################
         
         ##################### 6) Modtime #####################
         v=open("secret.txt","r")
         mod_time_dir=0
         mod_time_file=0
         Modtimedir=[]
         Modtimefiles=[]
         for line in v:
           line_split_v=line.split(',')
           pathname_v=line_split_v[0]
           modtime_v=line_split_v[5] 
           i=open(verify_vfile,"r")
           for line in i:
             line_split_i=line.split(',')
             pathname_i=line_split_i[0]
             modtime_i=line_split_i[5]
             if(pathname_v==pathname_i):
               if(modtime_v!=modtime_i):
                 if(directory_exists(pathname_v)):
                   mod_time_dir=mod_time_dir+1
                   Modtimedir.append(pathname_v)
                 elif(file_exists(pathname_v)):
                     mod_time_file=mod_time_file+1
                     Modtimefiles.append(pathname_v)
                 else:
                    pass
           i.close()
         v.close()

         ##################### 6) Modtime #####################

         total_warnings = new_count_dir+new_count_file+old_count+size_count_dir+size_count_file+hash_changes+user_changes+group_changes+access_rights_dir+access_rights_file+mod_time_dir+mod_time_file


         r=open(verify_rfile,"a")
         r.write('1(a) New directories:'+' ,'.join(newdir)+"\n")
         r.write('1(a) New files:'+' ,'.join(newfiles)+"\n")
         r.write('1(b) Removed files/directories:'+' ,'.join(oldfiles)+"\n")
         r.write('2(a) Directories with a different size than recorded:'+' ,'.join(Sizechangesdir)+"\n")
         r.write('2(b) Files with a different size than recorded:'+' ,'.join(Sizechangesfiles)+"\n")
         r.write('3) Files with a different message digest than computed before(contents changed):'+' ,'.join(Hashchanges)+"\n")
         r.write('4(a) Files/directories with a different user:'+' ,'.join(Userchanges)+"\n")
         r.write('4(b) Files/directories with a different group:'+' ,'.join(Groupchanges)+"\n")
         r.write('5(a) Directories with modified access right:'+' ,'.join(Accessrightsdir)+"\n")
         r.write('5(b) Files with modified access right:'+' ,'.join(Accessrightsfiles)+"\n")
         r.write('6(a) Directories with a different modification date:'+' ,'.join(Modtimedir)+"\n")
         r.write('6(b) Files with a different modification date:'+' ,'.join(Modtimefiles)+"\n")
         r.close()

         sleep(1)
         print "\tVerification mode is completed!"
         sleep(1)         

         r=open(verify_rfile,"a")
         r.write('\n')
         r.write('\n')
         r.write('1) Full pathname to monitored directory:%s'%(mon_dir)+"\n")
         r.write('2) Full pathname to verification file:%s'%(verify_vfile)+"\n")
         r.write('3) Full pathname to report file:%s'%(verify_rfile)+"\n")
         r.write('4) Number of directories parsed:%s'%(dir_count_v)+"\n")
         r.write('5) Number of files parsed:%s'%(file_count_v)+"\n")
         r.write('6) Number of warning issued:%s'%(total_warnings)+"\n")
         r.write('7) Time to complete the verification mode:%s'%(time.time()-start_time)+"\n")
         r.close()

      else: #this else is to check if elements -i -D -V -H are correct or not
        print "Enter \'python siv.py -h\' for help ... "
    else: #this else is to check if length_arguments!=10
      print "Enter \'python siv.py -h\' for help ... "
      sleep(1)
    
else:
  print "Enter \'python siv.py -h\' for help ... "
