#include "bxfio.h"

int main(int argc, char **argv )
{
    printf("Allocating memory for header data... ");
    char * filename = (char*) malloc(512);
    strcpy(filename, "sample.bxf");
    char * version = (char*) malloc(5);
    char * symmetry = (char*) malloc(4);
    int height;
    int width;
    int nnz;
    bxfio_status status;
    printf("done.\n");

    printf("reading header from file... ");
    status = bxfio_read_header(filename, version, &width, &height, &nnz, symmetry);
    if (BXFIO_READ_HEADER_SUCCESS == status)
    {
        printf("OK\n");
    }
    else
    {
        printf("FAILED\n");
    }
    
    printf("--- header data read --- \n");
    printf("VERSION: %s\n", version);
    printf("WIDTH: %d\n", width);
    printf("HEIGHT: %d\n", height);
    printf("NNZ: %d\n", nnz);
    printf("SYMMETRY: %s\n", symmetry);
    printf("-- end header data ---\n");
	return 0;
}