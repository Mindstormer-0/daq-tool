# -*- coding: utf-8 -*-
# Written by Caleb C. in 2022 for Carthage Space Sciences | WSGC | NASA
# This script will get the dependencies for fossS/MPG related Python projects and self update from the repo.
import sys
import os
import subprocess
from formatmodule import bcolors, bsymbols, prints, labels

fmt = prints()
deps_file = "config/deps.toml"
modules_base = []
modules_dependencies = []
modules_alt_name = {}
project_url = ""
fail = False


def basic():
    global modules_base, fmt
    fmt.color_print(f"{labels.prog_name}: Checking dependencies...")
    for module in modules_base:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__(module_alt)
            else:
                __import__(module)
        except ImportError:
            fmt.color_print(f"{labels.prog_name}: {module} not found...")
            fmt.color_print(f"{labels.prog_name}: Installing {module}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL)
            except subprocess.SubprocessError:
                fmt.color_print(
                    f"{labels.prog_name}: Could not acquire module named {module}.", "red")


def check_pip():
    global fmt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)
    except subprocess.SubprocessError:
        fmt.color_print(f"{labels.prog_name}: Could not update pip...", "red")
        fmt.color_print(
            f"{labels.prog_name}: Is Python 3.10 on your machine?", "red")


def deps_loader():
    global fmt, project_url, modules_base, modules_dependencies, modules_alt_name, deps_file
    abs_path = os.path.abspath(deps_file)
    import toml
    data = toml.load(abs_path)
    for key in data:
        if key == "project_url":
            project_url = data[key]
        elif key == "modules_base":
            modules_base = data[key]
        elif key == "modules_dependencies":
            modules_dependencies = data[key]
        elif key == "modules_alt_name":
            modules_alt_name = data[key]


def check_toml():
    global fmt
    try:
        __import__('toml')
        deps_loader()
    except ImportError:
        fmt.color_print(f"{labels.prog_name}: TOML parser not found...")
        fmt.color_print(f"{labels.prog_name}: Installing 'toml'...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "toml"], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            fmt.color_print(
                f"{labels.prog_name}: Could not get toml parser...", "red")


def self_update():
    global fmt
    try:
        import git
        fmt.spin_print(f"{labels.prog_name}: Checking for updates...")
        g = git.cmd.Git(project_url)
        msg = g.pull()
        tag = subprocess.check_output(
            ["git", "describe", "--always"]).strip().decode()
        fmt.spin_print(f"git: Latest commit to this branch was {tag}")
        fmt.spin_print(f"{msg}")
    except (git.exc.GitCommandError, subprocess.SubprocessError):
        fmt.spinner.text_color = 'red'
        fmt.spinner.fail(f"{labels.prog_name}: Could not update from git.")


def advanced():
    global modules_dependencies, fmt
    for module in modules_dependencies:
        try:
            if modules_alt_name.get(module) is not None:
                module_alt = modules_alt_name.get(module)
                __import__(module_alt)
            else:
                __import__(module)
        except ImportError:
            fmt.spinner.text_color = 'grey'
            fmt.spinner.fail(f"{labels.prog_name}: {module} not found...")
            fmt.spinner.start()
            fmt.spin_print(f"{labels.prog_name}: Installing {module}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL)
            except subprocess.SubprocessError:
                fmt.spinner.text_color = 'red'
                fmt.spinner.fail(
                    f"{labels.prog_name}: Could not acquire module named {module}.")


def test(mode):
    global modules_dependencies, modules_base, modules_alt_name, fmt, fail
    if mode == 'basic':
        fmt.color_print(f"{labels.prog_name}: Verifying...")
        for module in modules_base:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__(module)
            except ImportError:
                fail = True
                fmt.color_print(
                    f"{labels.prog_name}: {module} was not imported. Try manually installing it.", "red")
    elif mode == 'advanced':
        fmt.spin_print(f"{labels.prog_name}: Verifying...")
        for module in modules_dependencies:
            if modules_alt_name.get(module) is not None:
                module = modules_alt_name.get(module)
            try:
                __import__(module)
            except ImportError:
                fail = True
                fmt.spinner.text_color = 'red'
                fmt.spinner.fail(
                    f"{labels.prog_name}: {module} was not imported. Try manually installing it.")
    check_fail()


def check_fail():
    global fail, fmt
    if fail is not True and fmt.spinner is not None:
        fmt.spinner.text_color = 'green'
        fmt.spinner.succeed(
            f" {labels.prog_name}: Dependencies present & checked.")
        fmt.spinner.info(f"{labels.prog_name}: Done.")
    elif fail is True:
        if fmt.spinner is not None:
            fmt.spinner.text_color = 'red'
            fmt.spinner.fail(f" {labels.prog_name}: Some tests failed!")
        else:
            print(
                f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} {labels.prog_name}: Some tests failed!{bcolors.ENDC}")


def main():
    try:
        check_pip()
        check_toml()
        basic()
        test('basic')
        global fmt
        fmt.init_spinner()
        self_update()
        advanced()
        test('advanced')
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    sys.exit(0)


# Run the main function if this module is called directly.
if __name__ == '__main__':
    main()
