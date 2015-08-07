/* USAGE
./hercmio-example read [file] - read the hercm file [file] using hermio, print 
as csr matrix to stdout

./hercmio-example write [infile] [outfile] - reads the file [infile], converts 
to hercm csr matrix and writes to [outfile] 

for the above, [infile] should contain one or more lines, each with the same 
number of space-delineated values representing a matrix. 

An example might look like this: 
- begin -
1 2 3
4 5 6
7 8 9
- end - 
Do not include "- begin -" or "- end -"
*/

#include "hercmio.hpp"
#include <iomanip>

int main(int argc, char *argv[])
{

	int status = -1; 

	if (argc < 2) // make sure there is at least one argument 
	{
		cout << "FATAL: at least one argument is required" << endl;
		cout << "see ./hercmio-example help for help" 	   << endl;
	}

	string command = argv[1];
	if (command == "help")
	{
		cout << "hercmio-example usage:" 								<< endl;
		cout << "help   - - - - display this message"					<< endl;
		cout << "read [file]  - reads hercm file [file], prints as csr" << endl;
		cout << "write [file] - writes the following matrix to [file]"  << endl;
		cout << " 0 5 3 " 												<< endl;
		cout << " 2 9 4 " 												<< endl; 
		cout << " 0 0 1 " 												<< endl;
	}
	else if (command == "read")
	{
		if (argc != 3)
		{
			cout << "FATAL: incorrect number of arguments" << endl;
		}
		string inputFile = argv[2];
		cout << "reading file " << inputFile << endl;
		
		// variables needed to read headers 
		int width;
		int height;
		int nzentries;
		string symmetry;
		float verification; 

		if (readHercmHeader(inputFile, 
						   width, 
						   height, 
						   nzentries, 
						   symmetry, 
						   verification) != HERCMIO_STATUS_SUCCESS)
		{
			cout << "FATAL: hercmio encountered an error while reading";
			cout << " the header!" << endl;
		}

		cout << "Read header: "  	 			 << endl;
		cout << "width: " 		 << width		 << endl;
		cout << "height " 		 << height 		 << endl;
		cout << "nzentries: " 	 << nzentries	 << endl;
		cout << "symmetry: "	 << symmetry	 << endl;
		cout << "verification: " << verification << endl;

		cout << "reading matrix data..." << endl;
		cout << "allocating coo vectors..." << endl;
		float val[nzentries];
		int   col[nzentries];
		int   row[nzentries];

		cout << "reading data from file..." << endl;

		if (readHercm(inputFile, val, row, col) != HERCMIO_STATUS_SUCCESS)
		{
			cout << "FATAL: hercmio encountered error while reading the file";
			cout << endl;
		}

		cout << "read data in coo format: " << endl;
		cout << setprecision(6);
		cout << setw(10) << "val" << setw(10) << "col" << setw(10) << "row";
		cout << endl;
		cout << "------------------------------" << endl;
		for (int i = 0; i < nzentries; i++)
		{
			cout << setw(10) << val[i] << setw(10) << col[i] << setw(10);
			cout << row[i] << endl; 
		}

		cout << "making matrix row major..." << endl;
		makeRowMajor(row, col, val, nzentries);

		cout << "matrix in row major format: " << endl;
		cout << setprecision(6);
		cout << setw(10) << "val" << setw(10) << "col" << setw(10) << "row";
		cout << endl;
		cout << "------------------------------" << endl;
		for (int i = 0; i < nzentries; i++)
		{
			cout << setw(10) << val[i] << setw(10) << col[i] << setw(10);
			cout << row[i] << endl; 
		}

		cout << "converting matrix to csr format..." << endl;

		/*
		int cooToCsr(int * row, 
			 int * col, 
			 float * val, 
			 int * ptr, 
			 int nzentries, 
			 int height)
		*/
		cout << "allocating ptr vector..." << endl; 
		int ptr[height+1];
		for (int i=0; i<height+1; i++)
		{
			ptr[i] = -999; 
		}


		cout << "performing conversion..." << endl;
		cooToCsr(row, col, val, ptr, nzentries, height);

		cout << "matrix in csr format:" << endl;
		cout << setw(10) << "val" << setw(10) << "col" << setw(10) << "ptr";
		cout << endl;
		cout << "------------------------------" << endl;

		int ptrCounter = 0;

		for (int i = 0; i < nzentries; i++)
		{
			cout << setw(10) << val[i] << setw(10) << col[i] << setw(10);
			if (ptrCounter < height+1)
			{
				cout << ptr[ptrCounter] << endl; 
				ptrCounter++;
			}
			else
			{
				cout << "N/A" << endl;
			}
		}

	}
	


	return 0;
}