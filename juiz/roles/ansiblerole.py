import os

from ansible.playbook import PlayBook
from ansible.callbacks import AggregateStats
from ansible import constants

from .role import Role

class AnsibleRole(Role):
	playbook = None

	def __init__(self, *args, **kwargs):
		super(AnsibleRole, self).__init__(*args, **kwargs)

	def run(self, project, log, inventory, env):
		self.project = project
		self.log = log
		self.inventory = inventory
		self.env = env

		self.ansible_stats = AggregateStats()
		self.ansible_cb = LogCallback(self.log)
		self.ansible_runner_cb = LogRunnerCallback(self.log)
		
		playbook = self.build_playbook()
		playbook.run()

		self.log.debug(
			'OK: %s Changed: %s Skipped: %s',
			self.format_stat(self.ansible_stats.ok),
			self.format_stat(self.ansible_stats.changed),
			self.format_stat(self.ansible_stats.skipped),
		)

		out = True

		if self.ansible_stats.dark != {}:
			self.log.error('Unreachable: %s', self.format_stat(self.ansible_stats.dark))
			out = False
		if self.ansible_stats.failures != {}:
			self.log.error('Failed: %s', self.format_stat(self.ansible_stats.failures))
			out = False

		return out

	def format_stat(self, stat):
		stat = stat.items()
		out = ', '.join([
			'{0}[{1}]'.format(*x)
			for x in stat
		])

		if not out:
			return '-'

		return out

	def build_playbook(self, **kwargs):
		return PlayBook(
			playbook=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'playbook', self.playbook),
			host_list=None,
			inventory=self.inventory,
			stats=self.ansible_stats,
			callbacks=self.ansible_cb,
			runner_callbacks=self.ansible_runner_cb,
			extra_vars=self.get_ansible_vars(),
			**kwargs
		)

	def get_ansible_vars(self):
		return {
			'project': self.project,
			'buildpack': self.project.buildpack,
			'runtime_dir': '/var/juiz/remote',
			'env': self.env
		}

	def get_ip_of_role(self, roles=None):
		if not roles:
			roles = self.name
		hosts = self.inventory.get_hosts(roles)
		return [x.vars['ansible_ssh_host'] for x in hosts]

class LogCallback(object):
	def __init__(self, log):
		self.log = log

	def on_start(self):
		pass

	def on_notify(self, host, handler):
		pass

	def on_no_hosts_matched(self):
		self.log.warn('No host matched for role')

	def on_no_hosts_remaining(self):
		self.log.error('All hosts have failed -- aborting.')

	def on_task_start(self, name, is_conditional):
		if is_conditional:
			self.log.debug('Handler: %s', name)
		else:
			self.log.debug('Task: %s', name)

	def on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
		return default

	def on_setup(self):
		self.log.debug('Gathering facts')

	def on_import_for_host(self, host, imported_file):
		msg = '%s: importing %s' % (host, imported_file)
		self.log.debug(msg)

	def on_not_import_for_host(self, host, missing_file):
		msg = '%s: not importing file: %s' % (host, missing_file)
		self.log.debug(msg)

	def on_play_start(self, name):
		self.log.info('Setting up role %s', name)

	def on_stats(self, stats):
		pass

class LogRunnerCallback(object):
	def __init__(self, log):
		self.log = log
		self._async_notified = {}

	def on_unreachable(self, host, results):
		if self.runner.delegate_to:
			host = '%s -> %s' % (host, self.runner.delegate_to)

		item = None
		if type(results) == dict:
			item = results.get('item', None)
		if item:
			msg = "fatal: [%s] => (item=%s) => %s" % (host, item, results)
		else:
			msg = "fatal: [%s] => %s" % (host, results)
		self.log.error(msg)

	def on_failed(self, host, results, ignore_errors=False):
		if self.runner.delegate_to:
			host = '%s -> %s' % (host, self.runner.delegate_to)

		results2 = results.copy()
		results2.pop('invocation', None)

		item = results2.get('item', None)
		parsed = results2.get('parsed', True)
		module_msg = ''
		if not parsed:
			module_msg  = results2.pop('msg', None)
		stderr = results2.pop('stderr', None)
		stdout = results2.pop('stdout', None)
		returned_msg = results2.pop('msg', None)

		if item:
			msg = "failed: [%s] => (item=%s) => %s" % (host, item, results2)
		else:
			msg = "failed: [%s] => %s" % (host, results2)
		self.log.error(msg)

		if stderr:
			self.log.error('stderr: %s', stderr)
		if stdout:
			self.log.error('stdout: %s', stdout)
		if returned_msg:
			self.log.error('msg: %s', returned_msg)
		if not parsed and module_msg:
			self.log.error(module_msg)
		if ignore_errors:
			self.log.debug('...ignoring')

	def on_ok(self, host, host_result):
		if self.runner.delegate_to:
			host = '%s -> %s' % (host, self.runner.delegate_to)

		item = host_result.get('item', None)

		host_result2 = host_result.copy()
		host_result2.pop('invocation', None)
		changed = host_result.get('changed', False)
		ok_or_changed = 'ok'
		if changed:
			ok_or_changed = 'changed'

		# show verbose output for non-setup module results if --verbose is used
		msg = ''
		if item:
			msg = "%s: [%s] => (item=%s)" % (ok_or_changed, host, item)
		else:
			if 'ansible_job_id' not in host_result or 'finished' in host_result:
				msg = "%s: [%s]" % (ok_or_changed, host)

		if msg != '':
			self.log.debug(msg)
		if constants.COMMAND_WARNINGS and 'warnings' in host_result2 and host_result2['warnings']:
			for warning in host_result2['warnings']:
				self.log.warn('warning: %s', warning)

	def on_skipped(self, host, item=None):
		if self.runner.delegate_to:
			host = '%s -> %s' % (host, self.runner.delegate_to)

		if constants.DISPLAY_SKIPPED_HOSTS:
			msg = ''
			if item:
				msg = "skipping: [%s] => (item=%s)" % (host, item)
			else:
				msg = "skipping: [%s]" % host
			self.log.debug(msg)

	def on_no_hosts(self):
		self.log.error('FATAL: no hosts matched or all hosts have already failed -- aborting')

	def on_async_poll(self, host, res, jid, clock):
		if jid not in self._async_notified:
			self._async_notified[jid] = clock + 1
		if self._async_notified[jid] > clock:
			self._async_notified[jid] = clock
			msg = "<job %s> polling, %ss remaining"%(jid, clock)
			self.log.debug(msg)

	def on_async_ok(self, host, res, jid):
		if jid:
			msg = "<job %s> finished on %s"%(jid, host)
			self.log.info(msg)

	def on_async_failed(self, host, res, jid):
		msg = "<job %s> FAILED on %s" % (jid, host)
		self.log.error(msg)

	def on_file_diff(self, host, diff):
		pass