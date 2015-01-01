from .ansiblerole import AnsibleRole

class WebRole(AnsibleRole):
	playbook = 'web.yml'
	name = 'web'
	priority = 5000

	def get_post_message(self):
		hosts = self.inventory.get_hosts(self.name)
		return 'Point your DNS to {}'.format(', '.join([x.vars['ansible_ssh_host'] for x in hosts]))