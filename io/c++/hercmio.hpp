#include <string>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <sstream>
#include <typeinfo>
#include <cmath>
#include <algorithm>
#include <iterator>

#ifndef HERCMIO_H
#define HERCMIO_H

#define HERCMIO_STATUS_FAILURE 100
#define HERCMIO_STATUS_SUCCESS 101

using namespace std;


bool checkVectorForString(vector<string>);
int stringToInt(string);
float stringToFloat(string);
vector<string> split(string, char);
int readHercmHeader(string, int&, int&, int&, string&, float&);
int readHercm(string, float *, int *, int *);
int writeHercm(string, int, int, int, float *, int *, int *, string);
int cooToCsr(int *, int *, float *, int *, int, int);
int makeRowMajor(int *, int *, float *, int);
#endif