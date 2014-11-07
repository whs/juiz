import os

from .mixin import *

__all__ = ['Project', 'NoProjectException']

class Project(object, ConfigMixin, MachineMixin):
	root = None

	def __init__(self, path, *args, **kwargs):
		super(Project, self).__init__(*args, **kwargs)

		if not os.path.isdir(os.path.join(config.get('main', 'project_folder'))):
			raise NoProjectException()

		self.root = path
		self.load_config(self.root)

	@property
	def name(self):
		return os.path.basename(self.root)

class NoProjectException(IOError):
	pass