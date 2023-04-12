# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

import platform
import subprocess
import sys


def install_dependencies(python_path, system):

    dependencies = "kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/"

    print("Installing dependencies...")

    # Install module dependencies with pip
    subprocess.call(python_path + " -m pip install " + dependencies,
                    shell=True)


if __name__ == '__main__':
    python_exe = sys.executable  # location of python executable, avoids dependency on PATH

    try:  # check if pip is installed
        subprocess.check_call(python_exe + " -m pip --version", shell=True)

    except subprocess.CalledProcessError:  # info about pip and exit script
        print()
        print(
            "Pip is the recommended tool for installing Python packages, and usually comes bundled with python."
        )
        print("Without pip, dependencies are much harder to install...")
        print("Please install pip before trying to use this script again.")
        print(
            "Take a look at the installation guide if needed: https://pip.pypa.io/en/stable/installation/"
        )
        print()
        input("Press any key to exit")
        sys.exit()

    # check if running on windows
    current_system = platform.system().lower()

    if "windows" in current_system:  # windows
        install_dependencies(python_exe, "windows")

    else:
        # when running on linux or other OS that is not windows
        print("This script is meant to be run on Windows.")

    print()
    input("Press any key to exit")
