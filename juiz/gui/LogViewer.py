import subprocess
import os
import fcntl
import json
from datetime import datetime

from iowait import IOWait
import wx
from wx.lib.agw import ultimatelistctrl as ulc

from juiz.ui.LogViewer import LogViewer as LV
from .GetIPDialog import GetIPDialog

class LogViewer(LV):
	connection = None
	poller = None
	connected = False
	timer = None

	log_data = []
	identifiers = []

	command = 'journalctl -n 10000000 -b -f -o json'
	draw_freq = 50

	_draw_queue = []
	ids = {
		'search': 1000,
		'logname': 1001,
		'loglevel': 1002
	}

	filter = {
		'name': None,
		'level': None,
		'search': None
	}

	def __init__(self, project, machine, *args, **kwargs):
		super(LogViewer, self).__init__(*args, **kwargs)

		self.project = project
		self.machine = machine

		self.Bind(wx.EVT_CLOSE, self.close)
		self.Bind(wx.EVT_SHOW, self.on_show)

		self.logname.Append(_('Name'))
		self.loglevel.Append(_('Log level'))
		# not a class variable for gettext usage
		self.loglevel.Append(_('Emergency'), 0)
		self.loglevel.Append(_('Alert'), 1)
		self.loglevel.Append(_('Critical'), 2)
		self.loglevel.Append(_('Error'), 3)
		self.loglevel.Append(_('Warning'), 4)
		self.loglevel.Append(_('Notice'), 5)
		self.loglevel.Append(_('Info'), 6)
		self.loglevel.Append(_('Debug'), 7)

		self.SetTitle(_('{0} - Log viewer').format(self.machine.name))
		self.statusbar.SetFields([_('Connecting...')])

		self.Bind(wx.EVT_CHOICE, self.on_log_name_change, id=self.ids['logname'])

		self.build_list()

	def build_list(self):
		self.log.InsertColumn(0, _('Time'))
		self.log.InsertColumn(1, _('Name'))
		self.log.InsertColumn(2, _('Message'))

		self.log.SetColumnWidth(0, 150)
		self.log.SetColumnWidth(1, 100)
		self.log.SetColumnWidth(2, 300)

	def on_show(self, evt):
		if evt.GetShow():
			dialog = GetIPDialog(self.project, self.machine)
			if not dialog.ShowModal() or dialog.ip == None:
				wx.MessageDialog(self.GetParent(), _('IP of {} cannot be determined').format(self.machine.name), _('Cannot get IP'), wx.OK | wx.CENTER | wx.ICON_EXCLAMATION).ShowWindowModal()
				self.Close()
				self.Destroy()
				return
			self.ip = dialog.ip
			self.connect()
		evt.Skip()

	def on_log_name_change(self, evt):
		name = self.logname.GetStringSelection()
		self.filter['name'] = name

		self.update_filter()

	def update_filter(self):
		self.log.Freeze()
		for index, item in enumerate(self.log_data):
			if not self.is_filtered(item):
				print 'be gone'
			else:
				print 'be ok'
		self.log.Thaw()

	def close(self, evt=None):
		if self.poller:
			self.poller.clear()
		if self.connection:
			self.connection.terminate()
		if self.timer:
			self.timer.Stop()

		self.Destroy()
		
		if evt:
			evt.Skip()

	def connect(self):
		self.statusbar.SetFields([_('Connecting to {}...').format(self.ip)])
		self.connection = subprocess.Popen([
			'/usr/bin/ssh',
			'-C',
			'-i',
			os.path.expanduser(self.project.config.get('main', 'ssh_key')),
			'root@{}'.format(self.ip),
			self.command
		], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

		self.poller = IOWait()
		self.poller.watch(self.connection.stdout, read=True)
		self.poller.watch(self.connection.stderr, read=True)

		self.Bind(wx.EVT_IDLE, self.loop)
		self.Bind(wx.EVT_TIMER, self.draw_loop)

		self.timer = wx.Timer(self)
		self.timer.Start(self.draw_freq)

	def loop(self, evt):
		streams = self.poller.wait(0.01)

		for stream in streams:
			if stream.fileobj == self.connection.stderr:
				wx.MessageBox(self.connection.stderr.read(), _('Error'), wx.OK | wx.CENTER | wx.ICON_EXCLAMATION)
				self.close()
				return
			elif stream.fileobj == self.connection.stdout:
				if not self.connected:
					self.statusbar.SetFields([_('Connected to {}...').format(self.ip)])
					self.connected = True
				self.put_log(self.connection.stdout.readline())

		evt.RequestMore()

	def draw_loop(self, evt):
		if len(self._draw_queue) == 0:
			return

		self.log.Freeze()
		for item in self._draw_queue:
			self.log.Append(item)
		self._draw_queue = []
		self.log.Thaw()

		self.statusbar.SetFields([_('Connected to {}...').format(self.ip), str(len(self.log_data))])

	def put_log(self, log):
		try:
			log = json.loads(log)
		except ValueError:
			self.statusbar.SetFields([_('Cannot parse log line')])
			print log
			print '============='
			return

		self.log_data.append(log)

		identifier = log.get('SYSLOG_IDENTIFIER', None)
		log_name = log.get('SYSLOG_IDENTIFIER', None)

		if identifier:
			identifier += '['+log.get('_PID', '-1')+']'
		else:
			identifier = log.get('_PID', -1)

		if log_name and log_name not in self.identifiers:
			self.logname.Append(log_name)
			self.identifiers.append(log_name)

		self._draw_queue.append([
			self.format_date(log['__REALTIME_TIMESTAMP']),
			identifier,
			log.get('MESSAGE', _('No message'))
		])

	def is_filtered(self, log):
		level = int(log.get('PRIORITY', 6))
		name = log.get('SYSLOG_IDENTIFIER', None)
		message = log.get('MESSAGE', _('No message'))

		return (
			(self.filter['level'] == None or level <= self.filter['level']) and
			(self.filter['name'] == None or name == self.filter['name']) and
			(self.filter['search'] == None or message == self.filter['search'])
		)

	def format_date(self, date):
		return str(datetime.fromtimestamp(float(date)/1E6))
