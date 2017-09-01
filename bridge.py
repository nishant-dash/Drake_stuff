import subprocess

def clear_terminal():
    subprocess.call('clear', shell=True)

def call_DryVR():
    subprocess.call('python main.py inputFile/input_AEB', shell=True)

if __name__ == '__main__':
    clear_terminal()
    call_DryVR()
