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

/**
 * @brief      Drops the first n characters from a string in place. 
 *
 * @param      str   string to drop chars from
 * @param[in]  n     the number of chars to drop 
 */
void bxfio_drop_chars(char *str, int n)
{
   char* res = str + n;
   while ( *res )
   {
      *str = *res;
      ++str;
      ++res;
   }
   *str = '\0';
}

/**
 * @brief      Read the data from a BXF file. 
 *
 * @param[in]      filename  relative or absolute path of bxf file
 * @param[in]  nnz       number of nonzero entries (read from the header)
 * @param[out]      col       int array initialized to nnz indices long
 * @param[out]      row       int array initialized to nnz entries long
 * @param[out]      val       float array initialized to nns entries long
 *
 * @return     one of:
 * `BXFIO_READ_SUCCESS` - if the operation completed successfully
 * `BXFIO_READ_IOERROR` - if there was an error reading the file
 * `BXFIO_READ_FIELDERROR` - the file was read correctly, but one or more fields
 * were invalid
 */
bxfio_status bxfio_read_data(char * filename, 
    int nnz, 
    int * col, 
    int * row, 
    float * val)
{
    if (!bxfio_check_file_exists(filename))
    {
        // the file does not exist
        return BXFIO_READ_IOERROR;
    }

    FILE *fp;
    char buf[255];
    fp = fopen(filename, "r");
    int overflow_counter = 0; 
    
    // consume the header
    fgets(buf, 255, fp);

    // seek to the beginning of the VAL field
    while(strcmp(buf, "VAL FLOAT\n") != 0 && overflow_counter <= BXFIO_READ_OVERFLOWTHRESHOLD)
    {
        fgets(buf, 255, fp);
        overflow_counter++; // avoid non-terminating loop
    }

    if (overflow_counter >= BXFIO_READ_OVERFLOWTHRESHOLD)
    {
        return BXFIO_READ_FIELDERROR;
    }

    overflow_counter = 0;

    while(strcmp(buf, "ENDFIELD\n") !=0 )
    {
        fgets(buf, 255, fp);
        float current_val;
        int val_idx = 0, chars_read = 0;
        overflow_counter++; // avoid non-terminating loop
        if (strcmp(buf, "ENDFIELD\n") == 0 ||
            strcmp(buf, "") == 0 ||
            strcmp(buf, "ROW INT\n") ==0)
        {
            printf("DEBUG: skipping line: %s", buf);
            continue;
        }

        /*for (val_idx; sscanf(&buf[chars_read], "%f%n", &current_val, &chars_read) == 1; val_idx++) 
        {
            printf("DEBUG: read number: %f\n", current_val);
            val[val_idx] = current_val;
        }*/
        for (val_idx; sscanf(buf, "%f%n", &current_val, &chars_read) == 1; val_idx++)
        {
            printf("DEBUG: read number %f\n", current_val);
            bxfio_drop_chars(buf, chars_read);
        }
    }


    fclose(fp);

    return BXFIO_READ_SUCCESS;

}