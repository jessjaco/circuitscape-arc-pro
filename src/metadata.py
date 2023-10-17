"""This module writes the xml metadata for tools. For now, it is using a subset of what is created when
a tool is loaded in Arc Pro. Note that the xmltodict package is required to create the xml, so this
cannot be run in the stock Arc Pro environment. But it does need to be. It should only be run upon
build. Also note, if you load the tool in Arc Pro the output may be overwritten.

To get this to run, follow these instructions: 
https://support.esri.com/en-us/knowledge-base/how-to-clone-a-python-environment-with-the-python-comma-000020560

1. Start Menu -> Python Command Prompt (run as administrator)
2. Clone the env: `conda create --clone arcgispro-py3 --name arcgispro-py3-circuitscape-tool`
3. Activate the clone: `activate arcgispro-py3-circuitscape-tool`
4. Add what we need: `conda install xmltodict`
5. Run this file
"""
from typing import List, Dict
from pathlib import Path

from arcpy import Parameter
from xmltodict import unparse # not in arc pro python env!

from parameters import (
    load_circuitscape_parameters, 
    load_circuitscape_schema, 
    load_omniscape_parameters, 
    load_omniscape_schema
)

def write_metadata(parameters: List, tool_name: str, output_path: Path) -> None:
    metadict = {
        "metadata": {
            "@xml:lang":"en",
            "tool": { 
                "@name":"name", 
                "@displayname": "display name",
                "@toolboxalias": "Circuitscape",
                "@xmlns": "",
                "parameters": { "params": _parse_parameters(parameters) }
            }
        }
    }
    with open(output_path, "w") as dst:
        dst.write(unparse(metadict, pretty=True))

def _parse_parameters(parameters: List) -> Dict:
    return [_parse_parameter(parameter) for parameter in parameters]

def _parse_parameter(parameter: Parameter) -> Dict:
    return {
        "@name": parameter.name,
        "@displayname": parameter.displayName,
        "@type": parameter.parameterType,
        "@direction": parameter.direction,
        "@datatype": parameter.datatype,
        "@expression": f"{{{parameter.name}}}",
        # reverse-engineered style string from some edited metadata, all this html may not be required.
        # "dialogReference": f'&lt;DIV STYLE="text-align:Left;"&gt;&lt;DIV&gt;&lt;DIV&gt;&lt;P&gt;&lt;SPAN&gt;{parameter.dialogReference}&lt;/SPAN&gt;&lt;/P&gt;&lt;/DIV&gt;&lt;/DIV&gt;&lt;/DIV&gt;'
    }

if __name__ == "__main__":
    write_metadata(
        parameters=load_circuitscape_parameters(load_circuitscape_schema()),
        tool_name="Run Circuitscape",
        output_path="src/Circuitscape.Run_Circuitscape.pyt.xml"
    )

    write_metadata(
        parameters=load_omniscape_parameters(load_omniscape_schema()),
        tool_name="Run Omniscape",
        output_path="src/Circuitscape.Run_Omniscape.pyt.xml"
    )