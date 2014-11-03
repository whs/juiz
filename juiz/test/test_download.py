import os
import shutil
import unittest

from juiz import download

class TestDownload(unittest.TestCase):
	def test_sniff_git(self):
		self.assertIsInstance(
			download.sniff('git@github.com:heroku/heroku-buildpack-python.git'),
			download.GitDownload
		)

	def test_sniff_zip(self):
		self.assertIsInstance(
			download.sniff('https://github.com/heroku/heroku-buildpack-python/archive/v52.zip'),
			download.HttpDownload
		)

	def test_sniff_targz(self):
		self.assertIsInstance(
			download.sniff('https://github.com/heroku/heroku-buildpack-python/archive/v52.tar.gz'),
			download.HttpDownload
		)

	def test_sniff_404(self):
		self.assertEqual(
			download.sniff('http://httpbin.org/404'),
			None
		)

	def test_git_dl(self):
		dl = download.GitDownload('git@gist.github.com:/1.git')
		dl.get('/tmp/test_git')
		dl.extract()
		self.assertTrue(os.path.isfile('/tmp/test_git/gistfile1.txt'))
		shutil.rmtree('/tmp/test_git')

	def test_git_error(self):
		dl = download.GitDownload('git@gist.github.com:/xzncvlkjasdnfkjalfkj.git')
		self.assertRaises(download.DownloadException, dl.get, '/tmp/test_git')

	def test_http_dl_targz(self):
		dl = download.HttpDownload('https://gist.github.com/schacon/1/download')
		dl.get('/tmp/test_http')
		self.assertTrue(os.path.isfile('/tmp/test_http.tar.gz'))
		dl.extract()
		self.assertTrue(os.path.isfile('/tmp/test_http/gistfile1.txt'))
		shutil.rmtree('/tmp/test_http')
		os.unlink('/tmp/test_http.tar.gz')

	def test_http_dl_zip(self):
		dl = download.HttpDownload('https://github.com/ValveSoftware/portal2/archive/master.zip')
		dl.get('/tmp/test_http')
		self.assertTrue(os.path.isfile('/tmp/test_http.zip'))
		dl.extract()
		self.assertTrue(os.path.isfile('/tmp/test_http/README.md'))
		shutil.rmtree('/tmp/test_http')
		os.unlink('/tmp/test_http.zip')