# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        test
# @Author:      PuFeng
# @Purpose:
# @Created:     2018/8/19
# @update:      2018/8/19 10:00
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import pymongo
import json
from functools import reduce

class DataStorage:
	"""
	数据库查询类
	"""

	def __init__(self, name):
		self.name = name
		self.path = self.__login()

	def __login(self):
		client = pymongo.MongoClient(mod_config.getConfig("database", "dbhost"), 27017)
		db = client[mod_config.getConfig("database", "dbname")]
		if mod_config.getConfig("database", "dbuser") != "":
			db.authenticate("tanxian123", "123456")
		collection = client[mod_config.getConfig("database", "dbname")][self.name]
		return collection

	def Storage(self, dic):
		return self.path.insert(dic)

	def FindPPI(self, ID):
		a = self.FindByID(ID)
		if "PPI" in a:
			x = []
			for i in a["PPI"]:
				if "ENTREZ_A" in i:
					x.append(i)
			return x
		else:
			return None

	def FindByID(self, ID):
		x = self.path.find_one({'ENTREZ_ID': ID})
		return x

class DrawBioGridPPI:
	def __init__(self):
		pass

	def FindSymbol(self, symbol_id, ppi):
		node_symbol = ''
		for item in ppi:
			if (str(symbol_id) == str(item["ENTREZ_A"])):
				node_symbol = item["Symbol_A"]
				break
			elif (str(symbol_id) == str(item["ENTREZ_B"])):
				node_symbol = item["Symbol_B"]
				break
		#print("id:"+symbol_id+"symbol:"+node_symbol)
		return node_symbol

	def list_dict_duplicate_removal(self,data_list):#去重
		run_function = lambda x, y: x if y in x else x + [y]
		return reduce(run_function, [[], ] + data_list)
	# 绘制PPI图像
	def draw_biogrid_ppi(self, id, f):
		ppi = f.FindPPI(id)
		all = f.FindByID(str(id))
		arr_nodes = []
		arr_edges = []
		dict_nodes = {}
		dict_edges = {}
		try:
			for node_id in all.get("PPI_Points"):#点集
				node_symobel = self.FindSymbol(node_id, ppi)
				if node_symobel != 'NA':
					data_nodes = {'data': {}}
					if node_id == id:
						data_nodes['data']['group'] = 'core'
					else:
						data_nodes['data']['group'] = 'attr'
					data_nodes['data']['id'] = node_id
					data_nodes['data']['href'] = 'http://psymukb.net/GeneDetail/' + node_id
					data_nodes['data']['name'] = node_symobel
					dict_nodes['group'] = 'nodes'
					data_nodes.update(dict_nodes)
					arr_nodes.append(data_nodes)
			arr_nodes=self.list_dict_duplicate_removal(arr_nodes)#去重
			#print(arr_nodes)
			for item in ppi:#边集
				# print(item)
				data_edges = {'data': {}}
				if item["ENTREZ_A"] == id:#直接作用
					data_edges['data']['faveColor'] = '#FF6347'
				elif item["ENTREZ_B"] == id:
					data_edges['data']['faveColor'] = '#FF6347'
				else:#间接作用
					data_edges['data']['faveColor'] = '#BEBEBE'#灰色
				if(int(item["Evidence"])>90):
					data_edges['data']['width'] = 90
				else:
					data_edges['data']['width'] = item["Evidence"]
				# data_edges['data']['width'] = item["Evidence"]
				dict_edges['group'] = "edges"
				data_edges['data']['source'] = item["ENTREZ_A"]
				data_edges['data']['target'] = item["ENTREZ_B"]
				data_edges.update(dict_edges)
				arr_edges.append(data_edges)
			arr_edges = self.list_dict_duplicate_removal(arr_edges)
			#print(arr_edges)
			arr_nodes.extend(arr_edges)
			results = json.dumps(arr_nodes)
			return results
		except:
			return None


class Main:
	def __init__(self):
		pass

	def run(self, id):
		f = DataStorage("Genes")
		draw = DrawBioGridPPI()
		return draw.draw_biogrid_ppi(id, f)


if __name__ == '__main__':
	m = Main()
	m.run("7468")
