import masterPlugin

## Plot the working matrix with matplotlib 

class plot(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "plot"
        this.aliases = None
        this.commandInfo= {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Plots the matrix graphically with matplotlib'}

    def execute(this, arguments, WORKINGMATRIX):
        import matplotlib
        import matplotlib.pyplot

        matrix = WORKINGMATRIX.getInFormat('coo')

        matplotlib.pyplot.spy(matrix)
        matplotlib.pyplot.show()