import wx

from .page.CloudWizard import CloudPickProviderWizardPage

class CloudWizard(wx.wizard.Wizard):
	def __init__(self, project, parent=None):
		super(CloudWizard, self).__init__(parent, wx.ID_ANY, _('Cloud configuration'))
		self.project = project
		self.SetPageSize((500, 400))

	def run(self):
		page1 = CloudPickProviderWizardPage(self)
		success = self.RunWizard(page1)
		if success:
			self.build_config(page1)
		return success

	def build_config(self, page):
		while page:
			page.dump_config(self.project.config)
			page = page.GetNext()

	def show_error(self, message):
		wx.MessageDialog(self.GetParent(), message, _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()