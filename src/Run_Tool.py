import json
import os
from pathlib import Path
from typing import Callable, List

from arcpy import Parameter

class Run_Tool(object):
    def __init__(self, label:str, description:str, runner:Callable):
        """Define the tool (tool name is the name of the class)."""
        self.label = label
        self.description = description
        self.runner = runner
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = self.initial_params
        return params

    def updateParameters(self, parameters: List[Parameter]):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        for parameter in parameters:
            schema_for_parameter = self.schema["properties"][parameter.name]
            if "enum" in schema_for_parameter:
                parameter.filter.list = schema_for_parameter["enum"]
        return parameters

    def updateMessages(self, parameters: List[Parameter]):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters: List[Parameter], messages):
        """The source code of the tool."""

        messages.addMessage("running")
        messages.addMessage(os.path.realpath(__file__))
        config_file = Path(__file__).resolve().parent / "test.ini"
        with open(config_file, "w") as dst:
            for parameter in parameters:
                if parameter.value is not None:
                    dst.write(f"{parameter.name} = {parameter.value}\n")

        self.runner(config_file, messages)
        return True
