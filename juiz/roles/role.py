class Role(object):
	priority = 0
	name = ''

	def run(self, project, log, inventory):
		raise NotImplementedError

	def get_post_message(self):
		return None