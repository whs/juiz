import logging
import threading
import itertools

from libcloud.compute.types import Provider
from ansible.inventory import Inventory
from ansible.inventory.group import Group
from ansible.inventory.host import Host

from . import util

providers = {
	Provider.EC2: 'juiz.provider.aws.AWSProvider',
	Provider.CLOUDSTACK: 'juiz.provider.cloudstack.CloudStackProvider',
	Provider.DIGITAL_OCEAN: 'juiz.provider.digitalocean.DigitalOceanProvider',
}

LOG_PROGRESS=6
LOG_PROGRESS_TOTAL=5

logging.addLevelName(LOG_PROGRESS, 'PROGRESS')
logging.addLevelName(LOG_PROGRESS_TOTAL, 'PROGRESS_TOTAL')

class DeployThread(threading.Thread):
	def __init__(self, project, *args, **kwargs):
		self.project = project
		super(DeployThread, self).__init__(*args, **kwargs)

	def run(self):
		self.project.deploy()

class Deployable:
	def deploy(self):
		self.__log = logging.getLogger('deploy')
		self.__log.log(LOG_PROGRESS_TOTAL, 1)
		
		nodes = get_driver(self.config.get('main', 'target'))(self).deploy()
		inventory = self.build_inventory(nodes)

		self.__log.info('Running ansible...')
		

	def build_host(self, node):
		machine = Host(node['name'])
		cfg = self.get_machine(node['name'])
		for role in cfg.roles:
			machine.add_group(role)
		machine.set_variable('ansible_ssh_host', node['ip'])
		return machine

	def build_inventory(self, nodes):
		machines = dict([(key, self.build_host(machine)) for key, machine in nodes.items()])
		inventory = Inventory()

		groups = [Group(x) for x in set(itertools.chain(*[machine.roles for machine in self.list_machines()]))]
		for group in groups:
			machine_in_group = [x for x in self.list_machines() if group.name in x.roles]
			
			for machine in machines:
				group.add_host(machines[machine])

			inventory.add_group(group)

		return inventory


def get_driver(provider):
	return util.import_by_name(providers[provider])