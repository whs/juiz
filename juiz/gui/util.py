import os
import sys
import subprocess

def run_terminal(cmd):
	if sys.platform == 'darwin':
		terminal_bin = 'osx-terminal'
	else:
		terminal_bin = 'linux-terminal'
	
	terminal_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cmd', terminal_bin)
	subprocess.Popen([terminal_path, cmd])