from pathlib import Path
import os

def locate(filename):
    cwd = Path(os.getcwd())
    cwd_new = str(cwd)+'\Credentials'
#    cwd_new = str(cwd.parent)+'\Credentials'
        
    for r,d,f in os.walk(cwd_new):
        for files in f:
            if files == filename:
                path = os.path.join(r,files)
              
    with open(path, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
    return(content)