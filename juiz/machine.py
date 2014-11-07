import re

class Machine(object):
	name = ''
	roles = []

	def __init__(self, name):
		self.name = name

	@classmethod
	def from_config(cls, name, config):
		machine = cls(name)
		key = 'machine:{0}'.format(name)
		
		for name, val in config.items(key):
			if re.match('^role[0-9]+$', name):
				machine.roles.append(val)

		return machine