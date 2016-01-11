#include "bxfio.h"

int main(int argc, char **argv )
{
    char * version;
    char * symmetry;
    int * height;
    int * width;
    int * nnz;
    bxfio_read_header("test", version, height, width, nnz, symmetry);
	return 0;
}