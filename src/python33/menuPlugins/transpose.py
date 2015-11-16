import masterPlugin

## wrapper for libHercMatrix.hercMatrix.transpose()

class transpose(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "transpose"
        this.aliases = None
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Reflects the matrix about the diagonal'}

    def execute(this, arguments, WORKINGMATRIX):
        print("performing matrix transpose...")
        WORKINGMATRIX.transpose()
        print("done")

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if WORKINGMATRIX.symmetry == "SYM":
            print("ERROR: matrix is already symmetric, performing transpose " +
                "would produce non-compliant output")
            return False 

        return True 