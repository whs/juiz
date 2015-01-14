import os

from .ansiblerole import AnsibleRole

class WebRole(AnsibleRole):
	playbook = 'web.yml'
	name = 'web'
	priority = 5000

	def run(self, project, *args, **kwargs):
		# ignore juiz configuration folder
		# and .heroku which some buildpack use
		open(os.path.join(project.root, '.rsync-filter'), 'w') \
			.write('- .juiz\n- .heroku\n- .bp\n')

		return super(WebRole, self).run(project, *args, **kwargs)

	def get_post_message(self):
		return 'Point your DNS to {}'.format(', '.join(self.get_ip_of_role()))