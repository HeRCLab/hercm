import masterPlugin

# Prints all elements in the specified row
# 
class row(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "row"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'row']],
            'optionalArguments': None,
            'argumentInfo': ['the row to display'],
            'help': 'Displays all elements in the specified row'}

    def execute(this, arguments, WORKINGMATRIX):
        row = arguments[0]
        for index in range(0, WORKINGMATRIX.nzentries - 1):
            try:
                if WORKINGMATRIX.getValue(row, index) != 0:
                    print("col {0}, row {1}: {2}"
                        .format(index, row, WORKINGMATRIX.getValue(row, index)))
            except IndexError:
                pass

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True
