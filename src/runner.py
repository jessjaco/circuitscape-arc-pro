"""This contains the code to actually run CS or OS. Except for the `messages`
parameter, these are independent of ESRI. Theoretically if you created
some sort of messages object which had `addMessage` and `addErrorMessage`
accessors, you could use this by itself. Another approach would be to allow
messages to be None, and test for that before writing. Another option would be
wrap messages in some sort of logger class and treat it like a standard logger.
"""
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, CREATE_NO_WINDOW


def run_circuitscape(config_file: Path, command_args: dict, messages) -> None:
    working_dir = Path(__file__).resolve().parent
    config_file_fixed = str(config_file).replace("\\", "/")
    command = f'"using Pkg; Pkg.activate(realpath(\\"{working_dir}\\")); Pkg.instantiate(); using Circuitscape; compute(realpath(\\"{config_file_fixed}\\"))"'
    return run_julia_command(command, command_args, messages)


def run_omniscape(config_file: Path, command_args: dict, messages) -> None:
    working_dir = Path(__file__).resolve().parent
    config_file_fixed = str(config_file).replace("\\", "/")
    command = f'"using Pkg; Pkg.activate(realpath(\\"{working_dir}\\")); Pkg.instantiate(); using Omniscape; run_omniscape(realpath(\\"{config_file_fixed}\\"))"'

    return run_julia_command(command, command_args, messages)


def run_julia_command(command: str, command_args: dict, messages) -> None:
    working_dir = Path(__file__).resolve().parent

    # The path to the julia exe itself. This needs to be changed when the
    # workflow is changed
    julia_command = "julia-1.10.0/bin/julia.exe"

    for k, v in command_args.items():
        # Only supports full kw args
        julia_command += f" --{k} {v}"
    julia_exe = working_dir / julia_command
    full_command = f"{julia_exe} -e {command}"
    messages.addMessage(full_command)

    # this pattern is necessary (bufsize, but also the context) as it's the
    # only way I could find to get OS progress messages to propagate to the
    # Arc window.
    with Popen(
        full_command,
        stdout=PIPE,
        stderr=STDOUT,
        creationflags=CREATE_NO_WINDOW,
        bufsize=1,
        encoding="utf-8",
    ) as proc:
        for line in proc.stdout:
            if "ERROR" in line:
                messages.addErrorMessage(line)
            else:
                messages.addMessage(line)
