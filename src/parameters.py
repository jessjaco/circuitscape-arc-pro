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
    schema['properties']['number_of_threads'] = dict(name="Number of threads", "type": "integer"
        default=1)

    categories = {
        "General": ["project_name", "resistance_file", "source_file", "radius", "block_size"],
        "Resistance options": [
            "resistance_is_conductance", 
            "source_from_resistance",
            "r_cutoff",
            "reclassify_resistance",
            "reclass_table",
            "write_reclassified_resistance"
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
            "number_of_threads",
            "parallel_batch_size",
            "precision",
            "solver",
        ],
        "Mapping options": [
            "calc_normalized_current",
            "calc_flow_potential",
            "write_raw_currmap",
            "write_as_tif"
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
            "condition2_future_file"
        ] 
    }
    default_categories = ["General"]
    outputs = ["project_name"]
    return _load_parameters(schema, categories, default_categories, outputs)

def load_circuitscape_parameters(schema: dict) -> list[Parameter]:
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


def _load_parameters(schema, categories, default_categories, outputs) -> list[Parameter]:
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
        # enabled = None,
    )

    p.value = info.get("default")
    return p


def _get_type(info: dict) -> str:
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
        integer="GPLong"
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
