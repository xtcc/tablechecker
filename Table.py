from config.config import null_message, unique_message


class Table(object):
	path = ""
	keys = []
	values = []
	unique_keys = []
	notnull_keys = []
	dependence_rules = []
	error_msg = ""

	def __init__(self, path, keys, values):
		self.path = path
		self.keys = keys
		self.values = values
		self.unique_keys = []
		self.notnull_keys = []
		self.dependence_rules = []
		self.error_msg = ""

	def get_key_index(self, key):
		return self.keys.index(key)

	def get_element(self, row, key):
		return self.values[row][self.get_key_index(key)]

	def set_element(self, row, key, value):
		self.values[row][self.get_key_index(key)] = value

	def set_unique_keys(self, ukeys):
		self.unique_keys = ukeys

	def set_notnull_keys(self, nkeys):
		self.notnull_keys = nkeys

	def append_error_message(self, row, key, msg):
		# excel row start from 1 & table head plus 1
		my_row = row+2
		self.error_msg = self.error_msg + '('+str(my_row)+','+key+') '+msg + '\r\n'

	def check_unique(self):
		print("check unique rule")
		for key in self.unique_keys:
			key_map = {}
			for row in range(0, len(self.values)):
				if key_map.get(self.get_element(row, key)['value']):
					self.get_element(row, key)['status'] = 'error'
					self.append_error_message(row, key, unique_message)
				else:
					key_map[self.get_element(row, key)['value']] = True

	def check_notnull(self):
		print("check notnull rule")
		for key in self.notnull_keys:
			for row in range(0, len(self.values)):
				if len(self.get_element(row, key)['value']) == 0 or not self.get_element(row, key)['value']:
					self.get_element(row, key)['status'] = 'error'
					self.append_error_message(row, key, null_message)

	def check_dependence(self):
		for rule in self.dependence_rules:
			rule.check()

	def add_dependence_rule(self, rule):
		self.dependence_rules.append(rule)

	def check(self):
		#check unique keys
		self.check_unique()
		#check not null keys
		self.check_notnull()
		#check dependence keys
		self.check_dependence()

	def get_result(self):
		if len(self.error_msg) == 0:
			return True, ""
		else:
			return False, self.error_msg


