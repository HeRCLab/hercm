import masterPlugin

## Modify the value of the element at a specified col, row 

class touch(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "touch"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'col'],
            [1, int, 'row'],
            [2, float, 'val']],
        'optionalArguments': None,
        'argumentInfo': ['the column of the target element',
                'the row of the target element',
                'the new value for the element'],
        'help': 'Modifies the value of the matrix at the specified row and col'}

    def execute(this, arguments, WORKINGMATRIX):
        oldValue = None
        row = arguments[1]
        col = arguments[0]
        val = arguments[2]

        try:
            oldValue = WORKINGMATRIX.getValue(row, col)
        except IndexError:
            print("ERROR: row {0}, col {1} is out of bounds".format(row, col))
            return
        WORKINGMATRIX.setValue(row, col, val)
        print("updated value of col {1}, row {0} to {2} from {3}"
              .format(row, col, WORKINGMATRIX.getValue(row, col), oldValue))
    
        if oldValue == 0 and val != 0:
            print("WARNING: you have added a new non zero entry, COO vectors")
            print("may not be in row-major form!")

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        

        return True