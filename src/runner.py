from pathlib import Path
from subprocess import Popen, PIPE, STDOUT


def run_circuitscape(config_file: Path, messages) -> None:
    working_dir = Path(__file__).resolve().parent
    wrking_dir = str(working_dir).replace("\\", "/")
    cfg_file = str(config_file).replace("\\", "/")
    julia_exe = working_dir / "julia-1.9.2/bin/julia.exe"
    julia_script = f'"using Pkg; Pkg.activate(\\"{wrking_dir}\\"); Pkg.instantiate(); using Circuitscape; compute(\\"{cfg_file}\\")"'
    full_command = f"{julia_exe} -e {julia_script}"
    messages.addMessage(full_command)
    proc = Popen(full_command, stdout=PIPE, stderr=STDOUT)
    stdout_iterator = iter(proc.stdout.readline, b"")
    for line in stdout_iterator:
        messages.addMessage(line.rstrip())
