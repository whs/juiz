from libcloud.compute.drivers.cloudstack import CloudStackNodeDriver, CloudStackAddress
from libcloud.compute.providers import DRIVERS
from libcloud.compute.types import Provider

class CSPatch(CloudStackNodeDriver):
	# supported in list_nodes only now
	project = None

	# as cloudstack driver does not support list_public_ips
	# with project, this tries to monkey patch it in
	def ex_list_public_ips(self, project=None):
		ips = []

		res = self._sync_request(command='listPublicIpAddresses',
								params={'project': project},
								method='GET')

		# Workaround for basic zones
		if not res:
			return ips

		for ip in res['publicipaddress']:
			ips.append(CloudStackAddress(ip['id'],
										 ip['ipaddress'],
										 self,
										 ip.get('associatednetworkid', None),
										 ip.get('vpcid', None)))

		return ips

	def ex_allocate_public_ip(self, vpc_id=None, network_id=None,
							  location=None, project_id=None):
		args = {}

		if location is not None:
			args['zoneid'] = location.id
		else:
			args['zoneid'] = self.list_locations()[0].id

		if vpc_id is not None:
			args['vpcid'] = vpc_id

		if network_id is not None:
			args['networkid'] = network_id

		if project_id is not None:
			args['projectid'] = project_id

		addr = self._async_request(command='associateIpAddress',
								   params=args,
								   method='GET')
		addr = addr['ipaddress']
		addr = CloudStackAddress(addr['id'], addr['ipaddress'], self)
		return addr

	def ex_enable_static_nat(self, node, ip, network=None):
		if network:
			network = network.id
		return self._sync_request(command='enableStaticNat',
								params={'ipaddressid': ip.id, 'virtualmachineid': node.id, 'networkid': network},
								method='GET')

	def list_nodes(self, project=-1):
		if project == -1:
			project = self.project
		return super(CSPatch, self).list_nodes(project)

DRIVERS[Provider.CLOUDSTACK] = (__name__, 'CSPatch')