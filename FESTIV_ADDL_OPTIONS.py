# %Use Default Sub-Models. If "NO" then FESTIV will skip the running of the
# %sub-model, and if an additional sub-model is used in its place (e.g., from
# %a different program other than GAMS), then a functional mod must be put in
# %place either before or after the sub-model.

import settings
import numpy as np

def festiv_addl_options():
    settings.use_Default_DASCUC = 1
    settings.use_Default_RTSCUC = 1
    settings.use_Default_RTSCED = 1
    settings.use_Default_SCRPU  = 1
    settings.use_Default_AGC    = 1

    # %How to define starts for RTSCUC. RTC Default is 1, RPU default is 2. Any
    # %other value is user-defined, and requires modification to RTSCUCSTART.py.

    settings.RTSCUCSTART_MODE_RTC = 1
    settings.RTSCUCSTART_MODE_RPU = 2

    # %How to define how an RPU is triggered. Default is 1. Any other value is
    # %user-defined and requires modification to RPU_TRIGGER.py.
    settings.RPU_TRIGGER_MODE = 1

    # %Whether to stop with a breakpoint if there are any infeasibilities.
    settings.Stop_for_Infeasibilities = 1

    # %Absolute Line Flow Exceedance in Energy (ALFEE) Monitoring. ALFEE
    # %calculations can take substantial computation time and should only be
    # %monitored if a focus is to look at the exceedance in actual time
    # %resolution.
    settings.monitor_ALFEE = 0

    # %Pump parameters. Fix_RT_Pump of 1 if the real-time RTSCUC fixes the PSH (GEN_TYPE = 6) mode in
    # %real-time mode from the DASCUC solution. A value of 0 allows for RTSCUC to
    # %modify the commitment of the PSH from the DASCUC solution.
    settings.Fix_RT_Pump = 1

    settings.reg_proportion = 2 #1 by ramp rate, 2 by reg schedule, 3 from model rule

    #Settlement Option
    settings.DA2RTInterval_Lining = 2
    settings.RT2ACTInterval_Lining = 3

    '''
    1: Real-time intervals balance schedule with day-ahead from top of
    interval. Ex. if hourly DASCUC, 1:05, 1:10... 1:55, 2:00 real-time 
    intervals balance off 1:00 DASCUC interval.
    2: Real-time intervals balance schedule with day-ahead from middle of
    interval. Ex. if hourly DASCUC, 0:35, 0:40, 0:45... 1:25, 1:30 real-time 
    intervals balance off 1:00 DASCUC interval.
    3: Real-time intervals balance schedule with day-ahead from bottom of
    interval. Ex. if hourly DASCUC, 0:05, 0:10, 0:15... 0:50, 0:55 real-time 
    intervals balance off 1:00 DASCUC interval.
    Similar cases are for actual intervals aligning to real-time dispatch.
    '''

    settings.max_price = 1000; #This caps the price only for settlement purposes.

    # %Include other directories that are used. For example, some companies may
    # %want to include a github directory for their own Mods or organize those
    # %mods in a specific fashion. For each new path to include, you may either
    # %include the full path description, e.g., 'C:\Users\...\my_mod_folder' or a
    # %folder that is within the FESTIV directory, e.g.,
    # %{strcat(DIRECTORY,filesep,'MODEL_RULES\projectX_Modes')}, with each separated by a semicolon.
    # %Do not use a brace [] if only including one directory.

    settings.other_paths_to_include = {}

    # for k=1:size(other_paths_to_include,1)
    #     addpath(other_paths_to_include{k,1});
    # end 
    # github issue


    # %Forecast error when using forecast creation type of 4, in % actual
    # %Note that these are the standard deviation based on the energy level
    # %for example if value is .1, then forecast is actual + randn()*.1*actual
    settings.dac_vg_error = np.zeros((24, 1))
    settings.dac_load_error = np.zeros((24, 1))
    settings.rtc_vg_error = np.zeros((10, 1))
    settings.rtc_load_error = np.zeros((10, 1))
    settings.rtd_vg_error = np.zeros((5, 1))
    settings.rtd_load_error = np.zeros((5, 1))

    # %Dispatch Schedule Type (CURRENTLY NOT COMPLETE)
    # %{
    # 1: normal for dispatch that ramps continuously to meet schedule.
    # 2: ramp to schedule early and stay, like how is done in WECC
    # %}

    settings.Dispatch_Schedule_Type = 2
    settings.Dispatch_Schedule_Type2_begin = 10
    settings.Dispatch_Schedule_Type2_end = 10

    # %Printing results kills a lot of time. For now use this to say whether or
    # %not you would like to have all results thrown onto excel spreadsheet. Test
    # %inputs inside the loop would be a much timelier method if only certain
    # %results are of interest. At end of simulation there is chance to print
    # %only binding results.

    settings.RTCPrintResults = 0
    settings.RTDPrintResults = 0

    settings.eps = 0.0000001