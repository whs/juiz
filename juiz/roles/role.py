class Role(object):
	priority = 0
	name = ''
	machine_config_gui = ''

	def run(self, project, log, inventory, env):
		raise NotImplementedError

	def get_post_message(self):
		return None

	def get_env(self):
		return {}