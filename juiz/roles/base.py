import os

from .ansiblerole import AnsibleRole

class BaseRole(AnsibleRole):
	playbook = 'base.yml'
	name = 'base'
	priority = 0

	def get_ansible_vars(self):
		base = super(BaseRole, self).get_ansible_vars()
		base['runtime'] = os.path.join(os.path.dirname(__file__), '..', 'remote')
		return base