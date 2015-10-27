
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


def main(override=None):
    # override will be parsted instead of the user's input, if specified

    import pprint
    pp = pprint.PrettyPrinter()

    if override is None:
        usrIn = input("> ")
    else:
        usrIn = override

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
        try:
            BXFUtils.load(arguments[0], arguments[1], SC)
        except AttributeError:
            print("ERROR: file does not exist")
            return
        except OSError:
            print("ERROR: file does not exist")
        except KeyError:
            print("ERROR: requested format is not supported")

        print("done reading matrix")
        if SC.HSM.symmetry == 'SYM':
            print("INFO: matrix is symmetric, bottom triangle should be only "
                  + "zeros")

    elif command == 'write':
        fileName = arguments[0]
        fileFormat = arguments[1]
        try:
            BXFUtils.write(fileName, fileFormat, SC)
        except FileExistsError:
            print("ERROR: file already exists!")
            return

    elif command == 'info':
        BXFUtils.printInfo(SC.HSM)

    elif command == 'display':
        if len(arguments) == 2:
            height = arguments[0]
            width = arguments[1]
            try:
                BXFUtils.displayMatrix(SC.HSM, height, width)
            except ValueError:
                print("ERROR: display dimensions must be even numbers!")
        else:
            BXFUtils.displayMatrix(SC.HSM)

    elif command == 'csrdisplay':
        if len(arguments) == 2:
            BXFUtils.printCSR(SC.HSM, arguments[0], arguments[1])
        else:
            BXFUtils.printCSR(SC.HSM)

    elif command == 'raw':
        BXFUtils.printRaw(SC.HSM)

    elif command == 'value':
        BXFUtils.printValue(arguments[0], arguments[1], SC.HSM)

    elif command == 'row':
        BXFUtils.printRow(arguments[0], SC.HSM)

    elif command == 'col':
        BXFUtils.printCol(arguments[0], SC.HSM)

    elif command == 'range':
        col1 = arguments[0]
        col2 = arguments[2]
        row1 = arguments[1]
        row2 = arguments[3]
        BXFUtils.printRange(row1, row2, col1, col2, SC.HSM)

    elif command == 'touch':
        BXFUtils.touch(arguments[0], arguments[1], arguments[2], SC.HSM)

    elif command == 'paint':
        val = 0.0
        col1 = arguments[0]
        row1 = arguments[1]
        col2 = arguments[2]
        row2 = arguments[3]
        if len(arguments) == 5:
            val = arguments[4]

        BXFUtils.paint(row1, row2, col1, col2, val, SC.HSM)

    elif command == 'paint-diag':

        begin = arguments[0]
        end = arguments[1]
        spread = arguments[2]
        val = arguments[3]
        offset = 0
        if len(arguments) == 5:
            offset = arguments[4]

        BXFUtils.paintDiagonal(begin, end, spread, val, SC.HSM, offset)

    elif command == 'row-major':
        print("making matrix row major, this may take some time, standby...")
        SC.HSM.makeRowMajor()
        print("done")

    elif command == 'rmzeros':
        print("removing zeros, standby...")
        SC.HSM.removeZeros()
        print("done")

    elif command == 'setdims':
        if arguments[1] > arguments[0]:
            # TODO: fix this
            print("WARNING: height is greater than width, this will probably " +
                  "break several commands (this is a known bug)")
        BXFUtils.setDims(arguments[1], arguments[0], SC.HSM)

    elif command == 'setsym':
        symmetry = arguments[0]
        method = 'truncate'
        if len(arguments) == 2:
            method = arguments[1]
        BXFUtils.setSymmetry(symmetry, SC.HSM, method)

    elif command == 'init':
        height = arguments[1]
        width = arguments[0]
        val = 0
        if len(arguments) == 3:
            val = arguments[2]
        BXFUtils.initilize(height, width, SC.HSM, val)

    elif command == 'shell':
        print("Entering python interactive debug shell...")
        print("Enter \"runMain()\" to return to normal execution")
        import pdb
        pdb.set_trace()

    elif command == 'check-symmetry':
        BXFUtils.printSymmetry(SC.HSM)

    elif command == 'gen-verification':
        BXFUtils.generateVerification(SC.HERCMIO, SC.HSM)

    elif command == 'plot':
        BXFUtils.plot(SC.HSM)

    elif command == "transpose":
        SC.HSM.transpose()

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
        if SC.HSM.checkLowerTriangle():
            print("There are NO nonzero elements in the lower triangle")
        else:
            print("There ARE nonzero elements in the lower triangle")

    else:
        print("ERROR: Command not recognized")


def runMain():
    while True:
        main()

print("welcome to BXFExplorer. Enter \"help\" for help")
SC = libHercmIO.hercmIO()
commandInfoStream = open("commandInfo.yaml", 'r')
commandInfo = yaml.load(commandInfoStream)
commandInfoStream.close() 
runMain()
