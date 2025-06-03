# % As part of FESTIV and its use on different machines including NREL's
# % super computer, hardware must be detected to ensure proper use throughout
# % model run.

# %The Following will set whether FESTIV uses GUI and for specific options
# %related to high performance computing and other options.
from GUI_HPC_OPTIONS import *
import settings
import platform 
import matplotlib

def detect_hardware_options():
    gui_hpc_options()
    print(settings.use_gui)
    if platform.system() in ['Linux']:
        print("detected Linux Machine")
        settings.on_hpc = 1
        #read_tmps_txt_file()
        #create gams no gui()
        settings.use_gui=0
    
    if (settings.use_gui) and not(matplotlib.get_backend().lower().startswith('qt')):
        print(f"Warning use_gui was set to True but cannot open windows")
        settings.use_gui=0

    elif not settings.use_gui:
        print("NO GUI mode enabled (use_gui was set to False)")

    else:
        print("GUI can run on this!")

    if settings.on_hpc:
        pass
        #write the code for gams solver flags
    
    if platform.system() in ['Linux']:
        pass
        #write the code here for completing the windows path
    
    