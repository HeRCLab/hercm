import masterPlugin
import libBXF

## Updates the verification of the loaded matrix using
## libBXF.generateVerificationSum()


class updateVerification(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "update-verification"
        this.aliases = ["gen-verification","update-vs","uvs"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Updates the verification sum of the loaded matrix '}

    def execute(this, arguments, WORKINGMATRIX):
        try:
           newSum = libBXF.generateVerificationSum(WORKINGMATRIX)
        except TypeError:
            print("ERROR: could not generate verification sum of empty matrix")
        WORKINGMATRIX.verification = newSum