"""This is the entrypoint (from Arc Pro's perspective) for the tool and 
is what is loaded when a user selects "Add Toolbox".
"""
from tools import Run_Circuitscape, Run_Omniscape


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file). It containes two tools."""
        self.label = "Circuitscape"
        self.alias = "Circuitscape"

        self.tools = [Run_Circuitscape, Run_Omniscape]

