import re

class Machine(object):
	name = ''
	roles = None

	def __init__(self, name):
		self.name = name
		self.roles = []
		self.env = {}

	def get_ip(self, project):
		driver = project.get_driver()
		return driver.get_ip(self.name)

	def get_node(self, project):
		driver = project.get_driver()
		return driver.get_node(self.name)

	@classmethod
	def from_config(cls, name, config):
		machine = cls(name)
		key = 'machine:{0}'.format(name)
		
		for role, val in config.items(key):
			if re.match('^role[0-9]+$', role):
				machine.roles.append(val)
			if role.startswith('env_'):
				machine.env[role.replace('env_', '', 1)] = val

		return machine