from libcloud.compute.types import Provider

from .BaseWizardPage import WizardInputListPage
from .CloudConfigPage import CloudConfigPage

class AWSCloudConfigWizardPage(WizardInputListPage):
	fields = ['Access Key', 'Access Secret', 'Endpoint', 'Region']
	help_text = 'Use IAM to create access key and secret.'
	hyperlink = {
		'Access IAM': 'https://console.aws.amazon.com/iam/home#users'
	}

	def __init__(self, *args, **kwargs):
		super(AWSCloudConfigWizardPage, self).__init__(*args, **kwargs)
		self.set_next(AWSCloudConfigPage(*args, **kwargs))

	def dump_config(self, config):
		section = 'target:{0}'.format(Provider.EC2)
		config.add_section(section)
		
		for k, v in self.get_settings().iteritems():
			if k == 'endpoint' and v == 'auto':
				continue
			config.set(section, k, v)

	def get_settings(self):
		data = self.get_values_dict()
		if data['endpoint'] == 'auto':
			data['endpoint'] = None

		return {
			'key': data['access_key'],
			'secret': data['access_secret'],
			'host': data['endpoint'],
			'region': data['region']
		}

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

	def get_endpoint(self):
		return 'auto'

class AWSCloudConfigPage(CloudConfigPage):
	fields = ['Size']
	provider = Provider.EC2
	help_text = 'T2 instance (micro, small and burstable) are not supported'