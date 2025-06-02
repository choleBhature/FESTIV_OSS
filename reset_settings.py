import settings

def reset_settings_to_zero(use_float=False):
    """
    Resets all user-defined variables in settings.py to 0 (integer or float).
    
    Args:
        use_float (bool): If True, resets to 0.0 (float); if False, resets to 0 (int).
    """
    # Get all attributes from the settings module
    all_vars = dir(settings)
    
    # List of protected/special attributes to skip
    protected_vars = [
        '__builtins__', '__cached__', '__doc__', '__file__',
        '__loader__', '__name__', '__package__', '__spec__'
    ]
    
    # Choose reset value based on use_float parameter
    reset_value = 0.0 if use_float else 0
    
    # Iterate through all attributes and reset user-defined variables
    for var in all_vars:
        if var not in protected_vars and not callable(getattr(settings, var)):
            setattr(settings, var, reset_value)

# Example usage
if __name__ == "__main__":
    # Reset to 0.0 (float) for compatibility with MATLAB's floating-point numbers
    reset_settings_to_zero(use_float=True)