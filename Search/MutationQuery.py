# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        MutationQuery
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-01
# @update:      2018-09-01 0:16
# @Software:    PyCharm
#-------------------------------------------------------------------------------
from Base.DBBase import DBBase
class MutationQuery(object):

	def __init__(self, url_information):
		self.url_information = url_information
		# print(url_information)
		self.db = DBBase('Genes')

	def resolve_url(self):
		url_information_list = self.url_information.split(',')
		url_information_dict = {}
		for item in url_information_list:
			try:
				item_key, item_value = item.split('=')
				url_information_dict[item_key] = item_value
			except:
				num = 0
				for index, item_item in enumerate(item):
					if item_item in "0123456789":
						num = index
						break
				item_key = item[0:num]
				item_value = item[num:-1]
				url_information_dict[item_key] = item_value

		return url_information_dict

	def is_type(self, a):
		lis = "1234567890"
		for item in a:
			if item not in lis:
				return "symbol"
			else:
				return "ID"

	def get_mutation(self):
		mutation_dict = self.resolve_url()
		if self.is_type(mutation_dict.get('gene')) == 'ID':
			id_or_symbol = "ENTREZ_ID"
		else:
			id_or_symbol = "Symbol"
		if mutation_dict.get('location') == 'cnv':
			dnm_orcnv = 'CNV'
		else:
			dnm_orcnv = 'DNM'

		all_mutation = self.db.find_one_by_one_condition(id_or_symbol, mutation_dict.get('gene')).get(dnm_orcnv)
		for item in all_mutation:
			if dnm_orcnv == 'DNM':
				if item.get('chr') == mutation_dict.get('chr') and item.get('Position') == mutation_dict.get('position'):
					return item
			else:
				if item.get('start') == mutation_dict.get('start') and item.get('end') == mutation_dict.get('end'):
					return item



if __name__ == '__main__':
	# mq = MutationQuery('gene=7468,location=coding-dnm,position=1980530,chr=4')
	# print(mq.get_mutation())
	# db = DBBase('Gene')
	# print(db.find_one_by_one_condition("Symbol", "NSD2"))

	# mq1 = MutationQuery('gene=7468,location=cnv,start=45410,end=3541587')
	# mq1.resolve_utr()
	mq = MutationQuery('gene=29072,location=coding-dnm,position=47098932,chr=3')
	print(mq.get_mutation())
	pass
