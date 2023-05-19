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
    _categories = {
        "General": ["data_type", "scenario"],
        "Resistance options": ["habitat_file", "habitat_map_is_resistances"],
        "Output": ["output_file", "write_cur_maps"],
        "Pairwise options": ["point_file", "polygon_file"],
        "Advanced options": ["source_file", "ground_file"],
        "Logging": ["log_level", "log_file"],
        "Calculation options": [
            "connect_four_neighbors_only",
            "connect_using_avg_resistances",
            "preemptive_memory_release",
            "low_memory_mode",
            "use_unit_currents",
            "use_direct_grounds",
        ],
        "Mapping options": [
            "write_max_cur_maps",
            "write_cum_cur_map_only",
            "set_focal_node_currents_to_zero",
            "compress_grids",
            "log_transform_maps",
        ],
        "Optional inputs": [
            "use_mask",
            "mask_file",
            "use_variable_source_strengths",
            "variable_source_file",
            "use_included_pairs",
            "included_pairs_file",
        ],
    }
    _default_categories = ["General", "Resistance options", "Output"]

    parameters = []
    for category, parameter_keys in _categories.items():
        for parameter_key in parameter_keys:
            name = parameter_key
            parameter = _load_parameter(
                name=name,
                info=schema["properties"][name],
                required=name in schema["required"],
                category=None if category in _default_categories else category,
            )
            parameters.append(parameter)
    return parameters


def _load_parameter(name: str, info: dict, required: bool, **kwargs) -> Parameter:
    p = Parameter(
        name=name,
        displayName=info.get("name"),
        datatype=_get_type(info),
        parameterType="Required" if required else "Optional",
        **kwargs
        # enabled = None,
    )

    p.value = info.get("default")
    return p


def _get_type(info: dict) -> str:
    type = None
    if "type" in info:
        type = _get_base_type(info["type"])
    elif "$ref" in info:
        type = _get_defined_type(info["$ref"])
    return type


def _get_base_type(basetype: str, default: "GPType" = str) -> str:
    lookup = dict(
        boolean="GPBoolean",
        # Or could be GPLong, but this handles all numbers
        number="GPDouble",
        string="GPString",
    )
    return lookup.get(basetype, default)


def _get_defined_type(refstring: str) -> str:
    if "path" in refstring:
        type = "DEFile"
    elif "folder" in refstring:
        type = "DEFolder"
    return type
