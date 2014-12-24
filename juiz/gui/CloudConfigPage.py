import threading

import wx

from libcloud.compute.providers import get_driver

from .BaseWizardPage import WizardInputListPage
from .event import SimpleEvent, ValueEvent

class CloudConfigPage(WizardInputListPage):
	fields = ['Location', 'Size', 'Image']
	progress_count = 4
	provider = None

	def __init__(self, *args, **kwargs):
		super(CloudConfigPage, self).__init__(*args, **kwargs)
		if not self.provider:
			raise RuntimeError, 'Provider is not set'
		self.Connect(-1, -1, ProgressEvent.event_type, self.on_progress)
		self.Connect(-1, -1, MetadataLoadedEvent.event_type, self.on_loaded)
		self.Connect(-1, -1, LocationLoadedEvent.event_type, self.on_location_loaded)
		self.Connect(-1, -1, FetchErrorEvent.event_type, self.on_error)
		if 'Location' in self.fields:
			self.Bind(wx.EVT_CHOICE, self.on_change_location, self.get_widget('Location'))

	def on_show(self, event):
		if event.GetPage() == self:
			self.progress = wx.ProgressDialog('Loading', 'Loading data', self.progress_count, parent=self)
			self.progress.Pulse('Connecting')
			threading.Thread(target=self.fetch).start()
			self.progress.ShowModal()
		event.Skip()

	def on_progress(self, event):
		self.progress.Update(*event.value)

	def on_loaded(self, event):
		if self.progress:
			self.progress.EndModal(1)

		self.update_lists()

	def on_location_loaded(self, event):
		if self.progress:
			self.progress.EndModal(1)

		self.update_size()
		self.update_image()
		self.check_allow_forward()

	def on_error(self, event):
		if self.progress:
			self.progress.EndModal(0)

		wx.MessageDialog(self.GetParent(), 'Unable to fetch metadata:\n' + str(event.value), 'Error', wx.OK | wx.ICON_ERROR).ShowModal()
		self.GetParent().ShowPage(self.GetPrev(), False)

	def on_change_location(self, event):
		self.progress = wx.ProgressDialog('Loading', 'Loading location data', self.progress_count - 1, parent=self)
		self.progress.Pulse('Connecting')
		threading.Thread(target=self.fetch_location).start()
		self.progress.ShowModal()

	def fetch(self):
		try:
			Driver = get_driver(self.provider)
			self.driver = Driver(**self.get_settings())

			if 'Location' in self.fields:
				wx.PostEvent(self, ProgressEvent([1, 'Fetching location list']))
				self.locations = self.driver.list_locations()

			if 'Image' in self.fields:
				wx.PostEvent(self, ProgressEvent([2, 'Fetching images list']))
				self.images = self.driver.list_images()

			if 'Size' in self.fields:
				wx.PostEvent(self, ProgressEvent([3, 'Fetching machine sizes']))
				self.sizes = self.driver.list_sizes()

			self.fetch_post()
			wx.PostEvent(self, MetadataLoadedEvent())
		except Exception, e:
			print `e`
			wx.PostEvent(self, FetchErrorEvent(e))

	def fetch_post(self):
		wx.PostEvent(self, ProgressEvent([4, 'Done']))

	def fetch_location(self):
		location_id = self.get_values_dict()['location']
		location = [x for x in self.locations if x.id == location_id][0]
		try:
			if 'Image' in self.fields:
				try:
					wx.PostEvent(self, ProgressEvent([1, 'Fetching images list']))
					self.images = self.driver.list_images(location)
				except TypeError:
					pass

			if 'Size' in self.fields:
				try:
					wx.PostEvent(self, ProgressEvent([2, 'Fetching machine sizes']))
					self.sizes = self.driver.list_sizes(location)
				except TypeError:
					pass

			wx.PostEvent(self, ProgressEvent([3, 'Done']))
			wx.PostEvent(self, LocationLoadedEvent())
		except Exception, e:
			print `e`
			wx.PostEvent(self, FetchErrorEvent(e))

	def update_lists(self):
		self.update_locations()
		self.update_size()
		self.update_image()
		self.check_allow_forward()

	def update_locations(self):
		widget = self.get_widget('Location')
		if not widget:
			return

		widget.Clear()

		for item in self.locations:
			widget.Append(item.name, item.id)

	def update_size(self):
		widget = self.get_widget('Size')
		if not widget:
			return

		widget.Clear()

		for item in self.sizes:
			widget.Append('{0} ({1} MB RAM, {2} GB Disk, ${3:.2f}/hr)'.format(item.name, item.ram, item.disk, item.price), item.id)

	def update_image(self):
		widget = self.get_widget('Image')
		if not widget:
			return

		widget.Clear()

		for item in self.images:
			widget.Append(item.name, item.id)

	def update_project(self):
		widget = self.get_widget('Project')
		if not widget:
			return

		widget.Clear()
		widget.Append('', None)

		for item in self.projects:
			widget.Append(item.display_text, item.id)

	def get_location_type(self):
		return 'choice'

	def get_size_type(self):
		return 'choice'

	def get_image_type(self):
		return 'choice'

	def get_location_choices(self):
		return {}

	def get_size_choices(self):
		return {}

	def get_image_choices(self):
		return {}

	def get_settings(self):
		return self.prev.get_settings()

	def dump_config(self, config):
		for k, v in self.get_values_dict().iteritems():
			config.set('target:{0}'.format(self.provider), k, v)

	def get_widget_value(self, field, widget):
		if isinstance(widget, wx.Choice):
			return widget.GetClientData(widget.GetSelection())
		return super(CloudConfigPage, self).get_widget_value(field, widget)

class ProgressEvent(ValueEvent):
	event_type = wx.NewId()

class MetadataLoadedEvent(SimpleEvent):
	event_type = wx.NewId()

class FetchErrorEvent(ValueEvent):
	event_type = wx.NewId()

class LocationLoadedEvent(SimpleEvent):
	event_type = wx.NewId()