# Elastix Python API
This is a collection python tools made to work with and test out different elastix registration schemes for medical images. 

The code uses the elastix binaries, but is built around using a mixture of the elastix recipe .txt files and config files from python to perform the registrations. 

The code requires that elastix is added to path. In other words you should be able to open ```elastix```. Some functionality also relies on ITKSnap being added to path. 

## Usage
The code relies on two files to define a registration experiment: 
 1. A config file to determine which files are used as input for the registration
 2. A registration scheme defined as *elastix* `.txt` files. 

### To do
 - [ ] Update check_registration to rely on the config aswell.
 - [x] Move the ipython notebook from regout to this folder.
 - [ ] Create dummy folders in the repository for input and output and use them as a standard in the github repo and in the default configuration.
 - [ ] Add more documentation about the intended usage of the python files and some examples.
 - [ ] Add checks for file existance in [check_registration.py](check_registration.py)
 - [ ] make [convertToMhd.py](convertToMhd.py) a and importable function.