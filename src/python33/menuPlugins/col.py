import masterPlugin

## Prints all elements in the specified column


class col(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "col"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'col']],
            'optionalArguments': None,
            'argumentInfo': ['the row to display'],
            'help': 'Displays all elements in the specified column'}

    def execute(this, arguments, WORKINGMATRIX):
        col = arguments[0]

        for index in range(0, WORKINGMATRIX.nzentries - 1):
            try:
                if WORKINGMATRIX.getValue(index, col) != 0:
                    print("col {0}, row {1}: {2}"
                          .format(col, index, WORKINGMATRIX.getValue(index, col)))
            except IndexError:
                pass

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True
