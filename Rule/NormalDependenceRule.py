from DependenceRule import DependenceRule

def getRule(table, col, formater, objtable, objcol):
	return NormalDependenceRule(table, col, formater, objtable, objcol)


class NormalDependenceRule(DependenceRule):

	def check(self):
		print("check NormalDependenceRule")
		for row in range(0, len(self.table.values)):
			my_element = self.table.get_element(row, self.col)['value']
			if len(my_element) == 0 or not my_element:
				continue
			src_set = self.formater.formart(my_element)
			des_set = {self.objtable.get_element(row, self.objcol)['value'] for row in range(0, len(self.objtable.values))}
			if not src_set <= des_set:
				print(src_set, des_set)
				self.table.get_element(row, self.col)['status'] = 'error'
				self.table.append_error_message(row, self.col, self.dependence_message)