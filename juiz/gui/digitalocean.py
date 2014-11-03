from .BaseWizardPage import WizardInputListPage

class DOCloudConfigWizardPage(WizardInputListPage):
	fields = ['Client ID', 'API Key']
	help_text = 'Only v1 API key is supported'
	hyperlink = {
		'API Key Management': 'https://cloud.digitalocean.com/api_access'
	}