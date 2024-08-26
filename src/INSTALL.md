# Circuitscape Toolbox for Arc Pro

## Installation

To use this extension, unzip the release folder and save the contents in a stable location. Start ArcGIS Pro.
Then, either select "Toolbox" then "Add Toolbox" on the "Insert" panel:
![One way to add the toolbox](https://raw.githubusercontent.com/jessjaco/circuitscape-arc-pro/main/docs/img/add_option_one.png)
...or to the "Catalog" pane, right click on "Toolboxes", and select "Add Toolbox":
![Another way to add it](https://raw.githubusercontent.com/jessjaco/circuitscape-arc-pro/main/docs/img/add_option_two.png)

Navigate to the location where you unzipped the file and select "Circuitscape.pyt".

## Usage

The toolbox shadows the full functionality of Circuitscape and Omniscape in Julia.
Simply parameterize and hit run. To monitor while running , select "View Details" at the bottom
of the Arc Pro Toolbox window.

![User interface](https://raw.githubusercontent.com/jessjaco/circuitscape-arc-pro/main/docs/img/side_by_side.png)

Please note the first model run will take longer than usual, as the tool is
downloading, installing and testing Circuitscape and Omniscape.

For a full description of the parameters and their usage, please refer to the documentation for [Circuitscape](https://docs.circuitscape.org/Circuitscape.jl/latest/) and [Omniscape](https://docs.circuitscape.org/Omniscape.jl/stable/).

## Circuitscape tips
Specifying the output file is a bit tricky. If it's not clear by the help bubble,
you need to specify a new file with an ".out" extension. If using the file browser, navigate
to the folder you wish the place the output, and type a name ending in .out (e.g. "model.out")
and the bottom, then hit OK.

## Omniscape tips
The output location for Omniscape (the "Project Name" dialog) is a folder. Otherwise it is best 
to define it similarly to the Circuitscape instructions above. That is, navigate to a location
and type the name of the (new) folder at the bottom. If you use an existing folder, an
exclamation point will appear in the tool window, but it will still run.

The JULIA_NUM_THREADS environment variable, which defines the number of parallel threads to use
is represented by the "Number of Threads" parameter under "Calculation Options". The usage of this parameter supercedes any environment settings. Just noting
as this (along with making sure "Parallelize" is checked) can speed up calculations immensely.
(See Omniscape documentation for more info).


## Known Issues

- Sometimes when you add the toolbox in Arc Pro, it doesn't appear. For now the best
solution is to exit Arc Pro and try again.

- Using the "cancel" option in a running tool can be 
  ineffective (Arc Pro only cancels a python script between lines). To cancel a running process, 
  you will need to exit Arc Pro completely (or kill it in task manager).
- Errors do not always show as failed runs in Arc Pro. To be sure, click "View Details".
- The tool does not respect any environment settings in Arc Pro.