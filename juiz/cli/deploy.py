from .. import bootstrap
from .. import deploy
from .base import Command

def command(fn):
	def func(*args, **kwargs):
		bootstrap()
		return fn(*args, **kwargs)

	return func

class Deploy(Command):
	def build_args(self, parser):
		parser = parser.add_parser('deploy', help='Run deployment')
		parser.set_defaults(func=self.deploy)

	@command
	def deploy(self, args):
		try:
			deploy.Deploy().deploy()
		except deploy.ConfigError, e:
			# TODO: Write to stderr
			print 'Deployment failed: {0}.\nDid you run juiz config?'.format(e.args[0])
			exit(1)
		except deploy.NoBuildpackError, e:
			print 'Deployment failed: Unsupported project or buildpack is not installed'
			exit(1)


deploy_cmd = Deploy()