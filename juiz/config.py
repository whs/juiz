import os.path

import ConfigParser

config = ConfigParser.ConfigParser()

def load(path):
	return config.read(path)

def get_root():
	return os.path.expanduser(config.get('main', 'path'))

load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default.cfg'))
load(['/etc/juiz.cfg', os.path.expanduser('~/.juiz.cfg')])