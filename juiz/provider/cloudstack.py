from .base import BaseProvider
from ..util import memoized

class CloudStackProvider(BaseProvider):
	@memoized
	def get_image(self, machine):
		out = self.find_by_config_key(self.driver.list_images(), 'image')
		self.log.debug('Using image %s', out.name)
		return out

	def get_location(self, machine):
		return None

	@memoized
	def get_size(self, machine):
		out = self.find_by_config_key(self.driver.list_sizes(), 'size')
		self.log.debug('Using size %s', out.name)
		return out

	@memoized
	def get_network(self):
		out = self.find_by_config_key(self.driver.ex_list_networks(self.get_project()), 'network')
		self.log.debug('Using network %s', out.displaytext)
		return out

	@memoized
	def get_project(self):
		if self.get_driver_options()['project'] in ('None', None, ''):
			return None

		out = self.find_by_config_key(self.driver.ex_list_projects(), 'project')
		self.driver.project = out
		self.log.debug('Using project %s', out.display_text)
		return out

	def get_free_ip(self):
		ip = self.driver.ex_allocate_public_ip(network_id=self.get_network().id, project_id=self.get_project().id if self.get_project() else None)
		self.log.debug('Using IP %s', ip.address)
		return ip

	def post_create_machine(self, machine, node):
		self.driver.ex_enable_static_nat(node, self.get_free_ip(), self.get_network())

	def get_extra_create_options(self, machine):
		return {
			'networks': [self.get_network()],
			'project': self.get_project()
		}

	def find_by_config_key(self, lst, key):
		target = self.get_driver_options()[key]
		return [x for x in lst if x.id == target][0]