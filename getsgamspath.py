import os
import platform
import subprocess
import re
from pathlib import Path

def getgamspath():
    """
    Generically determine the path for gamside.exe
    """
    
    # Check if running on Microsoft Windows
    if platform.system() == 'Windows':
        # VD added several lines to skip searching for 'gamside.exe' (saves ~20 sec) where possible
        
        try:
            # Try to open pathfile.txt
            with open('pathfile.txt', 'r') as f:
                path = f.read()
        except FileNotFoundError:
            # If file doesn't exist, create it by capturing PATH environment variable
            try:
                # Get system PATH and write to file
                path = os.environ.get('PATH', '')
                with open('pathfile.txt', 'w') as f:
                    f.write(path)
            except Exception:
                path = ''
        
        if path:
            # Select GAMS-related paths using regex (case insensitive)
            gamspathcell = re.findall(r'[^;]+[gG][aA][mM][sS][^;]+', path)
            
            if len(gamspathcell) == 1:
                # If there is one path referring to GAMS, use it
                potential_path = gamspathcell[0]
                fullpath = os.path.join(potential_path, 'gamside.exe')
                
                # Check if gamside.exe exists at this path
                if os.path.isfile(fullpath):
                    return potential_path
            
            # If there are several GAMS paths or none is found, search for 'gamside.exe'
            else:
                try:
                    # Search for gamside.exe recursively from C drive
                    # Using 'where' command on Windows (equivalent to 'dir /s')
                    result = subprocess.run(['where', '/R', 'C:\\', 'gamside.exe'], 
                                          capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        
                        for line in lines:
                            # Look for lines containing 'GAMS'
                            if 'GAMS' in line.upper():
                                # Extract the directory path
                                gamspath = os.path.dirname(line)
                                return gamspath
                    
                    # Alternative method using os.walk if 'where' command fails
                    for root, dirs, files in os.walk('C:\\'):
                        if 'gamside.exe' in files and 'GAMS' in root.upper():
                            return root
                            
                except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
                    # If subprocess fails, try using pathlib to search
                    try:
                        for path_obj in Path('C:\\').rglob('gamside.exe'):
                            if 'GAMS' in str(path_obj).upper():
                                return str(path_obj.parent)
                    except Exception:
                        pass
        
        # If nothing found, return empty string
        return ''
    
    else:
        # For non-Windows platforms
        print("Warning: For non-Windows platforms the path to gams files are assumed to be in system PATH")
        return ''

# Example usage:
# if __name__ == "__main__":
#     gams_path = getgamspath()
#     if gams_path:
#         print(f"GAMS path found: {gams_path}")
#     else:
#         print("GAMS path not found")