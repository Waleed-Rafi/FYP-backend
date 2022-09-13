import os
import subprocess


def run_inference():
    # os.popen("bash ./experiments/demo_vox.sh")
    # print(os.getcwd())
    # os.system("chmod 700 face_reenactment/fr_modules/experiments/demo_vox.sh")
    shellscript = subprocess.Popen(["./experiments/demo_vox.sh"])
