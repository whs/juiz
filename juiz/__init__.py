from . import buildpack
from . import cloudstack_patch

def bootstrap():
	buildpack.load_cfg()
