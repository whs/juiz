from .role import Role

registry = {
	'base': 'juiz.roles.base.BaseRole',
	'web': 'juiz.roles.web.WebRole',
	'memcache': 'juiz.roles.memcache.MemcacheRole',
	'mysql': 'juiz.roles.mysql.MySQLRole',
}