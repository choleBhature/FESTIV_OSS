import scipy.io
import h5py
import numpy as np
import os

def load_mat_file(mat_file_path):
    """Load a .mat file using scipy.io.loadmat or h5py for HDF5 format."""
    try:
        # Try loading with scipy.io.loadmat (works for v7 or earlier)
        data = scipy.io.loadmat(mat_file_path)
        print(f"Loaded {mat_file_path} using scipy.io.loadmat")
        return data
    except NotImplementedError:
        # If scipy.io fails (likely HDF5 format), use h5py
        print(f"Failed to load with scipy.io, trying h5py for {mat_file_path}")
        data = {}
        with h5py.File(mat_file_path, 'r') as f:
            for key in f.keys():
                if not key.startswith('#'):  # Skip HDF5 metadata
                    data[key] = f[key][:] if isinstance(f[key], h5py.Dataset) else f[key]
        return data

def is_ui_component(data):
    """Check if data is a MATLAB UI component (struct with 'Style' field)."""
    if isinstance(data, np.ndarray) and data.dtype.names and 'Style' in data.dtype.names:
        return True
    return False

def map_ui_to_pyqt(ui_data):
    """Map MATLAB UI component properties to PyQt-compatible dictionary."""
    style = ui_data['Style'][0, 0] if 'Style' in ui_data.dtype.names else ''
    style = ''.join(chr(c) for c in style) if isinstance(style, np.ndarray) else style

    # Initialize PyQt properties
    pyqt_props = {'type': None, 'properties': {}}

    # Map MATLAB uicontrol styles to PyQt widgets
    if style.lower() == 'pushbutton':
        pyqt_props['type'] = 'QPushButton'
        if 'String' in ui_data.dtype.names:
            pyqt_props['properties']['text'] = ''.join(chr(c) for c in ui_data['String'][0, 0]) if isinstance(ui_data['String'][0, 0], np.ndarray) else str(ui_data['String'][0, 0])
    elif style.lower() == 'edit':
        pyqt_props['type'] = 'QLineEdit'
        if 'String' in ui_data.dtype.names:
            pyqt_props['properties']['text'] = ''.join(chr(c) for c in ui_data['String'][0, 0]) if isinstance(ui_data['String'][0, 0], np.ndarray) else str(ui_data['String'][0, 0])
    elif style.lower() == 'slider':
        pyqt_props['type'] = 'QSlider'
        if 'Value' in ui_data.dtype.names:
            pyqt_props['properties']['value'] = float(ui_data['Value'][0, 0])
    elif style.lower() == 'text':
        pyqt_props['type'] = 'QLabel'
        if 'String' in ui_data.dtype.names:
            pyqt_props['properties']['text'] = ''.join(chr(c) for c in ui_data['String'][0, 0]) if isinstance(ui_data['String'][0, 0], np.ndarray) else str(ui_data['String'][0, 0])

    # Add position if available
    if 'Position' in ui_data.dtype.names:
        pos = ui_data['Position'][0, 0]
        pyqt_props['properties']['geometry'] = [int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3])]

    return pyqt_props if pyqt_props['type'] else None

def append_to_settings(mat_data, settings_file='settings2.py'):
    """Append .mat file variables to settings.py, handling scalars, strings, and UI components."""
    # Read existing settings.py to check for existing variables
    existing_vars = set()
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            for line in f:
                if line.strip().startswith('#') or not '=' in line:
                    continue
                var_name = line.split('=')[0].strip()
                existing_vars.add(var_name)

    # Append new variables to settings.py
    with open(settings_file, 'a') as f:
        f.write('\n# Variables loaded from .mat file\n')
        f.write('import numpy as np\n')  # Ensure numpy is imported for arrays
        f.write('from PyQt5.QtWidgets import QPushButton, QLineEdit, QSlider, QLabel\n')  # Import PyQt widgets
        for key, value in mat_data.items():
            if key in ('__header__', '__version__', '__globals__', 'None'):  # Skip MATLAB metadata and invalid names
                print(f"Skipping invalid or metadata variable '{key}'")
                continue
            if key in existing_vars:
                print(f"Skipping '{key}' as it already exists in {settings_file}")
                continue

            # Handle UI components
            if is_ui_component(value):
                pyqt_props = map_ui_to_pyqt(value)
                if pyqt_props:
                    f.write(f"{key} = {repr(pyqt_props)}\n")
                    print(f"Added UI component '{key}' as PyQt definition to {settings_file}")
                continue

            # Handle char arrays or string arrays
            if isinstance(value, np.ndarray) and value.dtype.kind in ('U', 'S'):
                if value.size == 1:
                    # Single string (e.g., 'hello')
                    value_str = repr(str(value.item()))
                else:
                    # Array of strings or characters
                    value_str = repr(np.char.decode(value, 'utf-8').tolist() if value.dtype.kind == 'S' else value.tolist())
                f.write(f"{key} = {value_str}\n")
                print(f"Added string variable '{key}' to {settings_file}")
                continue

            # Handle 1x1 scalars (convert to simple Python variable)
            if isinstance(value, np.ndarray) and value.size == 1:
                scalar_value = value.item()  # Extract scalar
                value_str = repr(scalar_value)
                f.write(f"{key} = {value_str}\n")
                print(f"Added scalar variable '{key}' to {settings_file}")
                continue

            # Handle other arrays (convert to NumPy array)
            if isinstance(value, np.ndarray):
                value_str = f"np.array({np.array2string(value, separator=', ')})"
                f.write(f"{key} = {value_str}\n")
                print(f"Added array variable '{key}' to {settings_file}")
                continue

            # Fallback for other types
            value_str = repr(value)
            f.write(f"{key} = {value_str}\n")
            print(f"Added variable '{key}' to {settings_file}")

def main():
    mat_file_path = r'C:\Users\priya\OneDrive\Desktop\FESTIV_OSS\FESTIV_OSS\tempws.mat'  # Path from your error
    if not os.path.exists(mat_file_path):
        print(f"Error: {mat_file_path} not found!")
        return
    mat_data = load_mat_file(mat_file_path)
    append_to_settings(mat_data, settings_file='settings2.py')  # Use settings2.py as per your error

if __name__ == "__main__":
    main()