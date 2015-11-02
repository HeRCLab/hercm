import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.setDims()

class setdims(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "setdims"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'with'],
                [1, int, 'height']],
        'optionalArguments': None,
        'argumentInfo': ['the new width for the matrix',
            'the new height for the matrix'],
        'help': 'Changes the dimensions of the matrix, truncating elements ' +
                    'which become out of bounds'}

    def execute(this, arguments, WORKINGMATRIX):
        width = arguments[0]
        height = arguments[1]
        print("Setting dimensions of matrix to {0} columns by {1} rows..."
            .format(width, height))
        MatrixUtils.setDims(height, width, WORKINGMATRIX)
        print("done")


    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True