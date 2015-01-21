from config.config import dependence_message

class DependenceRule(object):
	table = None
	col = ""
	formater = None
	objtable = ""
	objcol = ""
	dependence_message = dependence_message
	def __init__(self, table, col, formater, objtable, objcol):
		self.table = table
		self.col = col
		self.formater = formater
		self.objtable = objtable
		self.objcol = objcol

	def check(self):
		pass
