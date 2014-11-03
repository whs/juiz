from .. import bootstrap
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
		parser.set_defaults(func=self.gui)

	@command
	def gui(self, args):
		main.run()


gui_cmd = GUI()