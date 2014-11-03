from snack import *

__all__ = ['ClsEntryWindow']

class ClsEntryWindow:
	buttons = []
	text = ''
	input = []
	width = 40
	title = ''

	def __init__(self, screen, title, text='', buttons=['Ok', 'Cancel'], width=40, entryWidth=20):
		self.screen = screen
		self.buttons = buttons
		self.text = text
		self.width = width
		self.title = title
		self.entryWidth = entryWidth

	def add_input(self, name, default=None):
		self.input.append((name, default))

	def build_input(self):
		grid = Grid(2, len(self.input))

		self.inputbox = []
		for index, name in enumerate(self.input):
			field = Entry(self.entryWidth)

			if type(name) == tuple:
				(name, val) = name
				if isinstance(val, str if sys.version >= '3' else basestring):
					field = Entry(self.entryWidth, val)

			grid.setField(Label(name), 0, index, padding = (0, 0, 1, 0), anchorLeft = 1)
			grid.setField(field, 1, index, anchorLeft = 1)
			self.inputbox.append(field)

		return grid

	def show(self):
		buttons = ButtonBar(self.screen, self.buttons)
		text = TextboxReflowed(self.width, self.text)

		grid = GridFormHelp(self.screen, self.title, None, 1, 3)

		grid.add(text, 0, 0, padding = (0, 0, 0, 1))
		grid.add(self.build_input(), 0, 1, padding = (0, 0, 0, 1))
		grid.add(buttons, 0, 2, growx = 1)

		result = grid.runOnce()

		return {
			'button': buttons.buttonPressed(result),
			'input': dict(zip([x[0] for x in self.input], [x.value() for x in self.inputbox]))
		}
