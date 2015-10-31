import masterPlugin

## blank sample plugin
#
# Doesn't actually do anything, just demonstrates how to do plugins. 

class sample(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "sample"
        this.aliases = None
        this.commandInfo['help'] = """This command does not do anything, it is 
            used to demonstrate and test the command system."""

    def execute(this, arguments):
        print("This is just a sample command, it doesn't actually do anything")

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        print("If this was a real command, validation would be done here")
        return True