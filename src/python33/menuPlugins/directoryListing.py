import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.printDirectoryListing()
##


class directoryListing(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "list-directory"
        this.aliases = ["ls","dir"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': [[0, str, "path"]],
            'argumentInfo': ["the path to get a listing for - default is ./"],
            'help': 'Prints a directory listing for the specified path'}

    def execute(this, arguments, WORKINGMATRIX):
        target = "."
        if len(arguments) == 1:
            target = arguments[0]
        MatrixUtils.printDirectoryListing(target)