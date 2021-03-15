# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        MutationImpactTranscript
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-08-31
# @update:      2018-08-31 19:34
# @Software:    PyCharm
#-------------------------------------------------------------------------------
from Base.DBBase import DBBase
from Search.MutationQuery import MutationQuery
# from UniprotKB_mapping_Entrez import UniprotKBMappingEnst
from Search.Convert_Enst_to_Isoform import GetIsoformAndEnst
class MutationTrancript(object):

	def __init__(self, ID, mutation):
		self.id = ID
		self.db = DBBase('Genes')
		self.mutation_query = MutationQuery(mutation)


	def get_all_tarncript(self):
		gene_data = self.db.find_one_by_one_condition("ENTREZ_ID", self.id)
		gene_genecode_trans = gene_data.get("Trans_Gencode")
		# gene_refseq_data = gene_data.get("Trans_Ref")
		all_tarncript = []
		if gene_genecode_trans!=None:
			for item in gene_genecode_trans:
				all_tarncript.append(item)
		# if gene_refseq_data != None:
		# 	for item in gene_refseq_data:
		# 		all_tarncript.append(item)
		return all_tarncript

	def judge_mutation_position_on_trancript_exon(self, position, transcriot_exon, type=None):
		flag = False
		if type == 'splice-site' or type.startswith("splice-site"):
			transcriot_exon_temp_list = transcriot_exon.split(",")
			for item in transcriot_exon_temp_list:
				if int(position) >= int(item.split("_")[0].replace('"',''))-10 and int(position) <= int(item.split("_")[1].replace('"',''))+10:
					flag = True
			return flag
		else:
			transcriot_exon_temp_list = transcriot_exon.split(",")
			for item in transcriot_exon_temp_list:
				if int(position) >= int(item.split("_")[0].replace('"', '')) and int(position) <= int(
						item.split("_")[1].replace('"', '')):
					flag = True
			return flag



	def get_mutation_impact_transcript(self):
		all_transcript = self.get_all_tarncript()
		mutation = self.mutation_query.get_mutation()
		if mutation.get("Exonic Func") != None:
			mutation_type = mutation.get("Exonic Func")
		else:
			mutation_type = None
		mutation_position = mutation.get("Position")
		mutation_chr = mutation.get("chr")
		if mutation_position != None:
			for item in all_transcript:
				if item.get('coding_exon_region') != 'NA':
					if mutation_chr == item.get("chrom").replace("chr","") or mutation_chr == item.get("chrom"):
						if self.judge_mutation_position_on_trancript_exon(mutation_position, item.get('coding_exon_region'), mutation_type):
							item['flag'] = True
						else:
							item['flag'] = False
					else:
						item['flag'] = False
				else:
					item['flag'] = False
		result = []
		for item in all_transcript:
			if item.get("flag")==True:
				result.append(item.get("TranscriptID"))
		return result

	def get_mutation_impact_isoforms(self):
		all_transcript = self.get_all_tarncript()
		mutation = self.mutation_query.get_mutation()
		# print(mutation.get("Exonic Func"))
		if mutation.get("Exonic Func") != None:
			mutation_type = mutation.get("Exonic Func")
		else:
			mutation_type = None
		mutation_position = mutation.get("Position")
		mutation_chr = mutation.get("chr")
		if mutation_position != None:
			for item in all_transcript:
				if item.get('coding_exon_region') != 'NA':
					if mutation_chr == item.get("chrom").replace("chr", "") or mutation_chr == item.get("chrom"):
						if self.judge_mutation_position_on_trancript_exon(mutation_position,
																		  item.get('coding_exon_region'), mutation_type):
							item['flag'] = True
						else:
							item['flag'] = False
					else:
						item['flag'] = False
				else:
					item['flag'] = False
		transcript_result = []
		for item in all_transcript:
			if item.get("flag") == True:
				transcript_result.append(item.get("TranscriptID"))

		isoform_result = []
		db = GetIsoformAndEnst(self.id)
		for item in transcript_result:
			if db.get_isoform(item) != None:
				isoform_result.append(db.get_isoform(item))


		return isoform_result



if __name__ == '__main__':

	mutation_impact_transcript = MutationTrancript("57680", "gene=57680,location=coding-dnm,position=21899618,chr=14")
	print(mutation_impact_transcript.get_mutation_impact_transcript())

	# print(m.mutation)
	# for i, item in enumerate(s):
	# 	print(i)
	# 	print(item)
