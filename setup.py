'''
<<<<<<< HEAD
import os
import subprocess
import sys
 
def run_in_background(script_path):
    if sys.platform.startswith("win"):
        # On Windows, use the start command to run the script in the background
        subprocess.Popen(["start", "python", f'{script_path}/elitebot.py'], shell=True)
    else:
        # On Linux, use the nohup command to run the script in the background
        subprocess.Popen(["nohup", "python3", f'{script_path}/elitebot.py', "&"], shell=True)
sys.exit
=======
nohup python3 elitebot.py &
>>>>>>> 8627ba5a471a81c71a5d1efd429439312972d75e
'''