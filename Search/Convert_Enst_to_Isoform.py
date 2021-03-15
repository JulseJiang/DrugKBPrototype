# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        Convert_Enst_to_Isoform
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-12
# @update:      2018-09-12 16:07
# @Software:    PyCharm
#-------------------------------------------------------------------------------

from Base.DBBase import DBBase

class GetIsoformAndEnst(object):
	def __init__(self, entrez_id):
		self.entrez_id = entrez_id
		self.db = DBBase("Uniprot_Information")

	def get_isoform_and_enst(self):

		query_id_result = self.db.find_one_by_one_condition("Entrez_ID", self.entrez_id)
		isoform_and_enst_list = []
		if query_id_result != None:
			uniprot_ensmbel_information = query_id_result.get("Ensmbl_information")
			if uniprot_ensmbel_information != None and uniprot_ensmbel_information != []:
				for item in uniprot_ensmbel_information:
					if item.get("uniprot_unique_flag") == True:
						note = "No assemble annotation found in GRCH37."
					else:
						note = "-"
					if note == '-':
						if item.get("molecule") != None:
							isoform = item.get("molecule").get("@id")
							enst_id = item.get("@id")
							if item.get('property') != None:
								for item_item in item.get('property'):
									if item_item.get("@type") == 'protein sequence ID':
										ensp_id = item_item.get("@value")
									if item_item.get("@type") == 'gene ID':
										ensg_id = item_item.get("@value")
						else:
							if item.get("@id")!= None:
								enst_id = item.get("@id")
								isoform = query_id_result.get("UniprotKB_AC")
								if item.get("property")!=None:
									for item_item in item.get("property"):
										if item_item.get("@type") == "protein sequence ID":
											ensp_id = item_item.get("@value")
										elif item_item.get("@type") == "gene ID":
											ensg_id = item_item.get("@value")
						item_list = [enst_id, ensp_id, ensg_id, isoform, note]
						isoform_and_enst_list.append(item_list)
					else:
						pass
			# print(isoform_and_enst_list)
			return isoform_and_enst_list

	def get_isoform(self, enst_id):
		all_isoform = self.get_isoform_and_enst()
		for item in all_isoform:
			if item[0] == enst_id.split(".")[0]:
				return item[3]


if __name__ == '__main__':
	GetIsoformAndEnst = GetIsoformAndEnst("7468")
	print(GetIsoformAndEnst.get_isoform_and_enst())