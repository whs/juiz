from libcloud.compute.types import Provider

from juiz.gui.wizard.page.BaseWizardPage import WizardInputListPage
from juiz.gui.wizard.page.CloudConfigPage import CloudConfigPage

class AWSCloudConfigWizardPage(WizardInputListPage):
	fields = ['Access Key', 'Access Secret', 'Endpoint', 'Region']
	help_text = 'Use IAM to create access key and secret.'
	hyperlink = {
		'Access IAM': 'https://console.aws.amazon.com/iam/home#users'
	}
	config_section = 'target:{0}'.format(Provider.EC2)

	def __init__(self, *args, **kwargs):
		super(AWSCloudConfigWizardPage, self).__init__(*args, **kwargs)
		self.set_next(AWSCloudConfigPage(*args, **kwargs))

	def get_widget_value(self, field, widget):
		value = super(AWSCloudConfigWizardPage, self).get_widget_value(field, widget)
		if field == 'endpoint' and value == 'auto':
			return None
		return value

	def format_field_name(self, name):
		if name == 'Access Key':
			return 'key'
		elif name == 'Access Secret':
			return 'secret'
		elif name == 'Endpoint':
			return 'host'

		return super(AWSCloudConfigWizardPage, self).format_field_name(name)

	def get_region_choices(self):
		# libcloud does not provide api to list regions
		return {
			'us-east-1': 'US East (Northern Virginia)',
			'us-west-1': 'US West (Northern California)',
			'us-west-2': 'US West (Oregon)',
			'eu-west-1': 'EU (Ireland)',
			'ap-southeast-1': 'Asia Pacific (Singapore)',
			'ap-northeast-1': 'Asia Pacific (Tokyo)',
			'sa-east-1': 'South America (Sao Paolo)',
			'ap-southeast-2': 'Asia Pacific (Sydney)',
		}

	def get_region_type(self):
		return 'choice'

	def get_region(self):
		return 'us-east-1'

	def get_host(self):
		return 'auto'

class AWSCloudConfigPage(CloudConfigPage):
	fields = ['Size']
	provider = Provider.EC2
	help_text = 'T2 instance (micro, small and burstable) are not supported'
	config_section = 'target:{0}'.format(Provider.EC2)
