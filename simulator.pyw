# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

import sys
import os

# log errors
if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(
        "errorlog-" + os.path.splitext(os.path.basename(sys.argv[0]))[0] +
        ".txt", "w")

from bin.ui.ui import start

# run App
start()
