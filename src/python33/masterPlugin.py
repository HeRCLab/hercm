
from yapsy.IPlugin import IPlugin
import logging

## @package masterPlugin
# provides a master plug in class which all other menu plug ins will inherit
# from

class masterPlugin(IPlugin):

    ## Default constructor 
    # sets command and aliases to none, and creates an empty commandInfo
    def __init__(this):
        this.command = None
        this.aliases = None  # list of strings - aliases to command
        this.commandInfo = {'argumentInfo': None,  # commandInfo for this item
            'help': "",
            'optionalArguments': None,
            'requiredArguments': None}

    ## Run this command (stub)
    # Should be overloaded by the child 
    # 
    # @param[in] arguments arguments already parsed by processArguments and
    # validated by validate()
    # @param[in,out] instance of libHercMatrix.hercMatrix for the command to
    # operate on, if needed
    # 
    # @returns None 
    def execute(this, arguments, WORKINGMATRIX):
        pass 

    ## called before execute to validate arguments
    # Child classes should overload this and also call super().validate() 
    # 
    # This stub fails only if command is uninitialized 
    # 
    # @param[in] arguments list of strings - arguments already parsed by 
    # processArguments()
    # @param[in] WORKINGMATRIX instance of libHercMatrix.hercMatrix which
    # the command may use for validation, if needed
    # 
    # @returns False if validation fails
    # @returns True if validation passes
    def validate(this, arguments, WORKINGMATRIX):
        if this.command is None:
            logging.warning("{0}.command is None".format(this))
            return False
        return True


    ## Process arguments for later use by command
    # This function should typecast all arguments (if needed) and verify any 
    # required arguments are present. Child classes are strongly discouraged
    # from overriding this method
    # 
    # @param[in] arguments split arguments, not including the command 
    # 
    # @returns arguments typecasted and verified as a list of objects
    # @returns None on error

    def processArguments(this, arguments):

        if this.commandInfo['requiredArguments'] != None:
            if len(arguments) < len(this.commandInfo['requiredArguments']):
                print("ERROR, incorrect number of arguments for {0}"
                      .format(this.command))
                firstMisingArgument = len(arguments)
                for i in range(firstMisingArgument,
                        len(this.commandInfo['requiredArguments'])):
                    print("Missing argument '{1}' at position {0}".format(i,
                            this.commandInfo['requiredArguments'][i][2]))
                return None

            for arg in this.commandInfo['requiredArguments']:
                try:
                    arguments[arg[0]] = arg[1](arguments[arg[0]])
                except Exception:
                    print("""ERROR: argument {0} was present, but is not of 
 required type {1}""".format(arg[0], str(arg[1])))
                    return None

        if this.commandInfo['optionalArguments'] != None:
            for arg in this.commandInfo['optionalArguments']:
                argOffset = 0
                if this.commandInfo['requiredArguments'] != None:
                    argOffset = len(this.commandInfo['requiredArguments'])
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
                    return None
        return arguments


    ## Prints the help text for this command 
    # uses commandInfo to generate a help message for this command. Child 
    # classes are discouraged from overloading this function

    def printHelp(this): 
        import textwrap
        
        print("-" * 40)
        print(this.command, end='')

        if this.commandInfo['requiredArguments'] != None:
            for arg in this.commandInfo['requiredArguments']:
                print(' [' + arg[2] + '] ', end='')
        if this.commandInfo['optionalArguments'] != None:
            for arg in this.commandInfo['optionalArguments']:
                print(' (' + arg[2] + ') ', end='')
        print("\n-- arguments --")
        argCounter = 0
        if this.commandInfo['requiredArguments'] != None:
            for arg in this.commandInfo['requiredArguments']:
                print('    [' + arg[2] + '] ' + str(arg[1]) + ' - ' + ' ' +
                      this.commandInfo['argumentInfo'][argCounter])
                argCounter += 1
        if this.commandInfo['optionalArguments'] != None:
            for arg in this.commandInfo['optionalArguments']:
                try:
                    print('    (' + arg[2] + ') - ' + str(arg[1]) + ' ' +
                          this.commandInfo['argumentInfo'][argCounter])
                except IndexError:
                    print("WARNING: commandInfo of {0} malformed"
                          .format(this.command))
                argCounter += 1

        print("-- use --")
        # get rid of extraneous white space
        helpText = this.commandInfo['help'].split()
        helpText = ' '.join(helpText) # put back just spaces 
        # wrap text, then print line by line
        for line in textwrap.wrap(helpText):
            print('    ' + line)

        if this.aliases is not None:
            print("-- aliases --")
            for alias in this.aliases:
                print(alias, end="")
                if this.aliases.index(alias) != len(this.aliases) -1:
                    print(", ", end="")
                else:
                    print("")
