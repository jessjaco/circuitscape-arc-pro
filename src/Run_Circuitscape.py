from parameters import load_circuitscape_parameters, load_circuitscape_schema
from runner import run_circuitscape
from Run_Tool import Run_Tool


class Run_Circuitscape(Run_Tool):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        label = "Run Circuitscape"
        description = ""
        runner = run_circuitscape
        super().__init__(label, description, runner)

        self.schema = load_circuitscape_schema()
        self.initial_params = load_circuitscape_parameters(self.schema)