import logging

import wx

from .event import ValueEvent
from ..ui.LogWindow import LogWindow
from ..deploy import DeployThread, LOG_PROGRESS, LOG_PROGRESS_TOTAL
from ..provider.base import ConfigError

class Deploy(LogWindow):
	project = None

	def __init__(self, project, *args, **kwargs):
		self.project = project
		super(Deploy, self).__init__(style=wx.SYSTEM_MENU | wx.RESIZE_BORDER, *args, **kwargs)
		self.Center()

		# disable closing
		self.SetEscapeId(wx.ID_NONE)
		self.Bind(wx.EVT_BUTTON, self.close, id=wx.ID_CLOSE)
		self.Bind(wx.EVT_CLOSE, self.cleanup)
		self.progressbar.SetRange(0)
		self.progressbar.Pulse()

		self.Connect(-1, -1, LogEvent.event_type, self.on_log)

		self.deploy()

	def deploy(self):
		self.logger = logging.getLogger('deploy')
		self.logger.setLevel(LOG_PROGRESS_TOTAL)
		self.handler = DeployLogToWindow(self)
		self.logger.addHandler(self.handler)
		def remove_handler():
			self.logger.removeHandler(self.handler)
			self.allow_close(True)
		DeployLogError(remove_handler, self.project).start()

	def allow_close(self, allow):
		self.close_btn.Enable(allow)
		if allow:
			self.SetEscapeId(wx.ID_ANY)
		else:
			self.SetEscapeId(wx.ID_NONE)

	def close(self, evt):
		self.Close()
		self.EndModal(True)

	def cleanup(self, evt):
		self.logger.removeHandler(self.handler)

	def on_log(self, evt):
		record = evt.value

		if record.levelno == LOG_PROGRESS:
			self.progressbar.SetValue(self.progressbar.GetValue() + int(record.msg))
			return
		elif record.levelno == LOG_PROGRESS_TOTAL:
			self.progressbar.SetRange(self.progressbar.GetRange() + int(record.msg))
			return

		if record.levelno in (logging.ERROR, logging.CRITICAL):
			self.log.SetDefaultStyle(wx.TextAttr(wx.RED))
		elif record.levelno == logging.WARNING:
			self.log.SetDefaultStyle(wx.TextAttr(wx.Colour(239, 204, 0)))
		elif record.levelno == logging.DEBUG:
			self.log.SetDefaultStyle(wx.TextAttr(wx.Colour(150, 150, 150)))
		else:
			self.log.SetDefaultStyle(wx.TextAttr())
		self.log.AppendText(record.preformat + '\n')

class DeployLogError(DeployThread):
	def __init__(self, cb=lambda: True, *args, **kwargs):
		super(DeployLogError, self).__init__(*args, **kwargs)
		self.cb = cb
	def run(self):
		try:
			super(DeployLogError, self).run()
		except ConfigError, e:
			logging.getLogger('deploy').error('Configuration error: %s', e.args[0])
		except Exception, e:
			logging.getLogger('deploy').exception('An error occurred during deployment', exc_info=True)
		self.cb()

class DeployLogToWindow(logging.Handler):
	wnd = None
	def __init__(self, wnd, *args, **kwargs):
		super(DeployLogToWindow, self).__init__(*args, **kwargs)
		self.wnd = wnd

	def emit(self, record):
		record.preformat = self.format(record)
		wx.PostEvent(self.wnd, LogEvent(record))

class LogEvent(ValueEvent):
	event_type = wx.NewId()