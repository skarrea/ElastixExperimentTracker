# Elastix Python API
This is a collection python tools made to work with and test out different elastix registration schemes for medical images. 

The code uses the elastix binaries, but is built around using a mixture of the elastix recipe .txt files and config files from python to perform the registrations. 

The code requires that elastix is added to path. In other words you should be able to run ```elastix``` from terminal. Some functionality also relies on ITKSnap being added to path. 

## Setup
Run `pip install -r requirements.txt` to isntall the required packages. To download test data run `python generateTestData.py`. This will download a sample CT and T1 weighted MRI image of the brain and create some binary masks based on simple intensity thresholding.

### Docker
An alternative way to setupt is to use a docker image. A [dockerfile](docker/Dockerfile) is provided in the [docker folder](docker/). For a description of how to setup and use docker see the [docker readme](/docker/README.md).

## Usage
The code relies on three files to define a registration experiment: 
 1. A config file to determine which files are used as input for the registration
 2. A registration scheme `.yaml` file that spesifies which elastix parameter files to use .
 3. *elastix* parameter files (`.txt` files).


## My first registration experiment
**NB: file paths are windows paths. For linux paths change `\` for `/`*
We will use the downloaded example data for our first registration experiment. First we need to specify a `config` file. We will use `config\translationAffine.yaml` as a base. We need to overwrite some of the defaults in `config.py`. Once we have set up eveything correctly our config file `config\testTranslationAffine.yaml` should look something like this: 

```yaml
REGISTRATION:
  SCHEME: "TranslationAffine"
  MOVING_IMAGE_NAME: 'CT.mha'
  FIXED_IMAGE_NAME: 'T1.mha'
  MOVING_MASK_NAME: 'CT_mask.nii.gz'
  FIXED_MASK_NAME: 'T1_mask.nii.gz'
  MASK_DIR: 'inputImages'
```

From the config file we see that the scheme `registrationSchemes/TranslationAffine/` is used. The experiment is run by calling `python run_elastix.py configs\testTranslationAffine.yaml`.

## My second registration experiment
We will now modify the registration parameters of our first registration experiment. We will first call `python create_new_scheme.py -c configs\testTranslationAffine.yaml -n testTranslationAffineModified`. This will create a new config file `configs\testTranslationAffineModified.yaml` pointing to a new corresponding registration scheme `registrationSchemes\testTranslationAffineModified`. The config, scheme and parameter files are otherwise the same.

Let's make some changes to the registraiton experiment. Let's not use the masks and let's change the output format of the final registration step to `.nii.gz` to save some space when writing the registration output. The first change is performed in chaging `configs\testTranslationAffineModified.yaml` to

```yaml
REGISTRATION:
  FIXED_IMAGE_NAME: T1.mha
  MOVING_IMAGE_NAME: CT.mha
  SCHEME: testTranslationAffineModified
  USE_FIXED_MASK: False
```

Then we change the parameter `(ResultImageFormat "nii")` in `registrationSchemes\testTranslationAffineModified\affine.txt` to `(ResultImageFormat "nii.gz")`.

We then run the experiment by calling `python run_elastix.py configs\testTranslationAffineModified.yaml`. The registration output will be written to a subdirectory in the chosed output directory named according to the registration scheme.