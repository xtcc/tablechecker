#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import string
from xml.dom import minidom


def my_import(name):
	mod = __import__(name)
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod


def my_import_silent(name):
	try:
		mod = my_import(name)
	except:
		mod = None
	return mod


def GetData(nodeData):
	#nodeData = node.getElementsByTagName( "Data" )
	#if nodeData == None :
	#	return None
	strRet = ""
	strType = nodeData.getAttribute("ss:Type")
	if strType == "String":
		strRet = "%s" % nodeData.firstChild.data
		#print( strRet )
		return strRet
	elif strType == "Number":
		# 检查是否有小数
		if nodeData.firstChild.data.find(".") == -1:
			return int(nodeData.firstChild.data)
		else:
			return string.atof(nodeData.firstChild.data)


def readxmldata(strXmlFilename):
	strSheetName, ext = os.path.splitext(os.path.basename(strXmlFilename))
	key = []  #保存列，作为key
	all_str_list = []  # 所有配置表字符串，元素为每一行的字符串
	doc = minidom.parse(strXmlFilename)
	# 遍历所有工作表
	for node in doc.getElementsByTagName("Worksheet"):
		#print( "SheetName", node.getAttribute("ss:Name"), strSheetName )
		if node.getAttribute("ss:Name") != strSheetName:
			continue
		# 找到了与文件名同名的工作表
		row = node.getElementsByTagName("Row")
		row_num = 0
		col_num = 0
		for data in row:
			row_num = row_num + 1
			xml_cell = data.getElementsByTagName("Cell")
			str_one_row = []
			str_col_content = ""
			# 第一行是配置表字段名
			if row_num == 1:
				for cell in xml_cell:
					cell_data = cell.getElementsByTagName("Data")
					# Excel真坑人，有时候又会变成ss:Data
					if not cell_data:
						cell_data = cell.getElementsByTagName("ss:Data")
					col_name = ""
					for var in cell_data:
						col_name = GetData(var)
					#以_开头的是策划说明字段不导出
					if not col_name or col_name[1] == "_":
						key.append(None)
					else:
						key.append(col_name)
					str_flag = "" if key[col_num] else "\t[Not Export]"
					#print("key[%s]\t%s %s" % (col_num, col_name, str_flag))
					col_num += 1
				print("--------------------------------------")
			else:
				# 注意: Excel如果某个单元格未设置值，则可能出现两种情况:
				# 1. 无Cell(消失了一列), 后续Cell里会增加ss:Index索引属性来表示列索引(索引是从1开始计数的)
				# 2. 有Cell, 但Cell里无"Data"tag
				key_idx = 0  # 字段索引
				for cell in xml_cell:
					#检查Cell是否有ss:Index属性，有就说明该行的第ss:Index列前面有些列没填数据，有Cell缺失，要补上，同时要修正字段索引
					cell_idx = cell.getAttribute("ss:Index")
					if cell_idx:
						new_key_idx = int(cell_idx) - 1  #Excel的Cell的ss:Index属性是从1开始的
						# 补上缺失的Cell
						for miss_idx in xrange(key_idx, new_key_idx):
							if key[miss_idx]:
								str_cell = ""
								str_cell.encode("utf-8")
								str_col_content += str_cell
								str_one_row.append({'value': str_cell, 'status': 'normal'})
						key_idx = new_key_idx
					#print("key_idx: %s" % key_idx)
					# 忽略首字为'_'的列，这种列是策划说明字段，不导出
					if key[key_idx] == None:
						key_idx += 1
						continue
					str_cell = ""
					cell_data = cell.getElementsByTagName("Data")
					# Excel真坑人，有时候又会变成ss:Data
					if not cell_data:
						cell_data = cell.getElementsByTagName("ss:Data")
					if cell_data:
						for var in cell_data:  # 其实只应该有一个cell，只循环一次
							data = GetData(var)
							if type(data) == 'unicode':
								str_cell = str(data)
							#print("unicode: %s" % str_cell)
							else:
								str_cell = str(data)
							#print("not unicode: %s" % str_cell)
					else:
						str_cell = ""
					str_cell.encode("utf-8")
					str_col_content += str_cell
					str_one_row.append({'value': str_cell, 'status': 'normal'})
					key_idx += 1
				# 如果字段索引小于col_num，则说明该行的末尾有些列未填数据，Cell有缺失，应补上。
				if key_idx < col_num:
					for miss_idx in xrange(key_idx, col_num):
						if key[miss_idx]:
							str_cell = ""
							str_cell.encode("utf-8")
							str_col_content += str_cell
							str_one_row.append({'value': str_cell, 'status': 'normal'})
				# 写入一行数据
				if len(str_col_content) > 0:
					all_str_list.append(str_one_row)
			#print( str_one_row )
	return key, all_str_list
