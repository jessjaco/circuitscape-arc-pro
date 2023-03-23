from importlib import reload

from Run_Circuitscape import Run_Circuitscape


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Circuitscape"
        self.alias = "Circuitscape"

        # List of tool classes associated with this toolbox
        self.tools = [Run_Circuitscape]