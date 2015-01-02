import threading
import wx

from libcloud.compute.types import Provider

from juiz.gui.wizard.page.BaseWizardPage import WizardInputListPage
from juiz.gui.wizard.page.CloudConfigPage import CloudConfigPage, ProgressEvent, FetchErrorEvent
from ..event import SimpleEvent

CONFIG_SECTION = 'target:{0}'.format(Provider.CLOUDSTACK)

class CloudStackCloudConfigWizardPage(WizardInputListPage):
	fields = ['API Key', 'API Secret', 'URL']
	help_text = 'To access your API keys, go to Accounts>Your username>View users>Your username. You might need to generate keys if one doesn\'t already exists'

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

	def dump_config(self, config):
		config.add_section(CONFIG_SECTION)

		for k, v in self.get_settings().iteritems():
			config.set(CONFIG_SECTION, k, v)

	def get_settings(self):
		settings = self.get_values_dict()
		settings['secure'] = False
		return settings

class CloudStackZoneConfigWizardPage(CloudConfigPage):
	fields = ['Location', 'Size', 'Image', 'Project', 'Network']
	nullable_field = ['Project']
	help_text = 'Juiz requires CentOS 7. Please select CentOS 7 image from the server.'
	progress_count = 6
	provider = Provider.CLOUDSTACK

	def __init__(self, *args, **kwargs):
		super(CloudStackZoneConfigWizardPage, self).__init__(*args, **kwargs)
		self.Connect(-1, -1, NetworkLoadedEvent.event_type, self.on_network_loaded)
		self.Bind(wx.EVT_CHOICE, self.on_change_project, self.get_widget('Project'))

	def on_network_loaded(self, event):
		if self.progress:
			self.progress.EndModal(1)

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

			wx.PostEvent(self, ProgressEvent([6, 'Done']))
		except Exception, e:
			wx.PostEvent(self, FetchErrorEvent(e))

	def fetch_networks(self):
		try:
			wx.PostEvent(self, ProgressEvent([1, 'Fetching project list']))
			project_id = self.get_values_dict()['project']
			project = None
			if project_id:
				project = [x for x in self.projects if x.id == project_id][0]

			wx.PostEvent(self, ProgressEvent([2, 'Fetching network associated with project']))
			self.networks = self.driver.ex_list_networks(project)

			wx.PostEvent(self, ProgressEvent([3, 'Done']))
			wx.PostEvent(self, NetworkLoadedEvent())
		except Exception, e:
			wx.PostEvent(self, FetchErrorEvent(e))

	def update_lists(self):
		self.update_project()
		self.update_network()
		super(CloudStackZoneConfigWizardPage, self).update_lists()

	def update_project(self):
		widget = self.get_widget('Project')
		widget.Clear()
		widget.Append('', None)

		for item in self.projects:
			widget.Append(item.display_text, item.id)

	def update_network(self):
		widget = self.get_widget('Network')
		widget.Clear()

		for item in self.networks:
			widget.Append(item.displaytext, item.id)

	def get_network_type(self):
		return 'choice'

	def get_project_type(self):
		return 'choice'

	def get_network_choices(self):
		return {}

	def get_project_choices(self):
		return {}

class NetworkLoadedEvent(SimpleEvent):
	event_type = wx.NewId()