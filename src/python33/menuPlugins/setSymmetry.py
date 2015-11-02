import masterPlugin

## wrapper for libHercMatrix.hercMatrix.makeSymmetrical() and 
## .makeAsymmetrical()

class setSymmetry(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "set-symmetry"
        this.aliases = ["setsym"]
        this.commandInfo = {'requiredArguments': [[0, str, 'symmetry']],
            'optionalArguments': [[0, str, 'method']],
            'argumentInfo': ['the new symmetry for the matrix',
                    'the algorithm to use'],
            'help': """ Makes the matrix symmetric or asymmetric, modifying COO 
                    data appropriately. By default, uses the truncate method. 
                    Available methods are: truncate - fastest, all elements from
                    the bottom triangle are removed/overwritten as needed; add -
                    all elements in in the lower triangle are added to 
                    corresponding elements in the upper triangle (asym->sym) OR 
                    all elements in the upper triangle are added to the 
                    corresponding elements in the lower (sym->asym); smart - 
                    only overwrites values with are zero, very slow"""}

    def execute(this, arguments, WORKINGMATRIX):
        newSymmetry = arguments[0]
        method = 'truncate'
        if len(arguments) == 2:
            method = arguments[1]


        
        if newSymmetry in ['sym', 'symmetric', 'symmetrical']:
            symmetry = 'SYM'
        else:
            symmetry = 'ASYM'
        
        if symmetry != WORKINGMATRIX.symmetry:
            if symmetry == 'SYM':
                WORKINGMATRIX.makeSymmetrical(method)
            elif symmetry == 'ASYM':
                WORKINGMATRIX.makeAsymmetrical(method)
        
        WORKINGMATRIX.symmetry = symmetry
        WORKINGMATRIX.makeRowMajor()
        WORKINGMATRIX.removeZeros()

    def validate(this, arguments, WORKINGMATRIX):
        newSymmetry = arguments[0].lower()
        method = 'truncate'
        if len(arguments) == 2:
            method = arguments[1].lower()

        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if method not in ['truncate', 'add', 'smart']:
            print("ERROR: method {0} is not one of `truncate`, `add`, `smart`"
                .format(method))
            return False
    
        validOptions = ['sym', 'asym', 'asymmetric', 'symmetric',
          'symmetrical', 'asymmetrical']

        
        if newSymmetry not in validOptions:
            print("ERROR: {0} is not a valid symmetry".format(newSymmetry))
            return False

       
        return True