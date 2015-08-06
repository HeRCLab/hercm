hercmio.so: hercmio.cpp hercmio.hpp
	g++ -w -fPIC -shared hercmio.cpp -o hecmio.so 
hercmio.o: 
	g++ -w -c hercmio.cpp -o hercmio.o
hercmio-example: hercmio.o 
	g++ hercmio-example.cpp hercmio.o -o hercmio-example 