import masterPlugin
import MatrixUtils

## Prints a rectangular selection of elements

class range(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "range"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'col1'],
            [1, int, 'row1'],
            [2, int, 'col2'],
            [3, int, 'row2']],
        'optionalArguments': None,
        'argumentInfo': ['column of top-left corner',
                    'row of top-left corner',
                    'column of bottom-right corner',
                    'row of bottom-right corner'],
        'help': 'Displays all elements in the rectangular region given by ' +
                    '(row1, col1), (row2, col2)'}

    def execute(this, arguments, WORKINGMATRIX):
        col1 = arguments[0]
        row1 = arguments[1]
        col2 = arguments[2]
        row2 = arguments[3]
        try:
            MatrixUtils.printRange(row1, row2, col1, col2, WORKINGMATRIX)
        except IndexError as e:
           #print("ERROR: specified endpoint(s) are out of bounds")
           print(e)
        except ValueError as e:
            #print("ERROR: col1 > col2 or row1 > row2")
            print(e)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True
