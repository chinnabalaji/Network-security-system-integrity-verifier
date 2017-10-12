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

int main(int argc, char *argv[]){
	//char **ptr = argv;
	//for(int i = 0; i < argc; i++){
		//printf("%s at %p\n", *(ptr + i), (ptr + i));
	//}
