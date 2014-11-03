from libcloud.compute.types import Provider

from .BaseWizardPage import WizardInputListPage

class AWSCloudConfigWizardPage(WizardInputListPage):
	fields = ['Access Key', 'Access Secret', 'Endpoint', 'Region']
	help_text = 'Use IAM to create access key and secret.'
	hyperlink = {
		'Access IAM': 'https://console.aws.amazon.com/iam/home#users'
	}

	def dump_config(self, config):
		section = 'target:{0}'.format(Provider.EC2)
		config.add_section(section)
		
		order = ['key', 'secret', 'endpoint', 'region']
		for k, v in zip(order, self.get_values()):
			if k == 'endpoint' and v == 'auto':
				continue
			config.set(section, k, v)


	def get_region(self):
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
			'us-gov-west-1': 'AWS GovCloud (US)'
		}

	def get_endpoint(self):
		return 'auto'