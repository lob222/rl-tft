import subprocess
import sys
import time

annotation = subprocess.Popen([sys.executable, "./annotator_window.py"])

while True:
    status = annotation.poll()
    if status is None:
        print("Subprocess is still running...")
    else:
        print(f"Subprocess finished with exit code {status}")
        break
    time.sleep(1)