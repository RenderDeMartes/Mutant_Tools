from __future__ import absolute_import
import sys
import os
from maya import cmds
mutant_path = os.path.join(cmds.internalVar(usd=True))
mutant_path = mutant_path.replace('2019', '2022')
if mutant_path not in sys.path:
    sys.path.append(mutant_path)
    
import Mutant_Tools
