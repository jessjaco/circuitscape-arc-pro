# circuitscape-arc-pro
Circuitscape Python Script Tool for Arcgis Pro

## Installation and Usage

To install, follow instructions in [src/INSTALL.md](src/INSTALL.md).

## Versions

The versions of Circuitscape, Omniscape, and Julia used in this tool are defined in [Project.toml](src/Project.toml) 
and the [packaging workflow](.github\workflows\zip_release.yaml); these will be periodically updated.

Since Arc Pro typically updates automatically, it is difficult to test across different versions. This tool was created
using Arc Pro 3.x series (last tested version: 3.2.1).

## Program Design

To ease usage and maintain compatibility, Julia itself is distributed in the zip package. It is the latest
version tested with the versions of Circuitscape and Omniscape included with [Project.toml](src/Project.toml).

All parameters are loaded as defined in the documentation and/or source code for Circuitscape and Omniscape.
Specifically, I defined a [json schema](https://json-schema.org) for each which are mantained in [a separate
repo](https://github.com/jessjaco/circuitscape-schema) and loaded as a submodule here. 

## Bugs and Caveats

The limitations of Arc Pro Python script tools as well as Python <-> Julia interprocess communications necessitate
certain limitations. Among these

1. There is no way to cancel running jobs.
Using the 'cancel' option in a running tool is typically ineffective (Arc Pro only cancels a python script between
lines). To cancel a running process, you will need to exit Arc Pro completely.
1. Errors do not always show as failed runs in Arc Pro. To be sure, click "View Details".
1. Omniscape progress does not update (see https://github.com/Circuitscape/Omniscape.jl/issues/148).
1. The tool does not respect any environment settings in Arc Pro.