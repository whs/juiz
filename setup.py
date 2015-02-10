#!/usr/bin/env python2

from setuptools import setup, find_packages
setup(
	name = 'juiz',
	version = '1.0',
	packages = find_packages(),
	setup_requires = ['setuptools-git'],
	zip_safe = False,
	entry_points={
		'console_scripts': [
			'juiz = juiz.cli:run'
		]
	},
	install_requires = [
		'requests',
		'apache-libcloud',
		'wxPython',
		'urllib3',
		'ansible',
		'iowait'
	],
	data_files=[
		('share/applications', ['data/Juiz.desktop'])
	],

	author = 'Manatsawin Hanmongkolchai',
	author_email = 'manatsawin@gmail.com',
	description = 'Desktop PaaS',
	license = 'Apache License 2.0',
	keywords = 'paas cloud',
	url = 'https://github.com/whs/juiz',
	include_package_data = True
)