import os
import re
import ConfigParser
import inspect

import snack
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from .base import Command
from ..config import config
from .. import proj_config as project_config
from . import ui

class Config(Command):
	menu_map = [
		['Target selection', 'target_select'],
		['Target configuration', 'target_config'],
		['Addons', 'addons'],
		['Machines', 'machines'],
		['Save configuration', 'save'],
	]

	def build_args(self, parser):
		parser = parser.add_parser('config', help='Run configuration tool')
		parser.set_defaults(func=self.config)

	def config(self, args):
		try:
			os.mkdir(config.get('main', 'project_folder'))
		except OSError:
			pass
		
		self.screen = snack.SnackScreen()
		self.main_menu()
		self.screen.finish()

	def update_menu_map(self):
		target = self.get_target()
		if target:
			self.menu_map[0][0] = 'Target selection [{0}]'.format(target)
		else:
			self.menu_map[0][0] = 'Target selection'

	def main_menu(self):
		self.update_menu_map()
		out = snack.ListboxChoiceWindow(
			self.screen,
			'Main menu',
			'',
			[x[0] for x in self.menu_map],
			['Enter', 'Exit'],
		)
		if out[0] == 'exit':
			self.confirm_save()
		else:
			getattr(self, self.menu_map[out[1]][1])()

	def save(self):
		self.confirm_save()
		self.main_menu()

	def confirm_save(self):
		btn = snack.ButtonChoiceWindow(
			self.screen,
			'Save',
			'Do you want to save?',
			['Yes', 'No']
		)
		if btn == 'yes':
			project_config.save()

	def target_select(self):
		options = self.get_available_drivers()
		human_options = [get_driver(x).name for x in options]
		try:
			default = options.index(self.get_target())
		except ValueError:
			default = None
		
		out = snack.ListboxChoiceWindow(
			self.screen,
			'Target selection',
			'Select a deployment target',
			human_options,
			['Ok', 'Cancel'],
			height=10, scroll=True, width=60,
			default=default
		)
		if out[0] != 'cancel':
			try:
				project_config.config.add_section('main')
			except ConfigParser.DuplicateSectionError:
				pass
			project_config.config.set('main', 'target', options[out[1]])

		self.main_menu()

	def target_config(self):
		if not self.get_target():
			snack.ButtonChoiceWindow(self.screen, 'Error', 'No target is selected.', ['Ok'])
			return self.main_menu()

		driver = self.get_target_driver()
		try:
			argspec = inspect.getargspec(driver.__new__)
		except TypeError:
			argspec = inspect.getargspec(driver.__init__)

		window = ui.ClsEntryWindow(
			self.screen,
			'{0} configuration'.format(driver.name),
			'See the options description at https://libcloud.readthedocs.org/en/latest/apidocs/libcloud.compute.drivers.html.\n\nWebsite: {0}'.format(driver.website),
			width=60
		)

		defaults = argspec[3][1:] if argspec[3] else []
		if len(defaults) + 1 < len(argspec[0]):
			defaults = [None] * (len(argspec[0])-1-len(defaults)) + list(defaults)
		for arg, default in zip(argspec[0][1:], defaults):
			default = self.format_default(default)
			window.add_input(arg, default)

		out = window.show()

		if out['button'] == 'ok':
			section = 'driver:{0}'.format(self.get_target())
			try:
				project_config.config.add_section(section)
			except ConfigParser.DuplicateSectionError:
				pass

			for key, value in out['input'].iteritems():
				project_config.config.set(section, key, value)

		self.main_menu()

	def get_target(self):
		try:
			target = project_config.config.get('main', 'target')
			return target
		except ConfigParser.NoSectionError:
			pass

	def get_target_driver(self):
		return get_driver(self.get_target())

	def get_available_drivers(self):
		def can_get(driver):
			try:
				return 'create_node' in get_driver(driver).features
			except:
				return False
			else:
				return True

		data = set([get_driver(x).type for x in vars(Provider).values() if can_get(x)])
		# filter none
		data = [x for x in data if x]
		return sorted(data)

	def format_default(self, data):
		if type(data) in (bool, int, float):
			return str(data)

		return data

config_cmd = Config()