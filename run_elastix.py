import os
import argparse
from config import get_cfg_defaults
import yaml
from pathlib import Path

def get_parser():
    parser = argparse.ArgumentParser(
        description='A python interface for Elastix')
    parser.add_argument(
        "config_file",
        default="",
        metavar="FILE",
        help="path to config file",
        type=str,
    )

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser

def extract_patients(cfg):
    '''Extracting the patients as specified in the 
    configuration file.
    '''

    input_dir = cfg.INPUT.DIRECTORY
    patients = os.listdir(input_dir)
    
    if cfg.TEST.TEST:
        if cfg.TEST.SPECIFIC_PATIENTS:
            patient_numbers = set([patient for patient in patients])
            if not(set(cfg.TEST.SPECIFIC_LIST).issubset(set(patients))):
                print('Patient(s)', list(set(cfg.TEST.SPECIFIC_LIST)-set(patients)),
                 'found in test list but not in input directory.') 
                return -1
            else:
                return cfg.TEST.SPECIFIC_LIST
        else:
            patients.shuffle()
            return patients[:cfg.TEST.NUMPATS]
    else:
        if set(cfg.INPUT.EXCLUDE).issubset(patients):
            return list(set(patients) - set(cfg.INPUT.EXCLUDE))
        else:
            print('Patients in exclusion list are not found in input directory.')
            return -1

def fix_spaces_in_paths(expression):
    # Takes the full elastix expression and fixes the issue of spaces in paths.
    # will assume anything containing :\ is a path and will wrap the path 
    # in quotation marks if it contains a space.
    
    expr_split = expression.split(' ')
    for i in range(len(expr_split)):
        if '\\:' in expr_split[i] and ' ' in expr_split[i]:
            expr_split[i] = "\"" + expr_split[i] + "\""
    return ' '.join(expr_split)

def register(cfg, patient):
    # Build the elastix expression for the terminal
    pat_im_dir = os.path.join(cfg.INPUT.DIRECTORY, patient)
    f_im = cfg.REGISTRATION.FIXED_IMAGE_NAME
    m_im = cfg.REGISTRATION.MOVING_IMAGE_NAME
    reg_out_dir = os.path.join(cfg.OUTPUT.DIRECTORY, cfg.REGISTRATION.SCHEME, patient)
    os.makedirs(reg_out_dir, exist_ok=True)



    expression = f'elastix -f "{os.path.join(pat_im_dir, f_im)}" -m "{os.path.join(pat_im_dir, m_im)}"' +\
        f' -out "{reg_out_dir}"'
    reg_folder = Path(cfg.REGISTRATION.BASE_DIR) / Path(cfg.REGISTRATION.SCHEME)
    with open(os.path.join(reg_folder, 'scheme.yaml'), 'r') as f:
        scheme = yaml.load(f, Loader=yaml.FullLoader)

    scheme['Scheme'] = ['"' + os.path.join(reg_folder, elem) + '"' for elem in scheme['Scheme']]

    parameter_maps = '-p ' + ' -p '.join(scheme['Scheme'])

    expression = ' '.join([expression, parameter_maps])

    if cfg.REGISTRATION.USE_FIXED_MASK:
        f_mask = ' '.join(['-fMask',
         '"' + os.path.join(cfg.REGISTRATION.MASK_DIR, patient, cfg.REGISTRATION.FIXED_MASK_NAME) + '"'])
        expression= ' '.join([expression, f_mask])

    if cfg.REGISTRATION.USE_MOVING_MASK:
        m_mask = ' '.join(['-mMask',
         '"' + os.path.join(cfg.REGISTRATION.MASK_DIR, patient,
          cfg.REGISTRATION.MOVING_MASK_NAME) + '"'])
        expression= ' '.join([expression, m_mask])
        
    print(expression)

    # subprocess.Popen(expression)
    os.system(expression)

if __name__ == '__main__':
    args = get_parser().parse_args()
    cfg = get_cfg_defaults()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    output_dir = cfg.OUTPUT.DIRECTORY
    os.makedirs(output_dir, exist_ok=True)
    
    patients = extract_patients(cfg)

    print(patients)

    for patient in patients:
        # try:
        register(cfg, patient)
        # except:
            # print(f'Error occurred for patient {patient}. Moving on to next patient.')
            
    