import masterPlugin

## Prints the value of the matrix at a specified col, row pair


class value(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "value"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'column'],
                                                  [1, int, 'row']],
                            'optionalArguments': None,
                            'argumentInfo': ['column of desired element', 'row of desired element'],
                            'help': 'display the value at column, row'}

    def execute(this, arguments, WORKINGMATRIX):
        row = arguments[1]
        col = arguments[0]
        print("value of col {1}, row {0}:".format(row, col),
              WORKINGMATRIX.getValue(row, col))

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True
