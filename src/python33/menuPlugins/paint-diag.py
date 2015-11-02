import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.paint-diag

class paintDiag(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "paint-diag"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'begin'],
            [1, int, 'end'],
            [2, int, 'spread'],
            [3, float, 'val']],
        'optionalArguments': [[0, int, 'offset']],
        'argumentInfo': ['the first column of the diagonal',
                    'last column of the diagonal',
                    'number of indices on each side of the diagonal to paint',
                    'value to paint',
                    'number of indices to offset the diagonal horizontally'],
        'help': """sets all elements along the diagonal of the matrix to val, as
                well as spread values to either side of the diagonal, starting 
                column begin, and ending with column end. The diagonal can also 
                be offset by offset elements to the left or right """
    }

    def execute(this, arguments, WORKINGMATRIX):
        begin = arguments[0]
        end = arguments[1]
        spread = arguments[2]
        val = arguments[3]
        offset = 0
        if len(arguments) == 5:
            offset = arguments[4]

        MatrixUtils.paintDiagonal(begin,
            end,
            spread,
            val,
            WORKINGMATRIX,
            offset)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True