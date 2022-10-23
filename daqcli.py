#!/usr/bin/env python
# Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
import argparse
import subprocess
from modules.formatmodule import bcolors, bsymbols, prints, labels
#from modules.database import ini_database


def handle_args():
    parser = argparse.ArgumentParser(
        description='Run foss.py help for more information. Run foss.py deps to install dependencies.')
    parser.add_argument('argument', type=str)
    args = parser.parse_args()
    return args


def switch(args):
    match args.argument:
        case "deps" | "dependencies" | "update":
            print(f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}{labels.prog_name}: Starting dependency check tool...{bcolors.ENDC}")
            subprocess.call("python ./modules/updater.py", shell=True)
            return
        case "data" | "d" | "collect" | "run":
            print(f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}{labels.prog_name}: Starting data collection tool...{bcolors.ENDC}")
            subprocess.call("python ./driver.py", shell=True)
            return
        case "clean" | "cleanup" | "remove":
            print(f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}{labels.prog_name}: Clean output directory...{bcolors.ENDC}")
            subprocess.call("python ./modules/cleanup.py", shell=True)
            return
        case "wisdom" | "zen":
            print(f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.OKBLUE}{bcolors.BOLD}{labels.prog_name}: Providing you with design ethic...{bcolors.ENDC}")
            subprocess.call("python ./modules/design-wisdom.py", shell=True)
            return
        case _:
            # launch help
            print(f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.FAIL}{bcolors.BOLD}{labels.prog_name}: Unknown argument...{bcolors.ENDC}")
            print(
                f"{bcolors.OKBLUE}{bsymbols.info} {bcolors.OKGREEN}{labels.prog_name}: Available commands:{bcolors.ENDC}")
            print(f"    deps{bcolors.ENDC}")
            print(f"    data{bcolors.ENDC}")
            print(f"    clean{bcolors.ENDC}")
            print(f"    sim{bcolors.ENDC}")
            print(f"    wisdom{bcolors.ENDC}")
            return


def main():
    p = prints()
    # ini_database()
    args = handle_args()
    p.title()
    switch(args)


if __name__ == '__main__':
    main()
else:
    print("The cli should be executed directly.")
