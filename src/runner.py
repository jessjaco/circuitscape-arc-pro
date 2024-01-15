from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from typing import Callable


def run_ascape(
    get_script: Callable, config_file: Path, command_args: dict, messages
) -> None:
    working_dir = Path(__file__).resolve().parent
    wrking_dir = str(working_dir).replace("\\", "/")
    cfg_file = str(config_file).replace("\\", "/")
    julia_command = "julia-1.9.2/bin/julia.exe"
    for k, v in command_args.items():
        # Only supports full kw args
        julia_command += f" --{k} {v}"
    julia_exe = working_dir / julia_command

    julia_script = get_script(wrking_dir, cfg_file)
    full_command = f"{julia_exe} -e {julia_script}"
    messages.addMessage(full_command)
    proc = Popen(full_command, stdout=PIPE, stderr=PIPE)
    stdout_iterator = iter(proc.stderr.readline, b"")
    for line in stdout_iterator:
        if b"ERROR" in line:
            messages.addErrorMessage(line.rstrip())
        else:
            messages.addMessage(line.rstrip())


def run_omniscape(config_file: Path, messages, command_args) -> None:
    julia_script = (
        lambda working_dir, config_file: f'"using Pkg; Pkg.activate(\\"{working_dir}\\"); Pkg.instantiate(); using Omniscape; run_omniscape(\\"{config_file}\\")"'
    )
    return run_ascape(julia_script, config_file, command_args, messages)


def run_circuitscape(config_file: Path, messages, command_args) -> None:
    julia_script = (
        lambda working_dir, config_file: f'"using Pkg; Pkg.activate(\\"{working_dir}\\"); Pkg.instantiate(); using Circuitscape; compute(\\"{config_file}\\")"'
    )
    return run_ascape(julia_script, config_file, command_args, messages)
