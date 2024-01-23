import os
from pathlib import Path
from typing import Callable, List

from arcpy import Parameter

from parameters import (
    load_circuitscape_parameters,
    load_circuitscape_schema,
    load_omniscape_parameters,
    load_omniscape_schema,
)

from runner import run_circuitscape, run_omniscape


class Run_Tool(object):
    def __init__(
        self,
        label: str,
        description: str,
        runner: Callable,
        schema: dict,
        initial_params: list[Parameter],
        commandArgParameterNames: list = [],
    ):
        """Base class for both tools (Run Omniscape & Run Circuitscape).
        Each follows the same basic flow. First load the parameters and
        start the tool. When executed, write a config file and call the runner.
        """
        self.label = label
        self.description = description
        self.runner = runner
        self.canRunInBackground = False
        self.schema = schema
        self.initial_params = initial_params
        self.commandArgParameterNames = commandArgParameterNames

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
        """Always licensed"""
        return True

    def execute(self, parameters: List[Parameter], messages):
        """Writes the config file and runs CS or OS."""

        messages.addMessage("running")
        messages.addMessage(os.path.realpath(__file__))
        config_file = Path(__file__).resolve().parent / "last_config.ini"
        command_args = dict()
        with open(config_file, "w") as dst:
            for parameter in parameters:
                if parameter.name in self.commandArgParameterNames:
                    command_args[parameter.name] = parameter.value
                elif parameter.value is not None:
                    dst.write(f"{parameter.name} = {parameter.value}\n")

        self.runner(config_file, command_args, messages)
        return True


class Run_Circuitscape(Run_Tool):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        label = "Run Circuitscape"
        description = ""
        schema = load_circuitscape_schema()
        initial_params = load_circuitscape_parameters(schema)
        super().__init__(
            label=label,
            description=description,
            runner=run_circuitscape,
            schema=schema,
            initial_params=initial_params,
        )


class Run_Omniscape(Run_Tool):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        label = "Run Omniscape"
        description = "Run the Omniscape tool"
        schema = load_omniscape_schema()
        initial_params = load_omniscape_parameters(schema)
        super().__init__(
            label=label,
            description=description,
            runner=run_omniscape,
            commandArgParameterNames=["threads"],
            schema=schema,
            initial_params=initial_params,
        )
