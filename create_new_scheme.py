import argparse
import os
import glob
import yaml
from config import get_cfg_defaults
from pathlib import Path
from shutil import copy
from datetime import datetime
from textwrap import dedent, wrap
from argparse import RawTextHelpFormatter

def get_parser():
    parser = argparse.ArgumentParser(
        description="\n".join(wrap(dedent("""\
        Makes a new registration scheme based on a previously created scheme.
        If no name is specified the name of the new scheme will be the same as the template scheme,
        but with an appended datetime suffix. This will copy both the config file and the scheme folder.
        Default storage locations will be used."""), 80, expand_tabs=False)),
        epilog=dedent('''\
        Example usage: 
        To create a copy of the translation scheme named translationCopy we can call
        python create_new_scheme.py --config ./configs/translation.yaml -n translationCopy
        
        '''),
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "-c",
        "--config",
        default="./configs/translationDeform.yaml",
        metavar="FILE",
        help="path to config file",
        type=str,
    )

    parser.add_argument(
        "-n", "--name", help="Name of new scheme.", default=None, type=str
    )

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    cfg = get_cfg_defaults()
    cfg.merge_from_file(args.config)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    reg_folder = (
        Path(cfg.BASE_DIR)
        / Path(cfg.REGISTRATION.BASE_DIR)
        / Path(cfg.REGISTRATION.SCHEME)
    )

    with open(os.path.join(reg_folder, "scheme.yaml"), "r") as f:
        scheme = yaml.load(f, Loader=yaml.FullLoader)

    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # created_schemes = [scheme_name.lower().replace('.yaml', '') for scheme_name in
    #  os.listdir(cfg.REGISTRATION.BASE_DIR) + os.listdir('./configs')]

    prev_scheme = scheme["Name"]
    time = datetime.now().strftime("%y%m%d-%H%M")

    scheme["Last updated"] = time

    if not (args.name):
        try:
            valid_check = datetime.strptime(
                config["REGISTRATION"]["SCHEME"][-11:], "%y%m%d-%H%M"
            )
            config["REGISTRATION"]["SCHEME"] = (
                config["REGISTRATION"]["SCHEME"][:-11] + time
            )
        except:
            config["REGISTRATION"]["SCHEME"] += time
    else:
        config["REGISTRATION"]["SCHEME"] = args.name

    # Write config
    with open(
        Path(cfg.BASE_DIR)
        / Path("configs")
        / Path(config["REGISTRATION"]["SCHEME"] + ".yaml"),
        "w",
    ) as f:
        yaml.dump(config, f)

    new_reg_folder = (
        Path(cfg.BASE_DIR)
        / Path(cfg.REGISTRATION.BASE_DIR)
        / Path(config["REGISTRATION"]["SCHEME"])
    )
    os.makedirs(new_reg_folder)

    with open(new_reg_folder / Path("scheme.yaml"), "w") as f:
        yaml.dump(scheme, f)

    for file in scheme["Scheme"]:
        copy(reg_folder / Path(file), new_reg_folder / Path(file))

    print(f'New scheme written to {config["REGISTRATION"]["SCHEME"] + ".yaml"}')
