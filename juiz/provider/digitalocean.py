from libcloud.compute.base import NodeImage

from .base import BaseProvider
from ..util import memoized

class DigitalOceanProvider(BaseProvider):
	IMAGE_ID = 9801950
	ssh_key = None
	
	def get_image(self, machine):
		return NodeImage(id=self.IMAGE_ID, name='CentOS 7 x86_64', driver=self.driver)

	def deploy(self):
		self.load_ssh_key()
		return super(DigitalOceanProvider, self).deploy()

	def load_ssh_key(self):
		keys = self.driver.ex_list_ssh_keys()
		key_name = 'juiz-{}'.format(self.project.id)

		for key in keys:
			if key.name == key_name:
				self.ssh_key = key
				self.log.info('Using ssh key %s', key.name)
				return False

		self.log.info('Uploading ssh key')
		self.ssh_key = self.driver.ex_create_ssh_key(key_name, open(self.get_ssh_public_key()).read())

		return True

	def get_extra_create_options(self, machine):
		return {
			'ex_ssh_key_ids': [str(self.ssh_key.id)]
		}