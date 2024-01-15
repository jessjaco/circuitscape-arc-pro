from parameters import load_omniscape_parameters, load_omniscape_schema
from runner import run_omniscape
from Run_Tool import Run_Tool


class Run_Omniscape(Run_Tool):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        label = "Run Omniscape"
        description = "Run the Omniscape tool"
        super().__init__(
            label=label,
            description=description,
            runner=run_omniscape,
            commandArgParameterNames=["threads"],
        )

        self.schema = load_omniscape_schema()
        self.initial_params = load_omniscape_parameters(self.schema)
