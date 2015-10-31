import masterPlugin

## Prints information about the matrix
#
# Prints information about the working matrix to the screen, including 
# dimensions, number of non zero entries, symmetry, and verification sum

class info(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "info"
        this.aliases = None
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Prints information about the loaded matrix'}

    def execute(this, arguments, WORKINGMATRIX):
        height       = WORKINGMATRIX.height
        width        = WORKINGMATRIX.width
        nzentries    = WORKINGMATRIX.nzentries
        symmetry     = WORKINGMATRIX.symmetry
        verification = WORKINGMATRIX.verification
    
        print("""- matrix properties -
height (number of rows) - {0}
width (number of cols)  - {1}
non zero elements - - - - {2} 
symmetry  - - - - - - - - {3}
verification  - - - - - - {4} 
- end matrix properties -""".format(height,
                                    width,
                                    nzentries,
                                    symmetry,
                                    verification))

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        
        return True