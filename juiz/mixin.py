import os
import fcntl
import ConfigParser
import re

from .config import config
from .machine import Machine

__all__ = ['ConfigMixin', 'MachineMixin', 'EnvironmentMixin']

class ConfigMixin(object):
	config = ConfigParser.ConfigParser()

	def __get(self, section, name, *args, **kwargs):
		try:
			return self._def_get(section, name, *args, **kwargs)
		except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
			try:
				return config.get('project:{0}'.format(section), name, *args, **kwargs)
			except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
				raise e

	def __has_option(self, section, name, *args, **kwargs):
		return self._def_has_option(section, name, *args, **kwargs) or config.has_option('project:{0}'.format(section), name, *args, **kwargs)

	def __init__(self, *args, **kwargs):
		super(ConfigMixin, self).__init__(*args, **kwargs)

		# case sensitive
		self.config.optionxform = str

		self._def_get = self.config.get
		self.config.get = self.__get
		self._def_has_option = self.config.has_option
		self.config.has_option = self.__has_option

	def load_config(self, path=''):
		path = os.path.join(path, config.get('main', 'project_folder'), 'config.cfg')
		return self.config.read(path)

	def save_config(self, path=''):
		with open(os.path.join(path, config.get('main', 'project_folder'), 'config.cfg'), 'w') as fp:
			fcntl.lockf(fp, fcntl.LOCK_EX)
			self.config.write(fp)
			fcntl.lockf(fp, fcntl.LOCK_UN)
			fp.flush()

class MachineMixin(object):
	def list_machines(self):
		return [
			self.get_machine(re.sub('^machine:', '', x))
			for x in self.config.sections() if x.startswith('machine:')
		]

	def get_machine(self, name):
		return Machine.from_config(name, self.config)

class EnvironmentMixin(object):
	def get_env(self):
		try:
			return dict(self.config.items('env'))
		except ConfigParser.NoSectionError:
			return {}
