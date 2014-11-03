import subprocess
import tarfile
import zipfile

import requests
import urllib3.exceptions

GIT_BIN = '/usr/bin/git'

def sniff(url):
	if url.endswith('.git'):
		return GitDownload(url)

	try:
		header = requests.head(url, allow_redirects=True)
		if header.headers['content-type'] in ('application/x-gzip', 'application/zip'):
			return HttpDownload(header.url)
	except urllib3.exceptions.LocationParseError:
		pass

class Downloader(object):
	def __init__(self, url):
		self.url = url

	def get(self, target):
		raise NotImplementedError

	def extract(self):
		pass

class GitDownload(Downloader):
	git = GIT_BIN

	def get(self, target):
		try:
			subprocess.check_call([self.git, 'clone', self.url, target])
		except subprocess.CalledProcessError:
			raise DownloadException("Git returned error")

class HttpDownload(Downloader):
	content_map = {
		'application/x-gzip': '.tar.gz',
		'application/zip': '.zip'
	}

	def get(self, target):
		self.target = target
		resp = requests.get(self.url, stream=True)

		self.extension = self.content_map[resp.headers['content-type']]
		fp = open(self.target + self.extension, 'wb')

		for block in resp.iter_content(1024):
			if not block:
				break
			fp.write(block)

	def extract(self):
		if self.extension == '.tar.gz':
			fp = tarfile.open(self.target + self.extension)
			names = fp.getnames()

			root = self.get_zip_root(names)

			def rewrite_tarinfo(info):
				# also strip the / after root name
				info.name = info.name[len(root) + 1:]
				if info.name:
					return info

			members = [x for x in [rewrite_tarinfo(info) for info in fp.getmembers()] if x]
		else:
			fp = zipfile.ZipFile(self.target + self.extension, 'r')
			names = fp.namelist()

			root = self.get_zip_root(names)

			def rewrite_zipinfo(info):
				# zip archive return trailing slash for root already
				info.filename = info.filename[len(root):]
				if info.filename:
					return info

			members = [x for x in [rewrite_zipinfo(info) for info in fp.infolist()] if x]

		if not root:
			raise ExtractException('Cannot find zip root, or there is no root directory')

		fp.extractall(self.target, members)

	def get_zip_root(self, names):
		prefix = names[0]
		for name in names:
			if not name.startswith(prefix):
				return

		return prefix

class DownloadException(Exception):
	pass

class ExtractException(Exception):
	pass