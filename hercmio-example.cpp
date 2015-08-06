/*
Copyright (c) 2015, Charles Daniels
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the 
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from 
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

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

void fatalError(string message)
{
	// accepts the string message as an argument. Exits the program after 
	// printing message.
	cout<<message<<endl<<"A fatal error has been encountered. Program "; 
	cout << "execution will now halt." << endl;
	exit(1);
}

int main(int argc, char *argv[])
{

	int status = -1; 
	string message; // temporary variable for storing messages

	if (argc < 2) // make sure there is at least one argument 
	{
		message = "ERROR: at least one argument required. Run"; 
		message.append(" ./hercmio-example help for further help");
		fatalError(message);
	}

	string command = argv[1];
	if (command == "help")
	{
		cout << "USAGE: \n\
./hercmio-example read [file] - read the hercm file [file] using hermio, print as csr matrix to stdout\n\
./hercmio-example write [infile] [outfile] - reads the file [infile], converts to hercm csr matrix and writes to [outfile]\n\
for the above, [infile] should contain one or more lines, each with the same number of space-delineated values representing a matrix.\n\
An example might look like this:\n \
- begin -\n\
1 2 3\n\
4 5 6\n\
7 8 9\n\
- end - \n\
Do not include \"- begin -\" or \"- end -\"";
	}
	else if (command =="read")
	{
		if (argc != 3)
		{
			message = "ERROR: the read command requires exactly one argument.";
			message.append(" Run ./hercmio-example help for further help");
			fatalError(message);
		}
		string fileName = argv[2];
		
		// variable which we will pass by reference to readHercmHeader()
		string format, symmetry;
		int width, height, nzentries; 
		cout << "Reading header of file " << fileName << " ..." << endl;

		// read in header data
		status = readHercmHeader(fileName, 
								 format, 
								 width, 
								 height, 
								 nzentries, 
								 symmetry); 

		if (status != HERCMIO_STATUS_SUCCESS)
		{
			fatalError("Error while reading header file");
		}

		cout << "done. \nread format: " << format << " width: ";
		cout << width << " height: " << height << " nzentries: "; 
		cout << nzentries << " symmetry " << symmetry << endl;

		// arrays we will bass by reference to headHercm()
		float val[nzentries];
		int row_ptr[width+1];
		int colind[nzentries];

		// read the hercm file itself 
		cout<< "Reading data from file " << fileName <<" ..." << endl;
		status = readHercm(fileName, val, row_ptr, colind); // read the file
		if (status != HERCMIO_STATUS_SUCCESS)
		{
			fatalError("Error while reading file");
		}

		// print the values we read to the user
		cout << "done.\nRead val: "; 
		for (int i=0; i<nzentries;i++)
		{
			cout << val[i] << " ";
		}
		cout << endl;
		cout << "row_ptr: ";
		for (int i=0; i<height+1;i++)
		{
			cout << row_ptr[i] << " ";
		}
		cout << endl;
		cout << "colind: ";
		for (int i=0; i<nzentries;i++)
		{
			cout << colind[i] << " ";
		}

		// just for fun, reconstruct the original dense matrix for the user
		cout << endl << "reconstructing matrix..." << endl;
		float row[width]; // one reconstructed row
		int current_ptr = 1; // current index in row_ptr. If we start at zero,
		// we get an extra row of just zeros because of the below loop

		// initialize row to zero (cannot initialize a variable sized array 
		// inline)
		for (int i=0; i<width; i++) 
		{
			row[i] = 0;
		}

		// we will iterate over each index in val
		for (int i=0; i<=nzentries; i++) 
		{
			 // if our current index is the beginning of a new row
			if (i == row_ptr[current_ptr])
			{
				// iterate over the row and print it out
				for (int j=0; j<width; j++)
				{ 
					cout << setw(7) << setprecision (3) << row[j]; 
					row[j] = 0; // row needs to be cleared out, so we can read 
					// in the next row
				}
				cout << endl;
				current_ptr++; // start looking for the next new row 
				if (current_ptr > height)
				{
					cout << "done." << endl;
					exit(0);
				}
			}
			int index = colind[i]; // the index within the row is set to the 
			// column index of this value 
			row[index] = val[i]; // set the appropriate index of row. Note that 
			// any indexes we don't fill in this way are initialized to zero
		}

	}
	else if (command =="write")
	{
		if (argc != 4)
		{
			message = "ERROR: the write command requires exactly two arguments";
			message.append(". Run ./hercmio-example help for further help");
			fatalError(message);
		}
		string inputFileName = argv[2]; 
		string outputFileName = argv[3];

		// read in the input file 
		ifstream inputFile(inputFileName.c_str());

		int inputMatrixWidth = 0, inputMatrixHeight = 0; // we will need 
		// somewhere to store...  
		string line; // the line we are currently reading

		if (!inputFile.is_open())
		{
			cout << "ERROR: could not open " << inputFileName << endl;
			exit(1);
		}
		else
		{
			cout << "opened file " << inputFileName << endl;
		}

		// first we need to get the size of the matrix
		while(getline(inputFile, line, '\n'))
		{
			inputMatrixHeight += 1;
			vector<string> lineVector; // we will split the line into this 
			// vector, using split from hercmio
			lineVector = split(line, ' ');
			inputMatrixWidth = 0;
			for (int i=0; i<lineVector.size(); i++)  
			{
				inputMatrixWidth++;
			}
		}

		cout << "detected matrix of size: " << inputMatrixWidth << " by "; 
		cout << inputMatrixHeight << endl;

		// instantiate the matrix 
		float inputMatrix[inputMatrixWidth][inputMatrixHeight]; 
		//                horizontal        vertical

		// read in the matrix 
		inputFile.clear(); // return to the beginning of the file
		inputFile.seekg(0, ios::beg);
		int lineCounter = 0; // counter so we know what line we are on, and 
		// thus our row index for inputMatrix 
		while(getline(inputFile, line, '\n'))
		{
			vector<string> lineVector; 
			lineVector = split(line, ' ');
			for (int i=0; i<lineVector.size(); i++)
			{
				inputMatrix[i][lineCounter] = stringToFloat(lineVector[i]);
			}
			lineCounter++;
		}
		for(int row=0; row<inputMatrixHeight; row++)
		{
			for (int col=0; col<inputMatrixWidth; col++)
			{
				cout << setw(9) << setprecision(5) << inputMatrix[col][row];
			}
			cout << endl;
		}

		int nzentries=0; // copunt the number of non zero entries
		for(int row=0; row<inputMatrixHeight; row++)
		{
			for (int col=0; col<inputMatrixWidth; col++)
			{
				if (inputMatrix[col][row] != 0)
				{
				nzentries++;
				}
			}
		}

		float val[nzentries];
		int row_ptr[inputMatrixHeight+1];
		int colind[nzentries];
		int valCounter = 0; // keep track of what index of val we are writing to
		int row_ptrCounter = 1;
		row_ptr[0] = 0; // the below does not account for the first index of 
		// row_ptr
		int tmp_ptr = 0;
	
		for (int row=0; row<inputMatrixHeight; row++) // for each row
		{
			for (int col=0; col<inputMatrixWidth; col++) // for each column 
			{
				float currentValue = inputMatrix[col][row]; // get the value at
				// the current index 
				if (currentValue != 0.0) // if it is a non zero value
				{
					// set the next index of value
					val[valCounter] = currentValue; 
					colind[valCounter] = col; // set col_ind 
					tmp_ptr++; 
					valCounter++; 
				}
			}
			row_ptr[row_ptrCounter] = tmp_ptr; // we are starting a new row, 
			// save our index
			row_ptrCounter++;
		}
	

		// output the results to the user 
		cout << "done." << endl;
		cout << "val: ";
		for (int i=0; i<nzentries; i++)
		{
			cout << val[i] << " ";
		}
		cout << endl;

		cout << "row_ptr: ";
		for (int i=0; i<inputMatrixHeight+1;i++)
		{
			cout << row_ptr[i] << " ";
		}
		cout << endl;

		cout << "colind: ";
		for (int i=0; i<nzentries;i++)
		{
			cout << colind[i] << " ";
		}
		cout << endl;

		// for this example, we will assume all matrices are symmetrical 
		status = writeHercm(outputFileName, 
							inputMatrixHeight, 
							inputMatrixWidth, 
							nzentries, 
							val, 
							row_ptr, 
							colind, 
							"ASYM");
		if (status != HERCMIO_STATUS_SUCCESS)
		{
			fatalError("could not write to file");
		}

	}


	return 0;
}