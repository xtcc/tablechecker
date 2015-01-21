#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Table import Table
from Util.MyUtil import readxmldata, my_import_silent
from config.config import TABLE_DIR, CONFIG_FILE


class TableMgr(object):
	_tables = []

	def init(self):
		#init tables from configuration file
		keys, values = readxmldata(CONFIG_FILE)
		for value in values:
			mypath = TABLE_DIR + value[0]['value']
			print("create " + mypath)
			# create table
			table = self.create_table(mypath)

			# create & set unique keys
			myukeys = eval(value[1]['value'])
			table.set_unique_keys(myukeys)

			# create & set not null keys
			mynkeys = eval(value[2]['value'])
			table.set_notnull_keys(mynkeys)

			# create & set dependence rules
			mydrules = eval(value[3]['value'])
			for drule in mydrules:
				col, rule, formater, objtable, objcol = drule
				myformater = my_import_silent(formater).getFormater()
				objpath = TABLE_DIR + objtable
				objtable = self.create_table(objpath)
				myrule = my_import_silent(rule).getRule(table, col, myformater, objtable, objcol)
				table.add_dependence_rule(myrule)

			self._tables.append(table)

	def create_table(self, table_path):
		mykeys, myvalues = readxmldata(table_path)
		table = Table(table_path, mykeys, myvalues)
		return table


	def check_all_tables(self):
		for table in self._tables:
			table.check()
			f = open('log.txt', 'w')
			f.write("check "+table.path+"\r\n")
			result, msg = table.get_result()
			f.write(msg)
			print (result, msg)