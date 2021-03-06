import os
import logging

from .. import deploy
from ..util import memoized

from libcloud.compute.providers import get_driver

class BaseProvider(object):
	bool_options = ['secure']

	def __init__(self, project):
		self.project = project
		self.config = project.config

		self.log = logging.getLogger('deploy')
		self.log.log(deploy.LOG_PROGRESS_TOTAL, 2*len(self.project.list_machines()))
		self.config_check()
		self.get_driver()

	def deploy(self):
		out = self.create_machines()
		return out

	def config_check(self):
		if not self.config.has_option('main', 'target'):
			raise ConfigError, 'Target not configured'

	def get_driver_name(self):
		return self.config.get('main', 'target')

	def get_driver_key(self):
		return 'target:{0}'.format(self.get_driver_name())

	def get_driver(self):
		try:
			driver = self.get_driver_name()
			self.driver_cls = get_driver(driver)
			options = self.get_driver_options()
			self.driver = self.driver_cls(**options)
		except AttributeError, e:
			raise ConfigError(*e.args)

	@memoized
	def get_driver_options(self):
		out = dict([x for x in self.config.items(self.get_driver_key()) if x[1] != ''])

		for opt in self.bool_options:
			if opt in out:
				out[opt] = self.config.getboolean(self.get_driver_key(), opt)
		return out

	def get_node(self, name):
		nodes = self.driver.list_nodes()
		formatted_name = 'juiz-{0}-{1}'.format(self.project.id, name)
		try:
			return [x for x in nodes if x.name == formatted_name][0]
		except IndexError:
			return None

	def get_ip(self, name):
		node = self.get_node(name)
		if node:
			try:
				return node.public_ips[0]
			except IndexError:
				return None
		else:
			return None

	def create_machines(self):
		machines = {}
		nodes = self.driver.list_nodes()
		wait_list = []
		for machine in self.project.list_machines():
			formatted_name = 'juiz-{0}-{1}'.format(self.project.id, machine.name)
			try:
				node = [x for x in nodes if x.name == formatted_name][0]
				self.log.info('Machine %s is already exists', machine.name)
				self.log.log(deploy.LOG_PROGRESS, 2)
				machines[machine.name] = {'node': node, 'ip': node.public_ips[0], 'name': machine.name}
			except IndexError:
				wait_list.append((machine, self.create_machine(machine, formatted_name)))


		for machine, node in wait_list:
			self.log.info('Waiting for %s to up', machine.name)
			node = self.driver.wait_until_running([node])[0][0]
			self.log.log(deploy.LOG_PROGRESS, 1)
			machines[machine.name] = {'node': node, 'ip': node.public_ips[0], 'name': machine.name}

		return machines

	def create_machine(self, machine, formatted_name):
		self.log.info('Creating machine %s', machine.name)
		self.pre_create_machine(machine)
		node = self.driver.create_node(
			name=formatted_name,
			size=self.get_size(machine),
			image=self.get_image(machine),
			location=self.get_location(machine),
			auth=self.get_auth(machine),
			**self.get_extra_create_options(machine)
		)
		self.post_create_machine(machine, node)
		self.log.log(deploy.LOG_PROGRESS, 1)
		self.log.info('%s created', machine.name)
		return node

	def pre_create_machine(self, machine):
		pass

	def post_create_machine(self, machine, node):
		pass

	def get_image(self, machine):
		raise NotImplementedError

	@memoized
	def get_size(self, machine):
		out = self.driver.list_sizes()[0]
		self.log.debug('Using size %s', out.name)
		return out

	@memoized
	def get_location(self, machine):
		out = [x for x in self.driver.list_locations() if 
			x.id == self.get_driver_options()['location']][0]
		self.log.debug('Using location %s', out.name)
		return out

	def get_auth(self, machine):
		return None

	def get_ssh_key(self):
		return os.path.expanduser(self.config.get('main', 'ssh_key'))

	def get_ssh_public_key(self):
		return os.path.expanduser(self.config.get('main', 'ssh_public_key'))

	def get_extra_create_options(self, machine):
		return {}

class ConfigError(StandardError):
	pass