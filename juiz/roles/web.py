from .ansiblerole import AnsibleRole

class WebRole(AnsibleRole):
	playbook = 'web.yml'
	name = 'web'
	priority = 5000

	def get_post_message(self):
		return 'Point your DNS to {}'.format(', '.join(self.get_ip_of_role()))