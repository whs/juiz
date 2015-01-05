from juiz.gui.wizard.page.BaseWizardPage import WizardInputListPage
from juiz.gui.wizard.page.CloudConfigPage import CloudConfigPage

from libcloud.compute.types import Provider

class DOCloudConfigWizardPage(WizardInputListPage):
	fields = ['Client ID', 'API Key']
	help_text = 'Only v1 API key is supported'
	hyperlink = {
		'API Key Management': 'https://cloud.digitalocean.com/api_access'
	}
	config_section = 'target:{0}'.format(Provider.DIGITAL_OCEAN)

	def __init__(self, *args, **kwargs):
		super(DOCloudConfigWizardPage, self).__init__(*args, **kwargs)
		self.set_next(DOCloudConfigPage(*args, **kwargs))

	def format_field_name(self, name):
		if name == 'Client ID':
			return 'key'
		elif name == 'API Key':
			return 'secret'
		return super(DOCloudConfigWizardPage, self).format_field_name(name)

class DOCloudConfigPage(CloudConfigPage):
	fields = ['Location', 'Size']
	provider = Provider.DIGITAL_OCEAN
	config_section = 'target:{0}'.format(Provider.DIGITAL_OCEAN)
