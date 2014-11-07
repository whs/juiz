import os
import argparse

from ..config import config
from .registry import registry

class Main(object):
	description = 'PaaS-like deployment tool'

	def __init__(self):
		self.args = argparse.ArgumentParser(description=self.description)
		self.build_args()

	def build_args(self):
		subparsers = self.args.add_subparsers()
		for cmd in registry:
			cmd.build_args(subparsers)

	def run(self):
		parsed = self.args.parse_args()

		try:
			os.mkdir(config.get('main', 'path'))
		except OSError:
			pass
		
		parsed.func(parsed)