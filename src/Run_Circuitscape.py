import json

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

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        for parameter in parameters:
            schema_for_parameter = self.schema['properties'][parameter.name]
            if "enum" in schema_for_parameter:
                parameter.filter.list = schema_for_parameter["enum"]
        return parameters

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return True