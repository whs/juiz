from juiz.ui.ProjectConfig import ProjectConfig as PC

class ProjectConfig(PC):
	def __init__(self, project, *args, **kwargs):
		self.project = project
		super(ProjectConfig, self).__init__(*args, **kwargs)