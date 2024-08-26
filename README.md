# Circuitscape Python Script Tool for ArcGIS Pro

## Overview

The goal of this project is to create a Python Script Tool for ArcGIS Pro which
provides an interface for running the current versions of
[Circuitscape](https://github.com/Circuitscape/Circuitscape.jl) and
[Omniscape](https://github.com/Circuitscape/Omniscape.jl).

Here is a picture of the tool in action:
![Picture of interfaces](https://raw.githubusercontent.com/jessjaco/circuitscape-arc-pro/main/docs/img/omniscape_running.png)

## Installation and Usage

The latest version of the tool can be downloaded at https://github.com/jessjaco/circuitscape-arc-pro/releases/latest. To install, follow instructions in [src/INSTALL.md](src/INSTALL.md).

## Versions

The versions of Circuitscape, Omniscape, and Julia used in this tool are defined in [Project.toml](src/Project.toml)
and the [packaging workflow](.github/workflows/zip_release.yaml); these will be periodically updated.

Since Arc Pro typically updates automatically, it is difficult to test across different versions. This tool was created
using Arc Pro 3.x series (last tested version: 3.2.1).

To ease usage and maintain compatibility, Julia itself is distributed in the zip package. It is the latest
version (currently 1.10.0) tested with the versions of Circuitscape and Omniscape included with
[Project.toml](src/Project.toml).

## Program Design

All parameters within the tool are loaded as defined in the documentation and/or source code for Circuitscape and Omniscape.
Specifically, I defined a [json schema](https://json-schema.org) for each which are mantained in [a separate
repo](https://github.com/jessjaco/circuitscape-schema) and loaded as a submodule here.

Circuitscape and Omniscape are installed in a siloed environment on first usage
and run via python using `subprocess.Popen`.

## Bugs and Caveats

The limitations of Arc Pro Python script tools as well as Python <-> Julia interprocess communications necessitate
certain limitations. See [src/INSTALL.md](src/INSTALL.md) for more information.

Please report other issues at
https://github.com/jessjaco/circuitscape-arc-pro/issues.

## Acknowledgements

This tool was authored by Jesse Anderson as guided by Kimberly Hall with The Nature Conservancy. It was inspired by the original ArcGIS Circuitscape tool authored by Brad McRae and Jim Platt. Funding for this project was provided by The Wilburforce Foundation. Circuitscape.jl was authored by Brad McRae, Viral Shah, Tanmay Mohapatra, and Ranjan Anantharaman. Omniscape.jl was authored by Vincent Landau.