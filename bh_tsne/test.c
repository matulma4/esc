#include <stdio.h>
#include <string.h>
save_data( int n, int d,double perplexity, double theta,int no_dims) {
    
	// Open file, write first 2 integers and then the data
	FILE *h;
	if((h = fopen("data.dat", "w+b")) == NULL) {
		printf("Error: could not open data file.\n");
		return;
	}
	int data[1000][100];
	int i,j;	
	for (i = 0;i < 1000;i++){
		for(j=0;j < 100;j++){
			data[i][j] = i+j;
		}
	}
	fwrite(&n, sizeof(int), 1, h);
	fwrite(&d, sizeof(int), 1, h);					// original dimensionality
    fwrite(&theta, sizeof(double), 1, h);			// gradient accuracy
	fwrite(&perplexity, sizeof(double), 1, h);		// perplexity
	fwrite(&no_dims, sizeof(int), 1, h);   
	fwrite(data, sizeof(double), n * d, h);
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
	//save_data(3,3,0,0.1,2);
	//printf("%s\n",argv[1]);
	if(atoi(argv[1]) == 1){
	load_result("result.dat");
	}
	else{
	FILE *f;
	f = fopen("data.txt","r");
	int n,d;
	fscanf(f,"%i %i",&n,&d);
	double data[n][d];
	//double data[1][1] = {{0}};
	int i,j;
	for(i = 0;i < n;i++){
	for(j = 0;j < d;j++){
	fscanf(f,"%lf",&data[i][j]);
	}
	}
	save_data(n,d,0,0.1,2);
	}
}
