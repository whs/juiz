from .ansiblerole import AnsibleRole

class MySQLRole(AnsibleRole):
	playbook = 'mysql.yml'
	name = 'mysql'
	priority = 3000