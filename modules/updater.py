# -*- coding: utf-8 -*-
#Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
#This script will get the dependencies for fossS/MPG related Python projects and self update from the repo.
import sys, subprocess
from formatmodule import bcolors, bsymbols, prints, labels

modules_base = ['wheel', 'halo', 'GitPython']
modules_dependencies = ['pyusb', 'pandas', 'bitarray', 'sqlite3', 'dash', 'dash-daq', 'dash-bootstrap-templates']
modules_alt_name = {'GitPython': 'git', 'pyusb': 'usb.core', 'dash-daq': 'dash_daq', 'dash-bootstrap-templates': 'dash_bootstrap_templates'}
project_url = "https://github.com/Mindstormer-0/daquery-tool.git"
fmt = prints()
fail = False

def basic():
    global modules_base, fmt
    fmt.color_print(f"{labels.prog_name}: Checking dependencies...")
    for module in modules_base:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__ (module_alt)
            else:
                __import__ (module)
        except ImportError:
            fmt.color_print(f"{labels.prog_name}: {module} not found...")
            fmt.color_print(f"{labels.prog_name}: Installing {module}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.SubprocessError:
                fmt.color_print(f"{labels.prog_name}: Could not acquire module named {module}.", "red")

def check_pip():
    global fmt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    except subprocess.SubprocessError:
        fmt.color_print(f"{labels.prog_name}: Could not update pip...", "red")

def self_update():
    global fmt
    try:
        import git
        fmt.spin_print(f"{labels.prog_name}: Checking for updates...")
        g = git.cmd.Git(project_url)
        msg = g.pull()
        tag = subprocess.check_output(["git", "describe", "--always"]).strip().decode()
        fmt.spin_print(f"git: Latest commit to this branch was {tag}")
        fmt.spin_print(f"{msg}")
    except (git.exc.GitCommandError, subprocess.SubprocessError):
        fmt.spinner.text_color ='red'
        fmt.spinner.fail(f"{labels.prog_name}: Could not update from git.")

def advanced():
    global modules_dependencies, fmt
    for module in modules_dependencies:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__ (module_alt)
            else:
                __import__ (module)
        except ImportError:
            fmt.spinner.text_color ='grey'
            fmt.spinner.fail(f"{labels.prog_name}: {module} not found...")
            fmt.spinner.start()
            fmt.spin_print(f"{labels.prog_name}: Installing {module}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.SubprocessError:
                fmt.spinner.text_color ='red'
                fmt.spinner.fail(f"{labels.prog_name}: Could not acquire module named {module}.")

def test(mode):
    global modules_dependencies, modules_base, modules_alt_name, fmt, fail
    if mode == 'basic':
        fmt.color_print(f"{labels.prog_name}: Verifying...")
        for module in modules_base:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__ (module)
            except ImportError:
                fail = True
                fmt.color_print(f"{labels.prog_name}: {module} was not imported. Try manually installing it.", "red")
    elif mode == 'advanced':
        fmt.spin_print(f"{labels.prog_name}: Verifying...")
        for module in modules_dependencies:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__ (module)
            except ImportError:
                fail = True
                fmt.spinner.text_color ='red'
                fmt.spinner.fail(f"{labels.prog_name}: {module} was not imported. Try manually installing it.")
    check_fail()

def check_fail():
    global fail, fmt
    if fail is not True and fmt.spinner is not None:
        fmt.spinner.text_color = 'green'
        fmt.spinner.succeed(f" {labels.prog_name}: Dependencies present & checked.")
        fmt.spinner.info(f"{labels.prog_name}: Done.")
    elif fail is True:
        if fmt.spinner is not None:
            fmt.spinner.text_color = 'red'
            fmt.spinner.fail(f" {labels.prog_name}: Some tests failed!")
        else:
            print(f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} {labels.prog_name}: Some tests failed!{bcolors.ENDC}")

def main():
    try:
        check_pip()
        basic()
        test('basic')
        global fmt;fmt.init_spinner()
        self_update()
        advanced()
        test('advanced')
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    sys.exit(0)

#Run the main function if this module is called directly.
if __name__ == '__main__':
    main()