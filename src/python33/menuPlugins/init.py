import masterPlugin
import MatrixUtils


## Wrapper for MatrixUtils.initialize()

class init(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "init"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, int, 'with'],
                [1, int, 'height']],
            'optionalArguments': [[0, float, 'val']],
            'argumentInfo': ['the width for the new matrix',
                'the height for the new matrix',
                'the value for all elements in the new matrix'],
            'help': """Creates a new matrix with specified dimensions, with all 
                elements initialized to zero, or to val if it is given"""}

    def execute(this, arguments, WORKINGMATRIX):
        width = arguments[0]
        height = arguments[1]
        val = 0
        if len(arguments) == 3:
            val = arguments[2]

        MatrixUtils.initialize(height, width, WORKINGMATRIX, val)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if arguments[0] <= 0:
            print("ERROR: width must be a positive integer")
            return False
        if arguments[1] <= 0:
            print("ERROR: height must be a positive integer")
            return False

        return True
