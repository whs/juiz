#!/usr/bin/env python
import os
import subprocess

import yaml
import jinja2

APP_PATH='/app'
RELEASE_BIN='/var/juiz/buildpack/bin/release'
BUILD_DIR='/var/juiz/source'
PROCFILE_NAME='Procfile'
TEMPLATE=jinja2.Template(open(os.path.join(os.path.dirname(__file__), 'unit.jinja')).read())
TARGET='/etc/systemd/system'

def release():
	base_s = subprocess.check_output([RELEASE_BIN, BUILD_DIR])
	proc = yaml.load(base_s)
	if type(proc) != dict:
		raise TypeError, 'Release binary generated non-dictionary data'
	return proc

def procfile():
	procfile_path = os.path.join(APP_PATH, PROCFILE_NAME)
	if os.path.isfile(procfile_path):
		procfile = yaml.load(open(procfile_path).read())
		if type(procfile) != dict:
			raise TypeError, 'Procfile contains non-dictionary data'
		return procfile
	return {}

def get_process_types():
	release_data = release()
	release_proc = {}
	if 'default_process_types' in release_data:
		release_proc = release_data['default_process_types']
	proc = dict(release_proc.items() + procfile().items())
	return proc

def generate_unit(units):
	for key, value in units.iteritems():
		TEMPLATE.stream(
			key=key,
			value=value
		).dump(os.path.join(TARGET, 'juiz-{}.service'.format(key)))

if __name__ == '__main__':
	generate_unit(get_process_types())
