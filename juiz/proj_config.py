import fcntl
import os.path
import ConfigParser

from .config import config as app_config

config = ConfigParser.ConfigParser()

_def_get = config.get

def _get(section, name, *args, **kwargs):
	try:
		return _def_get(section, name, *args, **kwargs)
	except ConfigParser.NoOptionError:
		return app_config.get('project:{0}'.format(section), name, *args, **kwargs)

config.get = _get

_def_has_option = config.has_option

def _has_option(section, name, *args, **kwargs):
	return _def_has_option(section, name, *args, **kwargs) or app_config.has_option('project:{0}'.format(section), name, *args, **kwargs)

config.has_option = _has_option

def load(path):
	return config.read(path)

def save():
	with open(os.path.join(app_config.get('main', 'project_folder'), 'config.cfg'), 'w') as fp:
		fcntl.lockf(fp, fcntl.LOCK_EX)
		config.write(fp)
		fcntl.lockf(fp, fcntl.LOCK_UN)
		fp.flush()

load(os.path.join(app_config.get('main', 'project_folder'), 'config.cfg'))