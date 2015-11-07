
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import pprint
from yapsy.PluginManager import PluginManager
import traceback
import sys


WORKINGMATRIX = libHercMatrix.hercMatrix()
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
                    return
            print("No help message found for command {0}".format(arguments[0]))
            return
        else:
            for item in menuItems:
                item.printHelp()

        print("\n" * 5)
        print("-- Special Commands --")
        print("help (command) - print all help messages, or print help for a ")
        print("specific command")
        print("-" * 20)
        print("list-plugins - list all loaded menu plugins (commands)")
        print("-" * 20)
        print("reload-plugins - (BUG: not currently working) reload all menu ")
        print("plugins")
        print("-" * 20)
        print("traceback - print the traceback for the most recent failed ")
        print("command")

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
                    print("\n" * 4)
                    print("Command halted by keyboard interrupt")
                except Exception as e:
                    logging.warning("Command halted because of exception: {0}"
                                    .format(e))
                    currentTraceBack = traceback.format_exc()
                if NEWWM is not None:  # ugly workaround because python refuses
                                      # to pass WORKINGMATRIX by reference
                    WORKINGMATRIX = NEWWM
            else:
                print("ERROR: command validation failed")
            return

    else:
        print("ERROR: command '{0}' not found!".format(command))


def runMain():
    while True:
        main()

loadPlugins()
if len(sys.argv) == 1:
    print("welcome to Herc Explorer. Enter \"help\" for help")
    runMain()
else:
    main(' '.join(sys.argv[1:]))
    runMain()


