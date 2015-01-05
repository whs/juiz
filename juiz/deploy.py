import os
import logging
import threading
import itertools

from libcloud.compute.types import Provider
from ansible.inventory import Inventory
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible import constants
from ansible import utils

from . import util, buildpack, roles

providers = {
	Provider.EC2: 'juiz.provider.aws.AWSProvider',
	Provider.CLOUDSTACK: 'juiz.provider.cloudstack.CloudStackProvider',
	Provider.DIGITAL_OCEAN: 'juiz.provider.digitalocean.DigitalOceanProvider',
}

LOG_PROGRESS=6
LOG_PROGRESS_TOTAL=5

logging.addLevelName(LOG_PROGRESS, 'PROGRESS')
logging.addLevelName(LOG_PROGRESS_TOTAL, 'PROGRESS_TOTAL')

constants.HOST_KEY_CHECKING = False
# utils.VERBOSITY = 4

class DeployThread(threading.Thread):
	def __init__(self, project, *args, **kwargs):
		self.project = project
		super(DeployThread, self).__init__(*args, **kwargs)

	def run(self):
		self.project.deploy()

class Deployable(object):
	def get_driver(self):
		return get_driver(self.config.get('main', 'target'))(self)

	def deploy(self):
		self.__log = logging.getLogger('deploy')

		self.__log.log(LOG_PROGRESS_TOTAL, 1)
		self.buildpack_detect()
		
		nodes = self.get_driver().deploy()
		self.inventory = self.build_inventory(nodes)

		open(os.path.join(self.root, '.rsync-filter'), 'w') \
			.write('- .juiz\n- .heroku\n')

		self.__log.info('Running deployment...')
		self.run_playbooks(self.inventory)
		self.__log.info('Finished')

		for k, v in self.get_post_messages(self.inventory).iteritems():
			if not v:
				continue
			self.__log.info('{}: {}'.format(k, v))

	def buildpack_detect(self):
		self.buildpack = buildpack.detect(self.root)
		if not self.buildpack:
			raise NoBuildpackError

		self.__log.info('Using buildpack: %s', self.buildpack['name'])
		self.__log.log(LOG_PROGRESS, 1)

	def build_host(self, node):
		machine = Host(node['name'])

		env = {}
		for key, value in self.config.items('machine:{}'.format(node['name'])):
			if key.startswith('env_'):
				env[key.replace('env_', '', 1)] = value
				continue
			elif key.startswith('role'):
				continue
			machine.set_variable(key, value)

		machine.set_variable('ansible_ssh_user', 'root')
		machine.set_variable('ansible_ssh_host', node['ip'])
		machine.set_variable('ansible_ssh_private_key_file', self.config.get('main', 'ssh_key'))
		machine.set_variable('host_env', env)

		return machine

	def build_inventory(self, nodes):
		machines = dict([(key, self.build_host(machine)) for key, machine in nodes.items()])
		inventory = Inventory(None)

		# fix synchronize module
		all_group = Group('all')
		inventory.add_group(all_group)

		groups = [Group(x) for x in set(
			itertools.chain(*[
				machine.roles for machine in self.list_machines()
			])
		)]
		for group in groups:
			machine_in_group = [x for x in self.list_machines() if group.name in x.roles]
			
			for machine in machine_in_group:
				machine = machines[machine.name]
				group.add_host(machine)

			inventory.add_group(group)

		inventory.clear_pattern_cache()
		return inventory

	def run_playbooks(self, inventory):
		roles = self.list_roles(inventory)
		self.__log.log(LOG_PROGRESS_TOTAL, len(roles))
		env = {}
		for item in roles:
			item.run(self, self.__log, inventory, env)
			env = dict(env.items() + item.get_env().items())

			# cleanup
			inventory.lift_restriction()
			inventory.lift_also_restriction()

			self.__log.log(LOG_PROGRESS, 1)

	def get_post_messages(self, inventory):
		roles = self.list_roles(inventory)

		out = {}
		for item in roles:
			out[item.name] = item.get_post_message()

		return out

	@util.memoized
	def list_roles(self, inventory):
		out = ['base']
		out += [x for x in inventory.list_groups() if x != 'all']

		# build role object
		out = [util.import_by_name(roles.registry[x])() for x in out]
		out.sort(key=lambda x: x.priority)

		return out



def get_driver(provider):
	return util.import_by_name(providers[provider])

class NoBuildpackError(StandardError):
	pass