import masterPlugin
import MatrixUtils

## wrapper for MatrixUtils.printCSR()


class csrdisplay(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "csrdisplay"
        this.aliases = ['csr']
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': [[0, int, 'rowStart'], [1, int, 'rowEnd']],
            'argumentInfo': ['first row to display', 'last row to display'],
            'help': """Displays the matrix as raw CSR data, prompts if nzentries 
            > 25.
             if provided, will only display the CSR values between a particular
             range of rows in the matrix"""}

    def execute(this, arguments, WORKINGMATRIX):
        first = 0
        last = WORKINGMATRIX.nzentries - 1
        if len(arguments) == 2:
            first = arguments[0]
            last = arguments[1]
        MatrixUtils.printCSR(WORKINGMATRIX, first, last)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True