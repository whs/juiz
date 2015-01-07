import sys
import subprocess
import threading
import fcntl
import pty
import os
import re

from iowait import IOWait
import wx

from ..ui.LogWindow import LogWindow
from .event import SimpleEvent
from juiz import buildpack

class Download(LogWindow):
	def __init__(self, download, *args, **kwargs):
		super(Download, self).__init__(style=wx.SYSTEM_MENU | wx.RESIZE_BORDER, *args, **kwargs)
		self.download = download
		self._had_clear_end = False
		self.Center()

		# disable closing
		self.allow_close(False)
		self.Bind(wx.EVT_BUTTON, self.close, id=wx.ID_CLOSE)
		self.Connect(-1, -1, OutputEvent.event_type, self.on_log)
		self.Connect(-1, -1, EndEvent.event_type, self.on_end)

		self.progressbar.SetRange(0)
		self.progressbar.Pulse()

	def run(self):
		self.initial_count = len(self.download)
		self.progressbar.SetRange(100 * self.initial_count)
		self._download_one()

	def _download_one(self):
		name, url = self.download.pop(0)
		DownloadThread(name, url, self).start()

	def on_log(self, evt):
		if evt.stream == 'stderr':
			self.log.SetDefaultStyle(wx.TextAttr(wx.RED))
		else:
			self.log.SetDefaultStyle(wx.TextAttr())

		old_value = self.log.GetValue()
		if self._had_clear_end:
			old_value = old_value[:old_value.rfind('\n')+1]

		# handle terminal control codes
		evt.value = evt.value.replace('\x1b[K', '').replace('\r\n', '\n')
		if evt.value.endswith('\r'):
			self._had_clear_end = True
			evt.value = evt.value[:-1]
		else:
			self._had_clear_end = False

		evt.value = re.sub('[^\n\r]*\r', '', evt.value)

		percent = re.findall('[0-9]+%', evt.value)
		if len(percent) > 0:
			percent = min(100, int(percent[-1][:-1]))
			my_percent = (self.initial_count - len(self.download) - 1) * 100
			self.progressbar.SetValue(my_percent + percent)

		self.log.ChangeValue(old_value + evt.value)
		self.log.AppendText('')

	def on_end(self, evt):
		self.progressbar.SetValue((self.initial_count - len(self.download)) * 100)
		if len(self.download) > 0:
			self._download_one()
		else:
			self.allow_close(True)

	def allow_close(self, allow):
		self.close_btn.Enable(allow)
		if allow:
			self.SetEscapeId(wx.ID_ANY)
		else:
			self.SetEscapeId(wx.ID_NONE)

	def close(self, evt):
		buildpack.load_cfg()
		self.EndModal(True)
		self.Destroy()

class DownloadThread(threading.Thread):
	def __init__(self, name, url, wnd):
		super(DownloadThread, self).__init__()
		self.name = name
		self.url = url
		self.wnd = wnd

	def run(self):
		self.pty_out_master, self.pty_out_slave = pty.openpty()
		self.pty_err_master, self.pty_err_slave = pty.openpty()

		self.proc = subprocess.Popen([sys.executable, sys.argv[0], 'buildpack', 'download', self.name, self.url], stdout=self.pty_out_slave, stderr=self.pty_err_slave)

		self.poller = IOWait()
		self.poller.watch(self.pty_out_master, read=True)
		self.poller.watch(self.pty_err_master, read=True)

		self.unblock(self.pty_out_master)
		self.unblock(self.pty_err_master)

		while self.proc.returncode == None:
			streams = self.poller.wait(1)

			for item in streams:
				txt = os.read(item.fileobj, 1000)
				if item.fileobj == self.pty_out_master:
					wx.PostEvent(self.wnd, OutputEvent(txt, 'stdout'))
				elif item.fileobj == self.pty_err_master:
					wx.PostEvent(self.wnd, OutputEvent(txt, 'stderr'))

			self.proc.poll()

		os.close(self.pty_out_master)
		os.close(self.pty_err_master)

		wx.PostEvent(self.wnd, EndEvent())

	def unblock(self, fp):
		flags = fcntl.fcntl(fp, fcntl.F_GETFL)
		fcntl.fcntl(fp, fcntl.F_SETFL, flags | os.O_NONBLOCK)

class OutputEvent(SimpleEvent):
	event_type = wx.NewId()
	value = None
	stream = None

	def __init__(self, value, stream='stdout'):
		super(OutputEvent, self).__init__()
		self.value = value
		self.stream = stream

class EndEvent(SimpleEvent):
	event_type = wx.NewId()