#ifndef BXFIO_H
#define BXFIO_H


typedef enum bxfio_status {
    BXFIO_READ_HEADER_SUCCESS,
    BXFIO_READ_HEADER_FIELDERROR,
    BXFIO_READ_HEADER_IOERROR,
    BXFIO_READ_SUCCESS,
    BXFIO_READ_IOERROR,
    BXFIO_READ_FIELDERROR
 } bxfio_status;

// maximum number of lines readable from a field, should always be 10000 except 
// for debugging purposes
#define BXFIO_READ_OVERFLOWTHRESHOLD 100 

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

bxfio_status bxfio_read_data(char * filename, 
    int nnz, 
    int * col, 
    int * row, 
    float * val);

int bxfio_check_file_exists (char *filename);

#endif