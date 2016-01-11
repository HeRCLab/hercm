#include "bxfio.h"

/*! Read a BXF header
 * Read in the header from a BXF file. All string arguments are of known length
 * and thus it is not necessary to pass their length. Be sure they are allocated
 * to the proper size before calling this function though! 
 * 
 * This function supports **only** BXF 2.2 (`BXF22`) at this time. Older header
 * formats are liable to cause crashes or unexpected behaviors
 * 
 * @param[in] filename always 512 characters long, containing the 
 * relative/absolute path to the file
 * @param[out] version always 6 characters long, containing the BXF version 
 * specifier
 * @param[out] width the width of the matrix
 * @param[out] height the height of the matrix
 * @param[out] nnz number of nonzero elements in the matrix
 * @param[out] symmetry always 4 characters long, containing `SYM` or `ASYM`
 */

void bxfio_read_header(char * filename, 
					   char * version, 
					   int * width, 
					   int * height, 
					   int * nnz, 
					   char * symmetry)
{
    printf(filename);
}