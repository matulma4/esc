#include <stdio.h>
#include <string.h>
#include <stdlib.h>
save_data( int n, int d,double perplexity, double theta,int no_dims,double** data) {
    
	// Open file, write first 2 integers and then the data
	printf("Opening file for writing\n");
	FILE *h;
	if((h = fopen("data.dat", "w+b")) == NULL) {
		printf("Error: could not open data file.\n");
		return;
	}
	//int data[1000][100];
	/*int i,j;
		
	for (i = 0;i < 1000;i++){
		for(j=0;j < 100;j++){
			data[i][j] = i+j;
		}
	}*/
	printf("Writing info\n");
	fwrite(&n, sizeof(int), 1, h);
	fwrite(&d, sizeof(int), 1, h);												// original dimensionality
   	fwrite(&theta, sizeof(double), 1, h);										// gradient accuracy
	fwrite(&perplexity, sizeof(double), 1, h);								// perplexity
	fwrite(&no_dims, sizeof(int), 1, h);   
	fwrite(data, sizeof(double), n * d, h);
	printf("Written\n");
	//fwrite(landmarks, sizeof(int), n, h);
 	//fwrite(costs, sizeof(double), n, h);
    	fclose(h);
	printf("Wrote the %i x %i data matrix successfully!\n", n, d);
}

load_result(char* fname){
	FILE *f;
	int i,j,n,d;
	double a;
	f = fopen(fname,"r+b");
	fread(&n,sizeof(int),1,f);
	fread(&d,sizeof(int),1,f);
	for(i = 0;i < n;i++){
		for(j = 0;j < d;j++){
			fread(&a,sizeof(double),1,f);
			printf("%f ",a);
		}
		printf("\n");
	}
	fclose(f);
}

int main(int argc,const char* argv[]){
	printf("Argument is %s\n",argv[1]);
	//save_data(3,3,0,0.1,2);
	//printf("%s\n",argv[1]);
	if(atoi(argv[1]) == 1){
	load_result("result.dat");
	}
	else{
	FILE *f;
	printf("Opening data.txt\n");
	f = fopen("data.txt","r");
	printf("Opened.\n");
	int n,d,y;
	fscanf(f,"%i %i",&n,&d);
	printf("%i %i\n",n,d);
	printf("Allocating data\n");
	double** data = (double **)malloc(n*sizeof(double));
	for (y = 0;y < n;y++){
	data[y] = (double *)malloc(d * sizeof(double));
	}
	printf("Allocated.\n");
	//double data[1][1] = {{0}};
	int i,j;
	printf("Scanning data\n");
	for(i = 0;i < n;i++){
	for(j = 0;j < d;j++){
	//printf("%i %i\n",i,j);
	fscanf(f,"%lf",&data[i][j]);
	}
	}
	int perplexity = atoi(argv[2]);
	double theta;
	sscanf(argv[3],"%lf",&theta)
	printf("Scanned,saving data\n");
	save_data(n,d,perplexity,theta,2,(double**) data);
	printf("Saved\n");
	free(data);
	}
}
