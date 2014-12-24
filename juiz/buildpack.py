import os
import subprocess
import shutil
import json
import fcntl

import requests

from . import download as download_mod
from . import config

BUILDPACK_PATH = os.path.join(config.get_root(), 'buildpack')
BUILDPACK_CFG = os.path.join(config.get_root(), 'buildpack.json')

_cfg = {
	'buildpack': {}
}

def load_cfg():
	global _cfg
	try:
		_cfg = json.load(open(BUILDPACK_CFG, 'r'))
	except (IOError, ValueError):
		pass

def save_cfg():
	with open(BUILDPACK_CFG, 'w') as fp:
		fcntl.lockf(fp, fcntl.LOCK_EX)
		json.dump(_cfg, fp, indent=4)
		fcntl.lockf(fp, fcntl.LOCK_UN)
		fp.flush()

def list():
	return _cfg['buildpack']

def get_path(name):
	return os.path.join(BUILDPACK_PATH, name)

def download(name, url):
	"""Download and install a buildpack"""
	fetch(name, url)
	if not check(name):
		remove(name)
		return False

	_cfg['buildpack'][name] = {
		'name': name,
		'source': url
	}

	save_cfg()

	return True

def fetch(name, url):
	dl = download_mod.sniff(url)

	try:
		os.mkdir(BUILDPACK_PATH)
	except OSError:
		pass

	dl.get(get_path(name))
	dl.extract()

def check(name):
	detect_bin = os.path.join(get_path(name), 'bin', 'detect')
	return os.access(detect_bin, os.X_OK)

def remove(name):
	shutil.rmtree(get_path(name))

	if name in _cfg['buildpack']:
		del _cfg['buildpack'][name]

def detect(project_path='.'):
	for name in list().keys():
		path = get_path(name)
		detect = os.path.join(path, 'bin', 'detect')
		try:
			subprocess.check_call([detect, project_path], stdout=subprocess.PIPE)
			return _cfg['buildpack'][name]
		except subprocess.CalledProcessError:
			pass