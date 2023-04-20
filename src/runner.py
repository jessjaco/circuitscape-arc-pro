from pathlib import Path
import subprocess

def run_circuitscape(config_file: Path, messages = None) -> None:
    working_dir = Path(__file__).resolve().parent
    julia_exe = working_dir / "julia-1.8.5-win64/julia-1.8.5/bin/julia.exe"
    julia_script = f"\"using Pkg; Pkg.activate(\\\".\\\"); Pkg.instantiate(); using Circuitscape; compute(\\\"{config_file}\\\")\""
    full_command = f"{julia_exe} -e {julia_script}"
    print(full_command)
    subprocess.run(full_command)