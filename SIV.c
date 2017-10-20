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
	
	
char *input[argc];
	for(int i = 0; i < argc; i++){
		input[i] = argv[i];	
	}
	char **ptr = input;
	//print(argc, ptr);
	

	if(strcmp(input[1],"-i") == 0 && strcmp(input[2],"-D") == 0 && strcmp(input[4],"-V") == 0 && strcmp(input[6],"-R") == 0 && strcmp(input[8],"-H") == 0 && argc == 10){
		printf("Initialization mode running ...\n");
		char* mondir = input[3];
		while(!checkdir(mondir)){
			printf("Please enter a valid directory:\n");
			scanf ("%[^\n]%*c", input[3]);
			mondir = input[3]; 
		}

		char *vfile = input[5];
		char *rfile = input[7];

		while(!checkoutside(mondir, vfile)){
			printf("Please enter verification file outside monitored directory:\n");
			scanf("%[^\n]%*c", input[5]);
			vfile = input[5];
		}

		while(!checkoutside(mondir, rfile)){
			printf("Please enter report file outside monitored directory:\n");
			scanf("%[^\n]%*c", input[7]);
			rfile = input[7];
		}

		if(checkfile(vfile)){
			printf("Do you want to re-write the verification file: y/n \n");
			char answer = getchar();
			getchar();
			while(!(answer == 'y' || answer == 'n')){
				printf("Enter y/n :\n");
				answer = getchar();
				getchar();
			}
			if(answer == 'y'){
				FILE *fp;
				fp = fopen(vfile, "w+");
				fclose(fp);
			}
			else if(answer == 'n'){
				printf("Terminating the program\n");
				printf("Bye\n");
				return -1;
			}
		}

		if(checkfile(rfile)){
			printf("Do you want to re-write the report file: y/n \n");
			char answer = getchar();
			getchar();
			while(!(answer == 'y' || answer == 'n')){
				printf("Enter y/n :\n");
				answer = getchar();
				getchar();
			}
			if(answer == 'y'){
				FILE *fp;
				fp = fopen(rfile, "w+");
				fclose(fp);
			}
			else if(answer == 'n'){
				printf("Terminating the program\n");
				printf("Bye\n");
				return -1;
			}
		}
		
		listdir(mondir, vfile);
		
	}
	else{
		printf("<-i | -v | -h -D Monitoring_Directory -V Verification_File -R Report_File -H Hash_function\n");	
	}
	return 0;
