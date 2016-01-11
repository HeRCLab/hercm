bxfio.a: # static library  
	gcc -c bxfio.c -o bxfio.o
	ar rcs bxfio.a bxfio.o
	rm bxfio.o
sample: bxfio.a
	gcc sample.c bxfio.a -o sample
