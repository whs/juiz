import os

from .mixin import *
from .deploy import Deployable
from .config import config

__all__ = ['Project', 'NoProjectException']

class Project(ConfigMixin, MachineMixin, Deployable):
	root = None
	id = None

	def __init__(self, path, *args, **kwargs):
		super(Project, self).__init__(*args, **kwargs)

		if not os.path.isdir(os.path.join(path, config.get('main', 'project_folder'))):
			raise NoProjectException()

		self.root = path
		self.load_config(self.root)
		self.id = open(os.path.join(self.root, config.get('main', 'project_folder'), 'id')).read()

	@property
	def name(self):
		return os.path.basename(self.root)


class NoProjectException(IOError):
	pass