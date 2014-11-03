import os
import unittest
import shutil
import json

from juiz import buildpack
from juiz import download

class TestBuildpack(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		try:
			os.mkdir(os.path.expanduser('~/.juiz'))
		except OSError:
			pass

		shutil.rmtree(os.path.expanduser('~/.juiz/buildpack/python_test'), True)
		buildpack.load_cfg()

	def test_download(self):
		self.assertTrue(buildpack.download('python_test', 'git@github.com:heroku/heroku-buildpack-python.git'))
		self.assertTrue(os.path.isfile(os.path.expanduser('~/.juiz/buildpack/python_test/bin/detect')))

		data = json.load(open(os.path.expanduser('~/.juiz/buildpack.json'), 'r'))
		self.assertIn('python_test', data['buildpack'])
		self.assertEqual(data['buildpack']['python_test']['name'], 'python_test')
		self.assertEqual(data['buildpack']['python_test']['source'], 'git@github.com:heroku/heroku-buildpack-python.git')

	def test_download_fail(self):
		self.assertRaises(download.DownloadException, buildpack.download, 'errortest', 'git@github.com:asdfsadfsdaf.git')

	def test_list(self):
		data = buildpack.list()
		self.assertIn('python_test', data)
		self.assertEqual(data['python_test']['name'], 'python_test')
		self.assertEqual(data['python_test']['source'], 'git@github.com:heroku/heroku-buildpack-python.git')

	def test_remove(self):
		buildpack.remove('python_test')
		self.assertNotIn('python_test', buildpack.list())