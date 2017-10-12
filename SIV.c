#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include<dirent.h>
#include<unistd.h>
#include<errno.h>
#include<pwd.h>
#include<grp.h>
#include<sys/stat.h>


        off_t filesize(char *name);
void listdir(char *name, char *verify);
char* getowner(char *name);
char* getgroup(char *name);
char* permissions(char *file);
long modtime(char *file);
void print(int argc, char **ptr);
bool checkdir(char* name);
bool checkfile(char* name);
bool checkoutside(char *dir, char *file);
