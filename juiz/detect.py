import os
import subprocess

from . import buildpack

def detect():
	for name in buildpack.list().keys():
		path = buildpack.get_path(name)
		detect = os.path.join(path, 'bin', 'detect')
		try:
			subprocess.check_call([detect, '.'], stdout=subprocess.PIPE)
			return name
		except subprocess.CalledProcessError:
			pass