from parameters import load_omniscape_parameters, load_omniscape_schema
from runner import run_omniscape
from Run_Tool import Run_Tool


class Run_Omniscape(Run_Tool):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        super().__init__(label="Run Omniscape", description="", runner=run_omniscape)

        self.schema = load_omniscape_schema()
        self.initial_params = load_omniscape_parameters(self.schema)