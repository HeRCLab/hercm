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
 * 
 * @returns one of: 
 * 
 * * `BXFIO_READ_HEADER_SUCCESS` if the operation completed correctly
 * * `BXFIO_READ_HEADER_IOERROR` if an error is encountered while reading the file
 * * `BXFIO_READ_HEADER_FIELDERROR` the file was read successfully, but one or more
 * fields contained an invalid value
 */


bxfio_status bxfio_read_header(char * filename, 
					   char * version, 
					   int * width, 
					   int * height, 
					   int * nnz, 
					   char * symmetry)
{

   
    if (!bxfio_check_file_exists(filename))
    {
        // the file does not exist
        return BXFIO_READ_HEADER_IOERROR;
    }

   // there should probably be some kind of error checking here
   FILE *fp;
   char buf[256];
   fp = fopen(filename, "r");

   fscanf(fp, "%s", version);
   fscanf(fp, "%d", width);
   fscanf(fp, "%d", height);
   fscanf(fp, "%d", nnz);
   fscanf(fp, "%s", symmetry);
   fclose(fp);


   if (strcmp(version,"BXF22") != 0)
   {
        return BXFIO_READ_HEADER_FIELDERROR;
   }

   if (strcmp(symmetry, "SYM") != 0 &&
       strcmp(symmetry, "ASYM") != 0)
   {
        return BXFIO_READ_HEADER_FIELDERROR;
   }

   if (width < 0 || height < 0 || nnz < 0)
   {
        return BXFIO_READ_HEADER_FIELDERROR;
   }

   return BXFIO_READ_HEADER_SUCCESS;

   
}

/**
 * @brief      Checks if a file exists
 *
 * @param      filename  name of file to check existence of
 *
 * @return     1 if the file exists, 0 otherwise
 */
int bxfio_check_file_exists (char *filename)
{
    return access( filename, F_OK ) != -1;
   
}