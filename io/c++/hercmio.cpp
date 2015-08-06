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


#include "hercmio.hpp"

bool checkVectorForString(vector<string> vectorToCheck, 
						  string stringToSearchFor)
{
	// checks of stringToSearchFor is contained by the vector of 
	//strings vectorToCheck. Returns true if it contains stringToSearchFor
	// is found at least once, and false if it is not found

	for (int i=0; i<vectorToCheck.size(); i++)
	{
		if (vectorToCheck[i] == stringToSearchFor)
		{
			return true;
		}
	}
	return false;
}

int stringToInt(string sourceString)
{
	// converts the string sourceString to an int, then returns that 
	int result; 
	stringstream convert(sourceString);
	if (!(convert >> result))
	{
		cout << "ERROR: failed to convert " << sourceString << " to integer";
		exit(1);
	}
	return result;

}

float stringToFloat(string sourceString)
{
	// converts the string sourceString to an float, then returns that 
	float result; 
	stringstream convert(sourceString);
	if (!(convert >> result))
	{
		cout << "ERROR: failed to convert " << sourceString << " to integer";
		exit(1);
	}
	return result;

}


vector<string> split(string str, char delimiter) 
{
 	vector<string> internal;
  	stringstream ss(str); 
  	string tok;
  	
  	while(getline(ss, tok, delimiter)) 
  	{
  		if (tok != "")
  		{
			internal.push_back(tok);
		}
  	}
	return internal;
}

int readHercmHeader(string fileName, 
					string &format, 
					int &width, 
					int &height, 
					int &nzentries, 
					string &symmetry)
{
	// reads header of a hercm file
	// accepts header fields by reference, then populates values into those 
	
	// fileName - name of file to open
	// width - matrix width (number of cols)
	// height - matrix height (number of rows)
	// nzentries - number of nonzero entries in matrix
	// symmetry - matrix symmetry

	// returns HERCMIO_STATUS_FAILURE on any error
	// returns HERCMIO_STATUS_SUCCESS otherwise

	string header; // this will store the header read from the file
	// the file object. c_str is required to make this work with c++98
	ifstream targetFile(fileName.c_str()); 

	if (targetFile.is_open())
	{
		getline(targetFile, header); // get the first line 
	}
	else
	{ 
		cout << "ERROR: Unable to open file " << fileName << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	if (header.substr(0,10) != "HERCM FILE")
	{
		cout << "ERROR: malformed  or not a HeRCM file. read ";
		cout << header.substr(0,10) <<" expected HERCM FILE" << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	vector<string> headerItemsVector;
	headerItemsVector = split(header, ' ');

	if (headerItemsVector.size() != 7)
	{
		cout << "ERROR: malformed or not a HeRCM file. Expected 7 fields,";
		cout << " read ";
		cout << headerItemsVector.size() << " from " << header << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	format    = headerItemsVector[2];
	width     = stringToInt(headerItemsVector[3]);
	height    = stringToInt(headerItemsVector[4]);
	nzentries = stringToInt(headerItemsVector[5]);
	symmetry  = headerItemsVector[6];
	return HERCMIO_STATUS_SUCCESS; 

}

int readHercm(string fileName, float * val, int * row_ptr, int * colind)
{
	// reads the file contents of the hercm file, then populates val, row_ptr,
	// and colind with the values thereof. 

	// fileName - the name of the hercm file to read 
	// val - the val array for the CSR matrix
	// row_ptr - the row_ptr array for the CSR matrix (sometimes called ptr)
	// colind - the colind array for the CSR matrix
	// symmetry will store the matrix's symmetry (SYM or ASYM)

	// returns HERCMIO_STATUS_FAILURE on any error
	// returns HERCMIO_STATUS_SUCCESS otherwise

	string line; // this will store each line of the file as we read it in
	int lineCounter=0; // we will use this to keep track of what line we are on
	ifstream targetFile(fileName.c_str()); // instantiate the file object
	// c_str is required pre-c++11 as ifstream expects a const char* 

	char* validFieldsStringArray [] = {"FORMAT","WIDTH","HEIGHT","NZENTRIES",
									   "ROWPTRLENGTH","VAL","ROWPTR","COLIND"};
	// this will throw compiler warnings, but it is the easiest way to 
	// initialize a data structure of strings in c++ 98.
	vector<string> validFields(validFieldsStringArray, 
							   validFieldsStringArray+8); 
	string currentField; // this will store the last read field

	// field values 
	string format;
	int width, height, nzentries, rowptrlength;

	if (targetFile.is_open()) // check if opening the file failed
	{
		while ( getline (targetFile, line)) // while we can get a new line 
		{
			lineCounter++;
			if (lineCounter == 1)
			{
				// we need to make sure this is a HeRCM file
				if (line.substr(0,10) != "HERCM FILE")
				{
					cout<<"ERROR: malformed file or not hercm format (expected";
					cout << " \"HERCM FILE\", found \""<<line<<"\")"<<endl;
					return HERCMIO_STATUS_FAILURE;
				}
			}
			else if (line == "END") 
			{
				return HERCMIO_STATUS_SUCCESS;
			}
			// check of this line is a valid field targetFile
			else if (checkVectorForString(validFields, line)) 
			{
				currentField = line; 
			}
			else
			{
				if (currentField == "VAL")
				{
					// vector in which to store split value string
					vector<string> valString; 
					char delimiter = ' ';
					valString = split(line, delimiter); // split the val vector
					for (int i=0; i<valString.size(); i++)
					{
						val[i] = stringToFloat(valString[i]);
					}
				}
				else if (currentField == "ROWPTR")
				{
					// vector in which to store split value string
					vector<string> row_ptrString; 
					char delimiter = ' ';
					row_ptrString = split(line, delimiter); // split the vector
					for (int i=0; i<row_ptrString.size(); i++)
					{
						row_ptr[i] = stringToInt(row_ptrString[i]);
					}
				}
				else if (currentField == "COLIND")
				{
					// vector in which to store split value string
					vector<string> colindString; 
					char delimiter = ' ';
					colindString = split(line, delimiter); // split the vector
					for (int i=0; i<colindString.size(); i++)
					{
						colind[i] = stringToInt(colindString[i]);
					}
				}

			}
		}
	}
	else
	{ 
		cout << "ERROR: Unable to open file " << fileName << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	return HERCMIO_STATUS_SUCCESS;
}


int writeHercm(string fileName, 
			   int height, 
			   int width, 
			   int nzentries, 
			   float * val, 
			   int * row_ptr, 
			   int * colind, 
			   string symmetry)
{
	// writes a CSR matrix to a file 

	// fileName - name of file for writing
	// height - height of matrix (number of rows)
	// width - width of matrix (number of cols)
	// nzentries - number of non zero entries in matrix
	// val - CSR val array
	// row_ptr - CSR row_ptr array
	// colind - CSR colind array 
	// symmetry - symmetry of matrix, either SYM or ASYM per hercm spec

	// returns HERCMIO_STATUS_FAILURE on failure
	// returns HERCMIO_STATUS_SUCCESS otherwise

	ofstream targetFile (fileName.c_str());
	string header; // the header 

	if (!targetFile.is_open())
	{
		cout <<"ERROR: could not open file " << fileName << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	if (symmetry != "SYM" && symmetry != "ASYM")
	{
		cout << "ERROR: illegal value for symmetry, expected SYM or ASYM, got ";
		cout << symmetry << endl;
		return HERCMIO_STATUS_FAILURE;
	}

	header = "HERCM FILE CSR ";
	// these are the easiest ways to cast ints and floats to string
	header.append(static_cast<ostringstream*>( &(ostringstream() << width) )->str()); 
	header.append(" ");
	header.append(static_cast<ostringstream*>( &(ostringstream() << height) )->str());
	header.append(" ");
	header.append(static_cast<ostringstream*>( &(ostringstream() << nzentries) )->str());
	header.append(" ");
	header.append(symmetry);

	targetFile << header <<endl; // write out the header we just generated

	targetFile << "VAL" << endl; // write out val array
	for (int i=0; i<nzentries; i++)
	{
		targetFile << val[i] << " ";
	}
	targetFile << endl;

	targetFile << "ROWPTR" << endl; // write out row_ptr array
	for (int i=0; i<height+1; i++)
	{
		targetFile << row_ptr[i] << " ";
	}
	targetFile << endl;

	targetFile << "COLIND" << endl; // write out colind array
	for (int i=0; i<nzentries; i++)
	{
		targetFile << colind[i] << " ";
	}
	targetFile << endl;

	targetFile << "END"; // signal EOF

	return HERCMIO_STATUS_SUCCESS;

}