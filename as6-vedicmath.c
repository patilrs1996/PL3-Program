#include <omp.h>
#include <stdio.h>
#include <stdlib.h>


int main() 
{	
	int ch1=1;		
	do{
	int num,num1,num2,result,u,t,ch;
	printf("enter 2 digit number: ");
	scanf("%d",&num);
	 u=num%10;
	 t=num/10;
	printf("1:method1\n 2:method2\n");
	printf("enter your choice:");
	scanf("%d",&ch);
	switch(ch)
	{
	  case 1:
		#pragma omp parallel sections shared(num,u,t)
		{
			#pragma omp section
				{
					
					 num1=((t*t)*100)+(u*u);
					
				}
				#pragma omp section
				{			
					num2=((u*t)*2)*10;
					
				}
				#pragma omp section
				{
					 result=num1+num2;
					
				}
		
				
		}
		printf("Square of %d is:%d\n",num,result);
		
		break;
	  case 2:
		#pragma omp parallel sections shared(num,u,t)
		{
			
				#pragma omp section
				{
					
					 num1=((t*10)*(num+u));
			      }
				#pragma omp section
				{			
					num2=u*u;
				}
				#pragma omp section
				{
					 result=num1+num2;
				}
			
		}
		printf("Square of %d is:%d\n",num,result);
		break;
	  default :
		break;


	}
	printf("Do u want to continue Y=1/N=0");
	scanf("%d",&ch1);
}while(ch1==1);
	
	
}
/*OUTPUT:

[student@localhost teb75]$ gcc -fopenmp sqr.c
[student@localhost teb75]$ ./a.out
enter 2 digit number: 25
1:method1
 2:method2
enter your choice:1
Square of 25 is:625
Do u want to continue Y=1/N=01
enter 2 digit number: 35
1:method1
 2:method2
enter your choice:2
Square of 35 is:1225
Do u want to continue Y=1/N=01
enter 2 digit number: 12
1:method1
 2:method2
enter your choice:1
Square of 12 is:144
Do u want to continue Y=1/N=00
[student@localhost teb75]$ 




*/
		
