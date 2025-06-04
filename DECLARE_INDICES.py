import pandas as pd
import h5py
import os
import settings

def load_system_indices():
    """Load SYSTEM tab indices"""
    
    if settings.useHDF5 == 0:
        # Read from Excel file
        df = pd.read_excel(settings.inputPath, sheet_name='SYSTEM', usecols='A:A', nrows=20)
        headers = df.iloc[:, 0].tolist()
    else:
        # Read from HDF5 file
        input_dir = os.path.dirname(settings.inputPath)
        input_name = os.path.splitext(os.path.basename(settings.inputPath))[0]
        fileName = os.path.join(input_dir, f"{input_name}.h5")
        
        with h5py.File(fileName, 'r') as f:
            headers = f['/Main Input File/SYSTEM']['Property'][:]
            headers = [h.decode() if isinstance(h, bytes) else h for h in headers]
    
    # Find indices for each parameter
    try:
        settings.slack_bus = headers.index('SLACK_BUS') + 1  # +1 for MATLAB 1-based indexing
    except ValueError:
        settings.slack_bus = None
        
    try:
        settings.mva_pu = headers.index('MVA_PERUNIT') + 1
    except ValueError:
        settings.mva_pu = None
        
    try:
        settings.voll = headers.index('VOLL') + 1
    except ValueError:
        settings.voll = None
    
    # Optional parameters with try-catch equivalent
    try:
        settings.inertia_load = headers.index('INERTIALOAD') + 1
    except ValueError:
        settings.inertia_load = None
        
    try:
        settings.dfmax = headers.index('DFMAX') + 1
    except ValueError:
        settings.dfmax = None
        
    try:
        settings.load_damping = headers.index('LOAD_DAMPING') + 1
    except ValueError:
        settings.load_damping = None
        
    try:
        settings.db_max = headers.index('DBMAX') + 1
    except ValueError:
        settings.db_max = None
        
    try:
        settings.frequency = headers.index('FREQUENCY') + 1
    except ValueError:
        settings.frequency = None
        
    try:
        settings.first_stage_startup = headers.index('FIRST_STAGE_STARTUP') + 1
    except ValueError:
        settings.first_stage_startup = None

def load_gen_indices():
    """Load GEN tab indices"""
    
    if settings.useHDF5 == 0:
        # Read from Excel file
        df = pd.read_excel(settings.inputPath, sheet_name='GEN', usecols='B:AZ', nrows=1)
        headers = df.columns.tolist()
    else:
        input_dir = os.path.dirname(settings.inputPath)
        input_name = os.path.splitext(os.path.basename(settings.inputPath))[0]
        fileName = os.path.join(input_dir, f"{input_name}.h5")
        
        with h5py.File(fileName, 'r') as f:
            gen_data = f['/Main Input File/GEN']
            headers = list(gen_data.keys())[1:]  # Skip first field
    
    # Map all GEN parameters
    gen_params = {
        'capacity': 'CAPACITY',
        'noload_cost': 'NO_LOAD_COST',
        'su_cost': 'STARTUP_COST',
        'mr_time': 'MIN_RUN_TIME',
        'md_time': 'MIN_DOWN_TIME',
        'ramp_rate': 'RAMP_RATE',
        'min_gen': 'MIN_GEN',
        'gen_type': 'GEN_TYPE',
        'su_time': 'STARTUP_TIME',
        'sd_time': 'SHUTDOWN_TIME',
        'agc_qualified': 'AGC_QUALIFIED',
        'max_starts': 'MAX_STARTS',
        'initial_status': 'INITIAL_STATUS',
        'initial_hour': 'INITIAL_HOUR',
        'initial_MW': 'INITIAL_MW',
        'forced_outage_rate': 'FORCED_OUTAGE_RATE',
        'mttr': 'MTTR',
        'variable_start': 'VARIABLE_STARTUP',
        'behavior_rate': 'BEHAVIOR_RATE',
        'inertia': 'INERTIA',
        'droop': 'DROOP',
        'gov_db': 'GOV_DB',
        'gov_beta': 'GOV_BETA',
        'gov_tg': 'GOV_TG',
        'gen_agc_mode': 'GEN_AGC_MODE',
        'q_max': 'Q_MAX',
        'q_min': 'Q_MIN',
        'pucost': 'PERUNIT_COST'
    }
    
    for param, header_name in gen_params.items():
        try:
            setattr(settings, param, headers.index(header_name) + 1)
        except ValueError:
            setattr(settings, param, None)

def load_storage_indices():
    """Load STORAGE tab indices"""
    
    try:
        if settings.useHDF5 == 0:
            df = pd.read_excel(settings.inputPath, sheet_name='STORAGE', usecols='B:AZ', nrows=1)
            headers = df.columns.tolist()
        else:
            input_dir = os.path.dirname(settings.inputPath)
            input_name = os.path.splitext(os.path.basename(settings.inputPath))[0]
            fileName = os.path.join(input_dir, f"{input_name}.h5")
            
            with h5py.File(fileName, 'r') as f:
                storage_data = f['/Main Input File/STORAGE']
                headers = list(storage_data.keys())[1:]  # Skip first field
        
        storage_params = {
            'max_pump': 'MAX_PUMP',
            'min_pump': 'MIN_PUMP',
            'min_pump_time': 'MIN_PUMP_TIME',
            'pump_su_time': 'PUMP_STARTUP_TIME',
            'pump_sd_time': 'PUMP_SHUTDOWN_TIME',
            'pump_ramp_rate': 'PUMP_RAMP_RATE',
            'initial_storage': 'INITIAL_STORAGE',
            'final_storage': 'FINAL_STORAGE',
            'storage_max': 'STORAGE_MAX',
            'efficiency': 'EFFICIENCY',
            'reservoir_value': 'RESERVOIR_VALUE',
            'initial_pump_status': 'INITIAL_PUMP_STATUS',
            'initial_pump_mw': 'INITIAL_PUMP_MW',
            'initial_pump_hour': 'INITIAL_PUMP_HOUR',
            'variable_efficiency': 'VARIABLE_EFFICIENCY',
            'enforce_final_storage': 'ENFORCE_FINAL_STORAGE'
        }
        
        for param, header_name in storage_params.items():
            try:
                setattr(settings, param, headers.index(header_name) + 1)
            except ValueError:
                setattr(settings, param, None)
                
    except Exception:
        # If STORAGE tab doesn't exist or has issues, skip
        pass

def load_reserve_indices():
    """Load RESERVE tab indices"""
    
    try:
        if settings.useHDF5 == 0:
            df = pd.read_excel(settings.inputPath, sheet_name='RESERVEPARAM', usecols='B:AZ', nrows=1)
            headers = df.columns.tolist()
        else:
            input_dir = os.path.dirname(settings.inputPath)
            input_name = os.path.splitext(os.path.basename(settings.inputPath))[0]
            fileName = os.path.join(input_dir, f"{input_name}.h5")
            
            with h5py.File(fileName, 'r') as f:
                reserve_data = f['/Main Input File/RESERVEPARAM']
                headers = list(reserve_data.keys())[1:]  # Skip first field
        
        reserve_params = {
            'res_on': 'RESERVE_ON',
            'res_time': 'RESERVE_TIME',
            'res_dir': 'RESERVE_DIR',
            'res_agc': 'RESERVE_AGC',
            'res_gov': 'RESERVE_GOV',
            'res_inertia': 'RESERVE_INERTIA',
            'res_inclusive': 'RESERVE_INCLUSIVE',
            'res_vg': 'RESERVE_VG',
            'res_voir': 'VOIR'
        }
        
        for param, header_name in reserve_params.items():
            try:
                setattr(settings, param, headers.index(header_name) + 1)
            except ValueError:
                setattr(settings, param, None)
                
    except Exception:
        # If RESERVEPARAM tab doesn't exist or has issues, skip
        pass

def load_branch_indices():
    """Load BRANCH tab indices"""
    
    try:
        if settings.useHDF5 == 0:
            df = pd.read_excel(settings.inputPath, sheet_name='BRANCHDATA', usecols='B:AZ', nrows=1)
            headers = df.columns.tolist()
        else:
            input_dir = os.path.dirname(settings.inputPath)
            input_name = os.path.splitext(os.path.basename(settings.inputPath))[0]
            fileName = os.path.join(input_dir, f"{input_name}.h5")
            
            with h5py.File(fileName, 'r') as f:
                branch_data = f['/Main Input File/BRANCHDATA']
                headers = list(branch_data.keys())
        
        branch_params = {
            'reactance': 'REACTANCE',
            'resistance': 'RESISTANCE',
            'line_rating': 'LINE_RATING',
            'ste_rating': 'STE_RATING',
            'par_low': 'PHASE_SHIFTER_ANGLE_LOW',
            'par_hi': 'PHASE_SHIFTER_ANGLE_HIGH',
            'ctgc_monitor': 'CTGC_MONITOR',
            'branch_type': 'BRANCH_TYPE',
            'susceptance': 'SUSCEPTANCE'
        }
        
        # Find indices
        indices = {}
        for param, header_name in branch_params.items():
            try:
                indices[param] = headers.index(header_name) + 1
            except ValueError:
                indices[param] = None
        
        # Calculate offset (equivalent to MATLAB offset calculation)
        valid_indices = [idx for idx in indices.values() if idx is not None]
        if valid_indices:
            firstcol = min(valid_indices)
            offset = 1 - firstcol
            
            # Apply offset to all indices
            for param in branch_params.keys():
                if indices[param] is not None:
                    setattr(settings, param, indices[param] + offset)
                else:
                    setattr(settings, param, None)
        
    except Exception:
        # If BRANCHDATA tab doesn't exist or has issues, skip
        pass

def load_ace_indices():
    """Load ACE indices (these are fixed)"""
    settings.ACE_time_index = 1
    settings.raw_ACE_index = 2
    settings.integrated_ACE_index = 3
    settings.CPS2_ACE_index = 4
    settings.SACE_index = 5
    settings.AACEE_index = 6

def load_type_indices():
    """Load generator and branch type indices (these are fixed)"""
    
    # Generator types
    settings.steam_gen_type_index = 1
    settings.CT_gen_type_index = 2
    settings.combined_cycle_gen_type_index = 3
    settings.hydro_gen_type_index = 4
    settings.nuclear_gen_type_index = 5
    settings.pumped_storage_gen_type_index = 6
    settings.wind_gen_type_index = 7
    settings.ESR_gen_type_index = 8
    settings.LESR_gen_type_index = 9
    settings.PV_gen_type_index = 10
    settings.CSP_gen_type_index = 11
    settings.demandresponse_gen_type_index = 12
    settings.virtual_gen_type_index = 13
    settings.interface_gen_type_index = 14
    settings.outage_gen_type_index = 15
    settings.variable_dispatch_gen_type_index = 16
    
    # Branch types
    settings.transmission_line_branch_type_index = 1
    settings.fixed_par_branch_type_index = 2
    settings.adj_par_branch_type_index = 3
    settings.HVDC_branch_type_index = 4

def load_all_indices():
    """Load all tab indices"""
    load_system_indices()
    load_gen_indices()
    load_storage_indices()
    load_reserve_indices()
    load_branch_indices()
    load_ace_indices()
    load_type_indices()

# Usage:
# if __name__ == "__main__":
#     load_all_indices()