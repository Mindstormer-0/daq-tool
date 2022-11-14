import sys
import os
import subprocess
from formatmodule import bcolors, bsymbols, prints, labels

fmt = prints()
deps_file = "config/deps.toml"
modules_base = []
modules_dependencies = []
fail = False


def autoremove_check():
    global fmt
    try:
        fmt.color_print(
            f"{labels.prog_name}: Leveraging pip3-autoremove...")
        __import__('pip3-autoremove')
    except ImportError:
        fmt.color_print(f"{labels.prog_name}: Installing 'pip3-autoremove'...")
        try:
            subprocess.run(['python', '-m', 'pip', 'install',
                           'pip3-autoremove'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            fmt.color_print(
                f"{labels.prog_name}: Could not get pip3-autoremove...", "red")


def deps_loader():
    global fmt, modules_base, modules_dependencies, deps_file
    abs_path = os.path.abspath(deps_file)
    import toml
    data = toml.load(abs_path)
    for key in data:
        if key == "modules_base":
            modules_base = data[key]
        elif key == "modules_dependencies":
            modules_dependencies = data[key]


def deps_remover():
    global fmt, modules_dependencies, fail
    fmt.color_print(f"{labels.prog_name}: Removing dependencies...")
    for module in modules_dependencies:
        try:
            fmt.color_print(
                f"{labels.prog_name}: Removing {module}...")
            subprocess.run(['pip3-autoremove', module, '-y'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            fmt.color_print(
                f"{labels.prog_name}: Could not remove module {module}.", "red")
            fail = True
    try:
        fmt.color_print(
            f"{labels.prog_name}: Removing GitPython...")
        subprocess.run(['pip3-autoremove', 'GitPython', '-y'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.SubprocessError:
        fmt.color_print(
            f"{labels.prog_name}: Could not remove module 'GitPython'.", "red")
        fail = True
    try:
        fmt.color_print(
            f"{labels.prog_name}: Removing halo...")
        subprocess.run(['pip3-autoremove', 'halo', '-y'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.SubprocessError:
        fmt.color_print(
            f"{labels.prog_name}: Could not remove module 'halo'.", "red")
        fail = True
    try:
        fmt.color_print(
            f"{labels.prog_name}: Removing autoremove...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", 'pip3-autoremove', "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.SubprocessError:
        fmt.color_print(
            f"{labels.prog_name}: Could not remove pip3-autoremove", "red")
        fail = True


def check_fail():
    global fail, fmt
    if fail is not True and fmt.spinner is not None:
        fmt.spinner.text_color = 'green'
        fmt.spinner.succeed(
            f" {labels.prog_name}: Dependencies removed.")
        fmt.spinner.info(f"{labels.prog_name}: Done.")
    elif fail is True:
        if fmt.spinner is not None:
            fmt.spinner.text_color = 'red'
            fmt.spinner.fail(
                f" {labels.prog_name}: Verify dependencies were removed!")
        else:
            print(
                f"{bcolors.OKBLUE}{bsymbols.info}{bcolors.FAIL} {labels.prog_name}: Verify dependencies were removed!{bcolors.ENDC}")
    else:
        fmt.color_print(
            f"{labels.prog_name}: Dependencies removed.", "green")
        fmt.color_print(
            f"{labels.prog_name}: Done.", "green")


def main():
    try:
        fmt.init_spinner()
        autoremove_check()
        deps_loader()
        deps_remover()
        check_fail()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    sys.exit(0)


# Run the main function if this module is called directly.
if __name__ == '__main__':
    main()
