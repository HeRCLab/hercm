
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import BXFUtils
import yaml
import pprint


WORKINGMATRIX = libHercMatrix.hercMatrix()
commandInfoStream = open("commandInfo.yaml", 'r')
commandInfo = yaml.load(commandInfoStream)
commandInfoStream.close()
pp = pprint.PrettyPrinter()


def main(override=None):
    # override will be parsted instead of the user's input, if specified

    global WORKINGMATRIX
    global commandInfo

    if override is None:
        usrIn = input("> ")
    else:
        usrIn = override
        logging.warning("override functionality for main() is going away soon")

    usrIn = usrIn.rstrip()
    splitInput = usrIn.split()
    try:
        command = splitInput[0]
        arguments = splitInput[1:]
    except IndexError:
        return

    if command not in commandInfo:
        print("WARNING: command is not in commandInfo, cannot check required " +
              "arguments!")
    else:
        if commandInfo[command]['requiredArguments'] != None:
            if len(arguments) < len(commandInfo[command]['requiredArguments']):
                print("ERROR, incorrect number of arguments for {0}"
                      .format(command))
                firstMisingArgument = len(arguments)
                for i in range(firstMisingArgument,
                        len(commandInfo[command]['requiredArguments'])):
                    print("Missing argument '{1}' at position {0}".format(i,
                            commandInfo[command]['requiredArguments'][i][2]))
                return

            for arg in commandInfo[command]['requiredArguments']:
                try:
                    arguments[arg[0]] = arg[1](arguments[arg[0]])
                except Exception:
                    print("""ERROR: argument {0} was present, but is not of 
 required type {1}""".format(arg[0], str(arg[1])))
                    return

        if commandInfo[command]['optionalArguments'] != None:
            for arg in commandInfo[command]['optionalArguments']:
                argOffset = 0
                if commandInfo[command]['requiredArguments'] != None:
                    argOffset = len(commandInfo[command]['requiredArguments'])
                if argOffset + arg[0] > (len(arguments) - 1):
                    # this optional arg was not given
                    break

                try:
                    arguments[arg[0] + argOffset] = \
                        arg[1](arguments[arg[0] + argOffset])

                except IndexError:
                    print("WARNING: IndexError while accessing index {0} of {1}"
                          .format(arg[0] + argOffset, arguments))
                except Exception:
                    print("""ERROR: argument {0} was present, but of type {1} 
 not required type {2}""".format(arg[0] + argOffset,
                                 type(arguments[arg[0] + argOffset]),
                                 str(arg[1])))
                    return

    if command == 'help':
        if len(arguments) > 0:
            BXFUtils.printHelp(commandInfo, arguments[0])
        else:
            BXFUtils.printHelp(commandInfo)

    elif command == 'exit':
        exit()

    elif command == 'load':
        WORKINGMATRIX = BXFUtils.load(arguments[0], arguments[1])

        if WORKINGMATRIX.symmetry == 'SYM':
            print("INFO: matrix is symmetric, bottom triangle should be only "
                  + "zeros")

    elif command == 'write':
        fileName = arguments[0]
        fileFormat = arguments[1]
        try:
            BXFUtils.write(fileName, fileFormat, WORKINGMATRIX)
        except FileExistsError:
            print("ERROR: file already exists!")
            return

    elif command == 'info':
        BXFUtils.printInfo(WORKINGMATRIX)

    elif command == 'display':
        if len(arguments) == 2:
            height = arguments[0]
            width = arguments[1]
            try:
                BXFUtils.displayMatrix(WORKINGMATRIX, height, width)
            except ValueError:
                print("ERROR: display dimensions must be even numbers!")
        else:
            BXFUtils.displayMatrix(WORKINGMATRIX)

    elif command == 'csrdisplay':
        if len(arguments) == 2:
            BXFUtils.printCSR(WORKINGMATRIX, arguments[0], arguments[1])
        else:
            BXFUtils.printCSR(WORKINGMATRIX)

    elif command == 'raw':
        BXFUtils.printRaw(WORKINGMATRIX)

    elif command == 'value':
        BXFUtils.printValue(arguments[0], arguments[1], WORKINGMATRIX)

    elif command == 'row':
        BXFUtils.printRow(arguments[0], WORKINGMATRIX)

    elif command == 'col':
        BXFUtils.printCol(arguments[0], WORKINGMATRIX)

    elif command == 'range':
        col1 = arguments[0]
        col2 = arguments[2]
        row1 = arguments[1]
        row2 = arguments[3]
        BXFUtils.printRange(row1, row2, col1, col2, WORKINGMATRIX)

    elif command == 'touch':
        BXFUtils.touch(arguments[0], arguments[1], arguments[2], WORKINGMATRIX)

    elif command == 'paint':
        val = 0.0
        col1 = arguments[0]
        row1 = arguments[1]
        col2 = arguments[2]
        row2 = arguments[3]
        if len(arguments) == 5:
            val = arguments[4]

        BXFUtils.paint(row1, row2, col1, col2, val, WORKINGMATRIX)

    elif command == 'paint-diag':

        begin = arguments[0]
        end = arguments[1]
        spread = arguments[2]
        val = arguments[3]
        offset = 0
        if len(arguments) == 5:
            offset = arguments[4]

        BXFUtils.paintDiagonal(begin, end, spread, val, WORKINGMATRIX, offset)

    elif command == 'row-major':
        print("making matrix row major, this may take some time, standby...")
        WORKINGMATRIX.makeRowMajor()
        print("done")

    elif command == 'rmzeros':
        print("removing zeros, standby...")
        WORKINGMATRIX.removeZeros()
        print("done")

    elif command == 'setdims':
        if arguments[1] > arguments[0]:
            # TODO: fix this
            print("WARNING: height is greater than width, this will probably " +
                  "break several commands (this is a known bug)")
        BXFUtils.setDims(arguments[1], arguments[0], WORKINGMATRIX)

    elif command == 'setsym':
        symmetry = arguments[0]
        method = 'truncate'
        if len(arguments) == 2:
            method = arguments[1]
        BXFUtils.setSymmetry(symmetry, WORKINGMATRIX, method)

    elif command == 'init':
        height = arguments[1]
        width = arguments[0]
        val = 0
        if len(arguments) == 3:
            val = arguments[2]
        BXFUtils.initilize(height, width, WORKINGMATRIX, val)

    elif command == 'shell':
        print("Entering python interactive debug shell...")
        print("Enter \"runMain()\" to return to normal execution")
        import pdb
        pdb.set_trace()

    elif command == 'check-symmetry':
        BXFUtils.printSymmetry(WORKINGMATRIX)

    elif command == 'gen-verification':
        BXFUtils.generateVerification(WORKINGMATRIX)

    elif command == 'plot':
        BXFUtils.plot(WORKINGMATRIX)

    elif command == "transpose":
        WORKINGMATRIX.transpose()

    elif command == "ls":
        directory = './'
        if len(arguments) == 1:
            directory = arguments[0]
        BXFUtils.printDirectoryListing(directory)

    elif command == "pwd":
        print(os.getcwd())

    elif command == "head":
        lines = 10
        path = arguments[0]
        if len(arguments) == 2:
            lines = arguments[1]

        BXFUtils.head(path, lines)

    elif command == "cat":
        BXFUtils.cat(arguments[0])

    elif command == "cd":
        BXFUtils.changeDirectory(arguments[0])

    elif command == "convert":
        BXFUtils.convert(
            arguments[0], arguments[2], arguments[1], arguments[3])

    elif command == 'check-tril':
        if WORKINGMATRIX.checkLowerTriangle():
            print("There are NO nonzero elements in the lower triangle")
        else:
            print("There ARE nonzero elements in the lower triangle")

    else:
        print("ERROR: Command not recognized")


def runMain():
    while True:
        main()

print("welcome to BXFExplorer. Enter \"help\" for help")
runMain()
