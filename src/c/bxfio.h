#ifndef BXFIO_H
#define BXFIO_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void bxfio_read_header(char* filename, 
					   char* version, 
					   int * width, 
					   int * height, 
					   int * nnz, 
					   char * symmetry);

#endif