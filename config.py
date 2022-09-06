from yacs.config import CfgNode as CN
import os

_C = CN()

_C.INPUT = CN()
_C.INPUT.DIRECTORY = './inputImages'

# patients that we want to exclude from our analysis
_C.INPUT.EXCLUDE = []

_C.OUTPUT = CN()
_C.OUTPUT.DIRECTORY = './outputRegistrations'

_C.TEST = CN()
_C.TEST.TEST = False
# All settings below are ignored if False
# NUMPATS is ignored if a list of specific patients is specified.
_C.TEST.NUMPATS = 1
# If no specific patients are specified NUMPATS random patient will be selected. 
_C.TEST.SPECIFIC_PATIENTS =  False # List of patient numbers.
_C.TEST.SPECIFIC_LIST =  [] # List of patient names.

_C.REGISTRATION = CN()
_C.REGISTRATION.BASE_DIR = 'registrationSchemes' 
_C.REGISTRATION.SCHEME = 'Default'

# Masks 
_C.REGISTRATION.USE_FIXED_MASK = True
_C.REGISTRATION.USE_MOVING_MASK = False

_C.REGISTRATION.MASK_DIR = './segmentations' 

_C.REGISTRATION.MOVING_MASK_NAME = 'moving_mask.nii.gz'
_C.REGISTRATION.FIXED_MASK_NAME = 'fixed_mask.nii.gz'

# Images to register
_C.REGISTRATION.MOVING_IMAGE_NAME = 'Image1.mha'
_C.REGISTRATION.FIXED_IMAGE_NAME = 'Image2.mha'

_C.SYSTEM = CN()
_C.NUM_THREADS = 14
_C.BASE_DIR = os.path.dirname(os.path.relpath(__file__))

def get_cfg_defaults():
    return _C.clone()
    