# %The parameters can be changed by the user if using hardware which does not
# %allow GUI or if using on NREL high performance computer (or other unique
# %hardware). GAMS solver flags set here as well.

import settings

def gui_hpc_options():
    settings.use_gui = 1;    # default is use gui
    settings.on_hpc  = 0;    # default is no hpc
    settings.gams_mip_flag = ' ' #these can be blank if they are not used in gams.
    settings.gams_lp_flag = ' '; #these can be blank if they are not used in gams.