from .ansiblerole import AnsibleRole

class MemcacheRole(AnsibleRole):
	playbook = 'memcache.yml'
	name = 'memcache'
	priority = 3000

	def get_ansible_vars(self):
		base = super(MemcacheRole, self).get_ansible_vars()
		base['web_ip'] = self.get_ip_of_role('web')
		return base

	def get_post_message(self):
		return 'available at {} from web machines or use environment variables MEMCACHE_SERVERS'.format(', '.join(self.get_ip_of_role()))

	def get_env(self):
		return {
			'MEMCACHE_SERVERS': ','.join(['{}:11211'.format(x) for x in self.get_ip_of_role()])
		}