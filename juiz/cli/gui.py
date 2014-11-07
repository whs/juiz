import os
import wx

from .. import bootstrap
from ..project import *
from ..gui import main
from .base import Command

def command(fn):
	def func(*args, **kwargs):
		bootstrap()
		return fn(*args, **kwargs)

	return func

class GUI(Command):
	def build_args(self, parser):
		parser = parser.add_parser('gui', help='Run gui')
		parser.add_argument('project_dir', nargs='?')
		parser.set_defaults(func=self.gui)

	@command
	def gui(self, args):
		project = None
		main.bootstrap()
		if args.project_dir:
			try:
				project = Project(os.path.abspath(os.path.expanduser(args.project_dir)))
			except NoProjectException:
				return main.error('Project configuration folder not found.')
		main.run(project)


gui_cmd = GUI()