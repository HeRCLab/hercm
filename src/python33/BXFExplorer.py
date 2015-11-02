
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import yaml
import pprint
from yapsy.PluginManager import PluginManager 
import traceback



WORKINGMATRIX = libHercMatrix.hercMatrix()
commandInfoStream = open("commandInfo.yaml", 'r')
commandInfo = yaml.load(commandInfoStream)
commandInfoStream.close()
pp = pprint.PrettyPrinter()
pluginManager = PluginManager()
menuItems = []
currentTraceBack = None


def loadPlugins():
    global pluginManager 
    global menuItems

    pluginManager.setPluginPlaces(["menuPlugins"])
    pluginManager.collectPlugins()

    for plugin in pluginManager.getAllPlugins():
        menuItems.append(plugin.plugin_object)


def main(override=None):
    # override will be parsted instead of the user's input, if specified

    global WORKINGMATRIX
    global commandInfo
    global menuItems
    global pluginManager
    global currentTraceBack

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

    # special commands not implemented by plugin
    if command == 'exit':
        exit()

    elif command == 'help':
        if len(arguments) == 1:
            for item in menuItems:
                if item.command == arguments[0]:
                    item.printHelp()
        else:
            for item in menuItems:
                item.printHelp()
        
        return

    elif command == 'list-plugins':
        for item in menuItems:
            print(item.command)
        return

    elif command == 'reload-plugins':
        menuItems = []

        loadPlugins()

        return

    elif command == 'traceback':
        if currentTraceBack is None:
            print("No errors have been encountered")
        else:
            print(currentTraceBack)
        return


    # resolve alises
    for item in menuItems:
        if item.aliases is not None:
            if command in item.aliases:
                command = item.command

    NEWWM = None
    for item in menuItems:
        if item.command == command:
            arguments = item.processArguments(arguments)
            if arguments is None:
                print("ERROR: one or more missing or incorrect arguments")
                return
            if item.validate(arguments, WORKINGMATRIX):
                try:
                    NEWWM = item.execute(arguments, WORKINGMATRIX)
                except KeyboardInterrupt:
                    print("\n"*4)
                    print("Command halted by keyboard interrupt")
                except Exception as e:
                    logging.warning("Command halted because of exception: {0}"
                        .format(e))
                    currentTraceBack = traceback.format_exc()
                if NEWWM is not None: # ugly workaround because python refuses
                                      # to pass WORKINGMATRIX by reference
                    WORKINGMATRIX = NEWWM
            else:
                print("ERROR: command validation failed")
            return

    else:
        print("ERROR: command not found!")
    


def runMain():
    while True:
        main()

print("welcome to BXFExplorer. Enter \"help\" for help")
loadPlugins()
runMain()
