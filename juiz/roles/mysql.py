import hashlib

from .ansiblerole import AnsibleRole

class MySQLRole(AnsibleRole):
	playbook = 'mysql.yml'
	name = 'mysql'
	priority = 3000

	machine_config_gui = 'juiz.gui.role.mysql.MySQLMachineConfig'

	# must be changed in playbook too
	mysql_user='app'

	def get_root_password(self):
		host = self.inventory.get_hosts(self.name)[0]

		if 'mysql_root' in host.vars and host.vars['mysql_root']:
			return host.vars['mysql_root']
		else:
			return hashlib.sha256(self.project.id).hexdigest()

	def get_app_password(self):
		host = self.inventory.get_hosts(self.name)[0]

		if 'mysql_app' in host.vars and host.vars['mysql_app']:
			return host.vars['mysql_app']
		else:
			return hashlib.sha256(self.project.id).hexdigest()

	def get_ansible_vars(self):
		base = super(MySQLRole, self).get_ansible_vars()
		base['web_ip'] = self.get_ip_of_role('web')
		base['root_pw'] = self.get_root_password()
		base['app_pw'] = self.get_app_password()
		return base

	def get_post_message(self):
		return 'use environment variables DATABASE_URL or JUIZ_MARIADB_URL to connect'

	def get_env(self):
		ip = self.get_ip_of_role()[0]
		url = 'mysql://app:{1}@{0}/app?reconnect=true'.format(ip, self.get_app_password())
		return {
			'DATABASE_URL': url,
			'JUIZ_MARIADB_URL': url
		}