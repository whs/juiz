from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeAuthSSHKey
from libcloud.compute.types import DeploymentError

from . import detect
from .proj_config import config

class Deploy:
	def deploy(self):
		self.config_check()
		self.detect()
		self.get_driver()
		self.provision()
		self.debug_destroy()

	def detect(self):
		self.buildpack = detect.detect()
		if not self.buildpack:
			raise NoBuildpackError

	def config_check(self):
		if not config.has_option('main', 'target'):
			raise ConfigError, 'Target not configured'
		if not config.has_option('main', 'ssh_key'):
			raise ConfigError, 'SSH Key not configured'

	def get_driver(self):
		try:
			driver = config.get('main', 'target')
			self.driver_cls = get_driver(driver)
			options = dict([x for x in config.items('driver:{0}'.format(driver)) if x[1] != ''])
			self.driver = self.driver_cls(**options)
		except AttributeError, e:
			raise ConfigError(*e.args)

	def provision(self):
		# TODO: Rewrite this to create vm based on user config
		self.driver.create_node(
			name='juiz',
			size=[x for x in self.driver.list_sizes() if x.id == '66'][0],
			image=[x for x in self.driver.list_images() if x.id == '6372526'][0],
			location=[x for x in self.driver.list_locations() if x.id == '6'][0]
		)

	def debug_destroy(self):
		for node in self.driver.list_nodes():
			print 'Debug: destroying {0}'.format(node)
			self.driver.destroy_node(node)

class ConfigError(StandardError):
	pass
class NoBuildpackError(StandardError):
	pass