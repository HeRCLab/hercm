
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os





def runMain():
	while True:
		main()

print("welcome to BXFExplorer. Enter \"help\" for help")
SC = libHercmIO.hercmIO()
runMain()