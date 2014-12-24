from libcloud.compute.base import NodeAuthSSHKey

from .base import BaseProvider
from ..util import memoized

class AWSProvider(BaseProvider):
	images = {
		'us-east-1': 'ami-96a818fe',
		'us-west-2': 'ami-c7d092f7',
		'us-west-1': 'ami-6bcfc42e',
		'eu-west-1': 'ami-e4ff5c93',
		'ap-southeast-1': 'ami-aea582fc',
		'ap-northeast-1': 'ami-89634988',
		'ap-southeast-2': 'ami-bd523087',
		'sa-east-1': 'ami-bf9520a2'
	}

	@memorized
	def get_image(self, machine):
		out = self.driver.get_image(self.get_image_name())
		self.log.debug('Using image %s', out.name)
		return out

	def get_image_name(self):
		region = self.config.get(self.get_driver_key(), 'region')
		return self.images[region]

	def get_location(self, machine):
		return None

	@memoized
	def get_size(self, machine):
		out = [x for x in self.driver.list_sizes() if x.id == 'm3.medium'][0]
		self.log.debug('Using size %s', out.name)
		return out

	def get_auth(self, machine):
		return NodeAuthSSHKey(open(self.get_driver_options()['ssh_key'] + '.pub').read())