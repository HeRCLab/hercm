import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.paint() 

class paint(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "paint"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'col1'],
            [1, int, 'row1'],
            [2, int, 'col2'],
            [3, int, 'row2']],
        'optionalArguments': [[0, float, 'val']],
        'argumentInfo': ['column of top-left corner',
                    'row of top-left corner',
                    'column of bottom-right corner',
                    'row of bottom-right corner',
                    'new value for elements'],
        'help': """Modifies the values of the rectangular range of elements 
                whose top-left corner is (col1, row1) and whose bottom right 
                corner is (col2, row2). If val is given, elements are set equal 
                val, otherwise they are set to zero"""}

    def execute(this, arguments, WORKINGMATRIX):
        col1 = arguments[0]
        row1 = arguments[1]
        col2 = arguments[2]
        row2 = arguments[3]
        val = 0
        if len(arguments) == 5:
            val = arguments[4]

        MatrixUtils.paint(row1, row2, col1, col2, val, WORKINGMATRIX)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True