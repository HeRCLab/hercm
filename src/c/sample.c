#include "bxfio.h"

int main(int argc, char **argv )
{
    printf("Allocating memory for header data... ");
    char * filename = (char*) malloc(512);
    strcpy(filename, "test.bxf");
    char * version = (char*) malloc(6);
    char * symmetry = (char*) malloc(4);
    int * height = (int*) malloc(1);
    int * width = (int*) malloc(1);
    int * nnz = (int*) malloc(1);
    printf("done.\n");

    bxfio_read_header(filename, version, height, width, nnz, symmetry);
	return 0;
}