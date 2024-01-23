"""This file contains code to convert the schemas for CS and OS into lists
of arcpy parameters to be consumed by the tools. The schemas are loaded more
or less exactly as written. The majority of the code here is to 
1) Convert types in the schema to corresponding parameter types
2) Categorize parameters based on where we want them to fall in the GUI. This
could be done in the schema in some way, but I think that would only be 
needed if these categories were used somewhere else.
"""
import json
from pathlib import Path

from arcpy import Parameter


def load_circuitscape_schema():
    return _load_schema("schema.json")


def load_omniscape_schema():
    return _load_schema("omniscape-schema.json")


def _load_schema(file: str) -> dict:
    schema_path = Path(__file__).parent / "circuitscape-schema" / file
    with schema_path.open() as f:
        schema = json.load(f)
    return schema


def load_omniscape_parameters(schema: dict) -> list[Parameter]:
    """Categorize OS parameters. This was done similarly to how they are
    layed out in the OS documentation."""
    schema["properties"]["threads"] = dict(
        name="Number of threads", type="integer", default=1
    )

    categories = {
        "General": [
            "project_name",
            "resistance_file",
            "source_file",
            "radius",
            "block_size",
        ],
        "Resistance options": [
            "resistance_is_conductance",
            "source_from_resistance",
            "r_cutoff",
            "reclassify_resistance",
            "reclass_table",
            "write_reclassified_resistance",
        ],
        "Advanced options": [
            "allow_different_projections",
            "buffer",
            "source_threshold",
        ],
        "Calculation options": [
            "connect_four_neighbors_only",
            "mask_nodata",
            "parallelize",
            "threads",
            "parallel_batch_size",
            "precision",
            "solver",
        ],
        "Mapping options": [
            "calc_normalized_current",
            "calc_flow_potential",
            "write_raw_currmap",
            "write_as_tif",
        ],
        "Conditional options": [
            "conditional",
            "n_conditions",
            "condition1_file",
            "comparison1",
            "condition1_lower",
            "condition1_upper",
            "condition2_file",
            "comparison2",
            "condition2_lower",
            "condition2_upper",
            "compare_to_future",
            "condition1_future_file",
            "condition2_future_file",
        ],
    }
    default_categories = ["General"]
    outputs = ["project_name"]
    return _load_parameters(schema, categories, default_categories, outputs)


def load_circuitscape_parameters(schema: dict) -> list[Parameter]:
    """Load and categorize CS parameters. The categories were derived from
    the documentation but also how they were layed out in the old CS 4 GUI
    tool."""
    categories = {
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
    default_categories = ["General", "Resistance options", "Output"]
    outputs = ["output_file"]
    return _load_parameters(schema, categories, default_categories, outputs)


def _load_parameters(
    schema, categories, default_categories, outputs
) -> list[Parameter]:
    parameters = []
    for category, parameter_keys in categories.items():
        for parameter_key in parameter_keys:
            name = parameter_key
            parameter = _load_parameter(
                name=name,
                info=schema["properties"][name],
                required=name in schema["required"],
                category=None if category in default_categories else category,
                direction="Output" if name in outputs else None,
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
    )

    p.value = info.get("default")
    p.description = info.get("description")
    return p


def _get_type(info: dict) -> str:
    """Set the (most) appropriate parameter type based on the schema types."""
    type = None
    if info["name"] == "Project name":
        type = "DEFolder"
    elif "type" in info:
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
        integer="GPLong",
    )
    return lookup.get(basetype, default)


def _get_defined_type(refstring: str) -> str:
    if "path" in refstring:
        type = "DEFile"
    elif "folder" in refstring:
        type = "DEFolder"
    elif "integer" in refstring:
        type = "GPDouble"
    return type
