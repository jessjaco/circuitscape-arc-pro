# Circuitscape Toolbox for Arc Pro

## Installation

To use this extension, unzip the release folder somewhere. Then fire up Arc Pro.
Go to the 'Catalog' pane, right click on 'Toolboxes', and select 'Add Toolbox'.
Navigate to the unzipped location and select "Circuitscape.pyt".

## Usage

The toolbox shadows the full functionality of Circuitscape and Omniscape in Julia.
Simply parameterize and hit run. To monitor while running , select "View Details" at the bottom
of the Arc Pro Toolbox window.

Please note the first model run will take longer than usual, as the tool is
downloading, installing and testing Circuitscape and Omniscape.

## Circuitscape tips
The parameterization of the output file is a bit clunky. If it's not clear by the help bubble,
you need to specify a new file with an ".out" extension. If using the file browser, navigate
to the folder you wish the place the output, and type a name ending in .out (e.g. "model.out")
and the bottom, then hit OK.

## Omniscape tips
The output location for Omniscape (the "Project Name" dialog) is a folder. Otherwise it is best 
to define it similarly to the Circuitscape instructions above. That is, navigate to a location
and type the name of the (new) folder at the bottom. If you use an existing folder, an
exclamation point will appear in the tool window, but it will still run.

The JULIA_NUM_THREADS environment variable, which defines the number of parallel threads to use
is represented by the "Number of Threads" parameter under "Calculation Options". Just noting
as this (along with making sure "Parallelize" is checked) can speed up calculations immensely.
(See Omniscape documentation for more info).


## Known Issues

- Sometimes when you add the toolbox in Arc Pro, it doesn't appear. For now the best
solution is to exit Arc Pro and try again.

- There is no way to cancel running jobs.  Using the 'cancel' option in a running tool is typically 
  ineffective (Arc Pro only cancels a python script between lines). To cancel a running process, 
  you will need to exit Arc Pro completely (or kill it in task manager).
- Errors do not always show as failed runs in Arc Pro. To be sure, click "View Details".
- The tool does not respect any environment settings in Arc Pro.