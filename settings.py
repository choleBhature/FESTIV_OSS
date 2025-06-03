#GLOBAL VARS FILE 
import numpy as np

execution_from_previous = 0

time = 0 
tRTC = 0
RTSCUC_binding_interval_index = 0


use_gui = 1
on_hpc  = 0    
gams_mip_flag = ' '
gams_lp_flag = ' '

#from the FESTIV_ADDL_OPTIONS file

use_Default_DASCUC = 0
use_Default_RTSCUC = 0
use_Default_RTSCED = 0
use_Default_SCRPU  = 0
use_Default_AGC    = 0

RTSCUCSTART_MODE_RTC = 0
RTSCUCSTART_MODE_RPU = 0

RPU_TRIGGER_MODE = 0

Stop_for_Infeasibilities = 0


monitor_ALFEE = 0

Fix_RT_Pump = 0

reg_proportion = 0

DA2RTInterval_Lining = 0
RT2ACTInterval_Lining = 0

max_price = 0

#use [] if no need of multiple paths
other_paths_to_include={}

dac_vg_error = np.zeros((24, 1))
dac_load_error = np.zeros((24, 1))
rtc_vg_error = np.zeros((10, 1))
rtc_load_error = np.zeros((10, 1))
rtd_vg_error = np.zeros((5, 1))
rtd_load_error = np.zeros((5, 1))

Dispatch_Schedule_Type = 0
Dispatch_Schedule_Type2_begin = 0
Dispatch_Schedule_Type2_end = 0

RTCPrintResults = 0
RTDPrintResults = 0

eps = 0