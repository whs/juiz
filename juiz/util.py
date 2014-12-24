import importlib
import hashlib
import random
import functools
import collections

def random_id():
	return hashlib.sha256(str(random.random())).hexdigest()[:6]

def import_by_name(name):
	module = '.'.join(name.split('.')[:-1])
	cls = name.split('.')[-1]
	return getattr(importlib.import_module(module), cls)

class memoized(object):
	'''Decorator. Caches a function's return value each time it is called.
	If called later with the same arguments, the cached value is returned
	(not reevaluated).
	'''
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		if not isinstance(args, collections.Hashable):
			# uncacheable. a list, for instance.
			# better to not cache than blow up.
			return self.func(*args)
		if args in self.cache:
			return self.cache[args]
		else:
			value = self.func(*args)
			self.cache[args] = value
			return value
	def __repr__(self):
		'''Return the function's docstring.'''
		return self.func.__doc__
	def __get__(self, obj, objtype):
		'''Support instance methods.'''
		return functools.partial(self.__call__, obj)