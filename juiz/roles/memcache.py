from .ansiblerole import AnsibleRole

class MemcacheRole(AnsibleRole):
	playbook = 'memcache.yml'
	name = 'memcache'
	priority = 3000