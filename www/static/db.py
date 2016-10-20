#-*- coding : utf -*-
#db.py

class _Engine(object):
	def __init__(self,connect):
		self.connect = connect
	def connect(self):
		return self._connect()
	
engine=None
#持有数据库链接的上下文对象
class _Dbctx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0
	def is_init(self):
		return not self.connection is None
	def init(self):
		self.connection = _LasyConnecion()
		self.transactions = 0
	def cleaup(self):
		self.connection.cleanup()
		self.connection = None
	def cursor(self):
		return self.connection.cursor();
_db_ctx = _Dbctx();

class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.is_init():
			_db_ctx.init();
			self.should_cleanup = True
		return self

	def __exit__(self,exctype,excvalue,traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()
	def connection