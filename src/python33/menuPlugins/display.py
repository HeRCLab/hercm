import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.display()
#
 

class display(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "display"
        this.aliases = ["d"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': [[0, int, 'height'], [1, int, 'width']],
            'argumentInfo': ['maximum number of elemets to display vertically',
                    'maximum number of elements to display horizontally'],
            'help': """Displays a visualization of the matrix. If the matrix is 
                    very large, only the corners will be displayed"""}

    def execute(this, arguments, WORKINGMATRIX):
        height = 10
        width = 10
        if len(arguments) == 2:
            height = arguments[0]
            width = arguments[1]

        try:
            MatrixUtils.displayMatrix(WORKINGMATRIX, height, width)
        except ValueError:
            print("ERROR: height and width must be even numbers!")

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True