#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#define DIM 1000

void initialization(void);
void delete_elements(int);

struct prim_data {
  		int edges_weight[DIM][DIM];
 		int dimension;
  		int U[DIM];
  		int total_min_distance;
  		int count_nodes_in_mst;
		};

struct prim_data prim;

int main()
{
	int ch,j,t,p_c,p_j,k,serial=1;
	int i;
	int min_distance;
	int new_next_element;

	prim.total_min_distance = 0;
	prim.count_nodes_in_mst = 0;

	
	min_distance = 1000;

	

	printf("Enter the number of nodes:\n");
	scanf( "%d", &prim.dimension);
	printf("Enter the cost of edges: \n");

	for (i = 0; i < prim.dimension; ++i) {
		for (j = 0; j < prim.dimension; j++) {
			  printf("From %d To %d\n",i,j);
			  scanf("%d",&(prim.edges_weight[i][j]));
		}
		
	}


	
    	initialization();

	
	for(k = 0; k < prim.dimension -1; k++)
	{
	    min_distance = 1000;
		
		for(i = 0; i < prim.count_nodes_in_mst; i++)
		{
			
			#pragma omp parallel for
                for(j = 0; j < prim.dimension; j++)
                {
				
                    if(prim.edges_weight[prim.U[i]][j] > min_distance || prim.edges_weight[prim.U[i]][j]==0)
                    {
                        continue;
                    }
                    else
                    {
					#pragma omp critical
                       {
						min_distance = prim.edges_weight[prim.U[i]][j];
						new_next_element = j;
				 	   }
				    }
			    }
 		}
		
		prim.total_min_distance += min_distance;
		
		prim.U[i] = new_next_element;
		
		delete_elements( new_next_element );
		
		prim.count_nodes_in_mst++;
	}

	printf("\n");
	
	for(i = 0 ; i < prim.dimension; i++) {
	    printf("%d ",prim.U[i] );//+1
	    if( i < prim.dimension - 1 ) printf("-> ");
      }

      printf("\n\n");
      printf("Total minimun distance: %d\n\n", prim.total_min_distance);
      printf("\nProgram terminates now..\n");
	  return 0;
}

void initialization(void) {

	int i,j;

	prim.total_min_distance = 0;
	prim.count_nodes_in_mst = 0;

	//initializing the U set
	for(i = 0; i < prim.dimension; i++) prim.U[i] = -1;

	//storing the first node into the U set
	prim.U[0] = 0;
	//deleting the first node
	delete_elements( prim.U[0] );
	//incrementing by one the number of node that are inside the U set
	prim.count_nodes_in_mst++;
}

void delete_elements(int next_element) {

  int k;
  for(k = 0; k < prim.dimension; k++) {
    prim.edges_weight[k][next_element] = 0;
  }
}
/*[student@localhost ~]$ gcc -fopenmp prims.c
[student@localhost ~]$ ./a.out
Enter the number of nodes:
4
Enter the cost of edges: 
From 0 To 0
0
From 0 To 1
3
From 0 To 2
4
From 0 To 3
5
From 1 To 0
3
From 1 To 1
0
From 1 To 2
6
From 1 To 3
1
From 2 To 0
4
From 2 To 1
6
From 2 To 2
0
From 2 To 3
2
From 3 To 0
5
From 3 To 1
1
From 3 To 2
2
From 3 To 3
0

0 -> 1 -> 3 -> 2 

Total minimun distance: 6


Program terminates now..
*/

