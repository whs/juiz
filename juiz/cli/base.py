from .registry import registry

class Command(object):
	def __init__(self):
		registry.append(self)

	def build_args(self, parser):
		pass
