#ifndef BXFIO_H
#define BXFIO_H

//#define BXFIO_READ_HEADER_IOERROR 1001;
//#define BXFIO_READ_HEADER_FIELDERROR 1002;
//#define BXFIO_READ_HEADER_SUCCESS 1003;

typedef enum bxfio_status {
    BXFIO_READ_HEADER_SUCCESS,
    BXFIO_READ_HEADER_FIELDERROR,
    BXFIO_READ_HEADER_IOERROR
 } bxfio_status;


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

bxfio_status bxfio_read_header(char* filename, 
					   char* version, 
					   int * width, 
					   int * height, 
					   int * nnz, 
					   char * symmetry);

int bxfio_check_file_exists (char *filename);

#endif