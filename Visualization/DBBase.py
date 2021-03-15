# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        DBBase
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-01
# @update:      2018-09-01 0:37
# @Software:    PyCharm
# -------------------------------------------------------------------------------
# from Base import mod_config
import pymongo


class DBBase(object):
	def __init__(self, name):
		self.name = name
		self.path = self.__login()

	def __login(self):
		client = pymongo.MongoClient("127.0.0.1", 27017)
		db = client['Denovo']
		# db.authenticate("tanxian123", "123456")
		collection = client['Denovo'][self.name]
		return collection

	def find_one_by_one_condition(self, db_field, value):
		return self.path.find_one({db_field: value})

	def find_count_by_one_condition(self, db_field, value):
		result_list = []
		for item in self.path.find({db_field: value}):
			result_list.append(item)
		return result_list

	def find_one_by_many_conditions(self, db_fields, value):
		assert len(db_fields) == len(value)
		condition_dict = {}
		for key, value in zip(db_fields, value):
			condition_dict[key] = value
		return self.path.find(condition_dict)

	def find_count_by_many_conditions(self, fields):
		pass


def main():
	pass


if __name__ == '__main__':
	main()
