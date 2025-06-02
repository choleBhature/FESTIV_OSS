# %% FESTIV
# %
# % Flexible Energy Scheduling Tool for Integration of Variable generation
# % 
# % FESTIV is a steady-state power system operations tool that covers 
# % temporal horizons in the scheduling process starting from the day-ahead
# % unit commitment all the way through automatic generation control to
# % correct the actual area control error occuring every few seconds.
# %
# % The FESTIV GUI will open and ask for necessary input files and input
# % parameters. You can add FESTIV Model Rules using Matlab scripts and add
# % them to various points throughout FESTIV by selecting the scripts in the
# % GUI for appropriate spots (either scheduling processes or "Other Rules").
# % Or you can load a whole set of models that were previously saved to
# % represent a certain operational procedure in its entirety.
# % Formulations can be modified by adding new .txt files, making sure sets,
# % parameters, variables, and equations are declared and defined, and the
# % model definition is updated. Create the .txt files and then press 'Opt.
# % Model' on the GUI to make sure the FESTIV simulation uses them correctly
# % for the appropriate scheduling model.
# %
# % For more information, see <a href="matlab: 
# % web('http://www.nrel.gov/electricity/transmission/festiv.html')">the FESTIV homepage</a>.
# % or review the FESTIV user manual.
# %
# % To get started, just type python FESTIV.py in the terminal
# % To start from the middle of a previous execution that did not finish,
# % type python START_FESTIV_FROM_PREVIOUS_EXECUTION in the terminal

#figure out the start mid execution and start from previous situation

import warnings
import inspect
import math
import os
import sys
from settings import *
from reset_settings import *

warnings.filterwarnings('ignore')

stack = inspect.stack()
starting_execution_script = os.path.basename(stack[-1].filename)  # should be FESTIV.py if correct

if execution_from_previous==0 or starting_execution_script == "FESTIV.py":
    execution_from_previous = 0
    # print("executing the FESTIV script now!") (checked if FESTIV only executing)

if execution_from_previous:
    eps = sys.float_info.epsilon
    mod_val = (time * 60) % tRTC
    if abs(mod_val) < eps or abs(tRTC - mod_val) < eps:
        RTSCUC_binding_interval_index -= 1
else:
    pass

reset_settings_to_zero(use_float=True)
execution_from_previous=0;

