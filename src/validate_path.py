import os

def validate_linux_path(path):
    
    if not os.path.exists(path):
        return False
    
    if not os.path.isdir(path):
        return False
    
    return True
