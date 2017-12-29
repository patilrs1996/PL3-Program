#include<stdio.h>
#include<omp.h>
omp_lock_t r;
omp_lock_t w;
int readcount=0;
FILE *fp;


void reader()
{
 char string[100];
 
   omp_set_lock(&r);
   readcount++;
   if(readcount==1)
   {
     omp_set_lock(&w);
   }
   omp_unset_lock(&r);

  printf("\n Reading thread id:%d",omp_get_thread_num());
 fp = fopen("a.txt" , "r");

  if(fp == NULL) 
 {
   perror("Error opening file");
   
 }

 while( fgets (string, 100, fp)!=NULL ) 
{
  
   puts(string);
 }
 fclose(fp);
 


   omp_set_lock(&r);
   readcount--;
   if(readcount==0)
   {
     omp_unset_lock(&w);
   }
   omp_unset_lock(&r);
	

}

void writer()
{

	char s[50];
   omp_set_lock(&w);
  
    fp=fopen("a.txt","a");
	printf("\n Enter Any String:-");
	scanf("%s",&s);
	fprintf(fp,"\n %s",s);
    //fprintf(fp,"\n Writing is performed by thread id:%d",omp_get_thread_num());
    fclose(fp);
    printf("\n Writing thread id:%d",omp_get_thread_num());
   omp_unset_lock(&w);
 
}


 

int main()
{ 
  omp_init_lock(&r);
  omp_init_lock(&w);
  
  int r1,w1,i,c;


  printf("\n Enter the number of readers:");
  scanf("%d",&r1);
  printf("\nEnter the number of writers:");
  scanf("%d",&w1);
  c=r1+w1;
  omp_set_num_threads(c);
	#pragma omp parallel
		#pragma omp for
			for(i=0;i<(r1+w1);i++)
			{
			  if(i<r1)
			  {  
                             
			     reader();
			  }
			  else
			  {
			     writer();
			  }
			}	
 return 0;

}
/*
OUTPUT:_
[student@localhost teb75]$ gcc -fopenmp read_write.c
[student@localhost teb75]$ ./a.out

 Enter the number of readers:1

Enter the number of writers:2

 Enter Any String:-welcome

 Writing thread id:2
 Reading thread id:0

 welcome

 Enter Any String:-thanks

 Writing thread id:1[student@localhost teb75]$ 
*/
/*a.txt

 welcome
 thanks
*/


