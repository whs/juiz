import threading
import wx

from libcloud.compute.types import Provider

from juiz.gui.wizard.page.BaseWizardPage import WizardInputListPage
from juiz.gui.wizard.page.CloudConfigPage import CloudConfigPage, ProgressEvent, FetchErrorEvent
from ..event import SimpleEvent

class CloudStackCloudConfigWizardPage(WizardInputListPage):
	fields = ['API Key', 'API Secret', 'URL']
	help_text = 'To access your API keys, go to Accounts>Your username>View users>Your username. You might need to generate keys if one doesn\'t already exists'
	config_section = 'target:{0}'.format(Provider.CLOUDSTACK)

	def __init__(self, *args, **kwargs):
		super(CloudStackCloudConfigWizardPage, self).__init__(*args, **kwargs)
		self.set_next(CloudStackZoneConfigWizardPage(*args, **kwargs))

	def format_field_name(self, name):
		if name == 'API Key':
			return 'key'
		elif name == 'API Secret':
			return 'secret'
		return super(CloudStackCloudConfigWizardPage, self).format_field_name(name)
	
	def get_url(self):
		return 'http://localhost/client/api'

	def get_settings(self):
		settings = self.get_values_dict()
		settings['secure'] = False
		return settings

class CloudStackZoneConfigWizardPage(CloudConfigPage):
	fields = ['Location', 'Size', 'Image', 'Project', 'Network']
	nullable_field = ['Project']
	help_text = 'Please select Ubuntu 14.04 LTS image from the server.'
	progress_count = 6
	provider = Provider.CLOUDSTACK
	config_section = 'target:{0}'.format(Provider.CLOUDSTACK)

	def __init__(self, *args, **kwargs):
		super(CloudStackZoneConfigWizardPage, self).__init__(*args, **kwargs)
		self.Bind(wx.EVT_CHOICE, self.on_change_project, self.get_widget('Project'))

	def on_progress(self, event):
		super(CloudStackZoneConfigWizardPage, self).on_progress(event)

		if event.done and event.type == 'project':
			self.update_network()
			self.check_allow_forward()

	def on_change_project(self, event):
		self.progress = wx.ProgressDialog('Loading', 'Loading network list', 3, parent=self)
		self.progress.Pulse('Connecting to CloudStack')
		threading.Thread(target=self.fetch_networks).start()
		self.progress.ShowModal()

	def fetch_post(self):
		try:
			wx.PostEvent(self, ProgressEvent([4, 'Fetching project list']))
			self.projects = self.driver.ex_list_projects()

			wx.PostEvent(self, ProgressEvent([5, 'Fetching network list']))
			self.networks = self.driver.ex_list_networks()

			wx.PostEvent(self, ProgressEvent([6, 'Done'], done=True))
		except Exception, e:
			wx.PostEvent(self, FetchErrorEvent(e))

	def fetch_networks(self):
		try:
			wx.PostEvent(self, ProgressEvent([1, 'Fetching project list'], type='project'))
			project_id = self.get_values_dict()['project']
			project = None
			if project_id:
				project = [x for x in self.projects if x.id == project_id][0]

			wx.PostEvent(self, ProgressEvent([2, 'Fetching network associated with project'], type='project'))
			self.networks = self.driver.ex_list_networks(project)

			wx.PostEvent(self, ProgressEvent([3, 'Done'], done=True, type='project'))
		except Exception, e:
			wx.PostEvent(self, FetchErrorEvent(e))

	def update_lists(self):
		self.update_project()
		self.update_network()
		super(CloudStackZoneConfigWizardPage, self).update_lists()

	def update_project(self):
		widget = self.get_widget('Project')
		if not widget:
			return

		widget.Clear()
		widget.Append('', None)

		default = self.get_default_value('Project')
		for item in self.projects:
			index = widget.Append(item.display_text, item.id)
			if default == item.id:
				widget.SetSelection(index)

	def update_network(self):
		widget = self.get_widget('Network')
		widget.Clear()

		default = self.get_default_value('Network')
		for item in self.networks:
			index = widget.Append(item.displaytext, item.id)
			if default == item.id:
				widget.SetSelection(index)

	def get_network_type(self):
		return 'choice'

	def get_project_type(self):
		return 'choice'

	def get_network_choices(self):
		return {}

	def get_project_choices(self):
		return {}