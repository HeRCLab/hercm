#include "bxfio.h"

int main(int argc, char **argv )
{
    printf("Allocating memory for header data... ");
    char * filename = malloc(256 * sizeof(char));
    strcpy(filename, "bcsstk01.bxf");
    char * version = malloc(5 * sizeof(char));
    char * symmetry = malloc(4 * sizeof(char));
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

    printf("Allocating memory for file data... ");
    int * row = malloc(nnz * sizeof(int));
    int * col = malloc(nnz * sizeof(int));
    float * val = malloc(nnz * sizeof(float));
    printf("done.\n");

    printf("reading data from file... ");
    status = bxfio_read_data(filename, nnz, col, row, val);
    if (status == BXFIO_READ_SUCCESS)
    {
        printf("OK\n");

    }
    else
    {
        printf("FAILED\n");
    }

    printf("--- COO data read ---\n");
    printf("row  col  val\n");
    for (int i = 0; i < nnz; i++)
    {
        printf("%d %d %f\n", row[i], col[i], val[i]);
    }

    printf("--- end COO data ---\n");

	return 0;
}