import json
import os 
from typing import List

from arcpy import Parameter

from parameters import load_parameters, load_schema

class Run_Circuitscape(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Run Circuitscape"
        self.description = ""
        self.canRunInBackground = False

        self.schema = load_schema()
        self.initial_params = load_parameters(self.schema)

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = self.initial_params
        return params

    def updateParameters(self, parameters: List[Parameter]):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        for parameter in parameters:
            schema_for_parameter = self.schema['properties'][parameter.name]
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
        messages.addMessage("running")
        messages.addMessage(os.path.realpath(__file__))
        """The source code of the tool."""
        with open('test.ini', 'w') as dst:
            for parameter in parameters:
                dst.write(f"{parameter.name} = {parameter.value}\n")

        return True