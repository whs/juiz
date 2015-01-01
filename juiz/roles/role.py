class Role(object):
	priority = 0
	name = ''

	def run(self, project, log, inventory, env):
		raise NotImplementedError

	def get_post_message(self):
		return None

	def get_env(self):
		return {}