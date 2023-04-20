import json
import os
from pathlib import Path

from arcpy import Parameter

def load_schema():
    schema_path = Path(__file__).parent / "circuitscape-schema" / "schema.json"
    with schema_path.open() as f:
        schema = json.load(f)
    return schema

def load_parameters(schema: dict) -> list[Parameter]:
    return [
        _load_parameter(name, info, name in schema['required']) 
        for name, info in schema['properties'].items()
    ]

def _load_parameter(name: str, info: dict, required: bool) -> Parameter:
    p =  Parameter(
        name = name,
        displayName = info.get('name'),
        datatype = _get_type(info),
        parameterType = "Required" if required else "Optional"
    )

    p.value = info.get('default')
    return p

def _get_type(info: dict) -> str:
    type = None
    if "type" in info:
        type = _get_base_type(info['type'])
    elif "$ref" in info:
        type = _get_defined_type(info['$ref'])
    return type

def _get_base_type(basetype: str, default: 'GPType'=str) -> str:
    lookup = dict(
        boolean='GPBoolean',
        # Or could be GPLong, but this handles all numbers 
        number='GPDouble',
        string='GPString'
    )
    return lookup.get(basetype, default)

def _get_defined_type(refstring: str) -> str:
    if 'path' in refstring:
        type = 'DEFile'
    return type