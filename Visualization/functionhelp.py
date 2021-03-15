# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        function
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2019-04-21
# @update:      2019-04-21 9:39
# @Software:    PyCharm
#-------------------------------------------------------------------------------
import pymongo
import numpy as np
import math

class DataStorage:

	def __init__(self, collection_name="", ip_adress='127.0.0.1', port=27017, user="tanxian123", password="123456",
				 db_name="Denovo"):
		self.name = collection_name
		self.path = self.__login(ip_adress, port, user, password, db_name)

	def __login(self, ip_adress, port, user, password, db_name):
		client = pymongo.MongoClient("127.0.0.1", 27017)
		db = client['Denovo']
		# db.authenticate("tanxian123", "123456")
		collection = client['Denovo'][self.name]
		return collection

	def Storage(self, dic):
		return self.path.insert(dic)

	def FindByID(self, ID):
		return self.path.find_one({'ENTREZ_ID': ID})

	def find_one_by_one_condition(self, db_field, value):
		return self.path.find_one({db_field: value})

	def find_count_by_one_condition(self, db_field, value):
		result_list = []
		for item in self.path.find({db_field: value}):
			result_list.append(item)
		return result_list


class PPIPointClass(object):

	def __init__(self):
		self.ds_gene = DataStorage('Genes')

		# self.ds_protein_exp = DataStorage('ProteinExpress_Update')
		# self.ds_gene_express = DataStorage('Gtex_Gene_AllTissue')


	def get_mutation_count(self, id):
		'''
		判断目标基因携带新发突变个数
		:param id: 基因ENTREZ_ID
		:return: 该基因携带新发突变个数
		'''
		gene_inforamtion = self.ds_gene.FindByID(id)
		if gene_inforamtion == None:
			return 0
		else:
			return gene_inforamtion.get('MutationCount')

	def get_protein_brain_exp_flag(self, id):
		'''
		判断目标基因对应的蛋白在脑组织中是否有表达
		:param id: 基因ENTREZ_ID
		:return: 蛋白层面是否在脑中有表达
		'''
		gene_inforamtion = self.ds_gene.FindByID(id)
		if gene_inforamtion == None:
			return False
		else:
			return gene_inforamtion.get('ProteinBrainExpress')


	def get_gene_brain_exp_flag(self, id):
		'''
		判断目标基因在脑组织中是否有表达
		:param id: 基因ENTREZ_ID
		:return: 基因层面是否在脑中有表达
		'''
		gene_inforamtion = self.ds_gene.FindByID(id)
		if gene_inforamtion == None:
			return False
		else:
			return gene_inforamtion.get('GeneBrainExpress')

# if __name__ == '__main__':
# 	node_id='126961'
# 	data_nodes = {'data': {}}
# 	ppipointclass=PPIPointClass()
# 	print(ppipointclass.get_mutation_count(node_id))
# 	print(ppipointclass.get_protein_brain_exp_flag(node_id))
# 	print(ppipointclass.get_gene_brain_exp_flag(node_id))
# 	if ((ppipointclass.get_mutation_count(node_id) != 0) and (
# 			ppipointclass.get_protein_brain_exp_flag(node_id) == False) and (
# 			ppipointclass.get_gene_brain_exp_flag(node_id) == False)):
# 		data_nodes['data']['color'] = '#FE0000'  # 红色
# 		data_nodes['data']['type'] = 'circle'
# 	elif ((ppipointclass.get_mutation_count(node_id) == 0) and (
# 			ppipointclass.get_protein_brain_exp_flag(node_id) == True) and (
# 				  ppipointclass.get_gene_brain_exp_flag(node_id) == False)):
# 		data_nodes['data']['color'] = '#000081'  # 蓝色
# 		data_nodes['data']['type'] = 'circle'
# 	elif ((ppipointclass.get_mutation_count(node_id) == 0) and (
# 			ppipointclass.get_protein_brain_exp_flag(node_id) == False) and (
# 				  ppipointclass.get_gene_brain_exp_flag(node_id) == True)):
# 		data_nodes['data']['color'] = '#039735'  # 绿色
# 		data_nodes['data']['type'] = 'circle'
# 	elif ((ppipointclass.get_mutation_count(node_id) != 0) and (
# 			ppipointclass.get_protein_brain_exp_flag(node_id) == True) and (
# 				  ppipointclass.get_gene_brain_exp_flag(node_id) == False)):
# 		data_nodes['data']['color'] = '#D60093'
# 		data_nodes['data']['type'] = 'triangle'
# 	elif ((ppipointclass.get_mutation_count(node_id) != 0) and (
# 			ppipointclass.get_protein_brain_exp_flag(node_id) == False) and (
# 				  ppipointclass.get_gene_brain_exp_flag(node_id) == True)):
# 		data_nodes['data']['color'] = '#FFFE35'
# 		data_nodes['data']['type'] = 'rectangle'
# 	elif ((ppipointclass.get_mutation_count(node_id) == 0) and (
# 			ppipointclass.get_gene_brain_exp_flag(node_id) == True) and (
# 				  ppipointclass.get_protein_brain_exp_flag(node_id) == True)):
# 		data_nodes['data']['color'] = '#3497CE'
# 		data_nodes['data']['type'] = 'barrel'
# 	elif ((ppipointclass.get_mutation_count(node_id) != 0) and (
# 			ppipointclass.get_gene_brain_exp_flag(node_id) == True) and (
# 				  ppipointclass.get_protein_brain_exp_flag(node_id) == True)):
# 		data_nodes['data']['type'] = 'diamond'
# 		data_nodes['data']['color'] = '#000000'
# 	else:
# 		data_nodes['data']['type'] = 'circle'
# 		data_nodes['data']['color'] = '#669999'
# 	print(data_nodes)