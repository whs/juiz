from .base import Command
from .. import buildpack

def command(fn):
	def func(*args, **kwargs):
		buildpack.load_cfg()
		return fn(*args, **kwargs)

	return func

class Buildpack(Command):
	def build_args(self, parser):
		parser = parser.add_parser('buildpack', help='Manage buildpacks')
		subparser = parser.add_subparsers()

		dl = subparser.add_parser('download', help='Download new buildpack')
		dl.add_argument('name', help='Buildpack name')
		dl.add_argument('url', help='HTTP or git url of buildpack source')
		dl.set_defaults(func=self.download)

		ls = subparser.add_parser('ls', help='List installed buildpacks')
		ls.set_defaults(func=self.list)

		rm = subparser.add_parser('rm', help='Remove installed buildpacks')
		rm.add_argument('name', help='Buildpack name')
		rm.set_defaults(func=self.rm)

	@command
	def download(self, args):
		if args.name in buildpack.list():
			print 'Buildpack is already installed'
			exit(1)

		buildpack.download(args.name, args.url)
		buildpack.save_cfg()
		print 'Buildpack {0} installed'.format(args.name)

	@command
	def list(self, args):
		ls = buildpack.list()
		print 'total {0}'.format(len(ls))

		for name, pack in ls.iteritems():
			print '{0}\t\t{1}'.format(pack['name'], pack['source'])

	@command
	def rm(self, args):
		if args.name not in buildpack.list():
			print 'Buildpack is not installed'
			exit(1)

		buildpack.remove(args.name)
		buildpack.save_cfg()

buildpack_cmd = Buildpack()