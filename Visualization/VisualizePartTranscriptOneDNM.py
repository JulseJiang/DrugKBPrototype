# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        Transcript DNM visualization
# @Author:      GuoSijia
# @Purpose:     修正了转录本大量重复时候的bug
# @Created:     2018-05-24
# @update:      2018-06-13 13:26
# @Software:    PyCharm
#-------------------------------------------------------------------------------
import pymongo
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly
from itertools import chain

class DataQuery(object):
	"""
	数据库查询类
	"""

	def __init__(self, name, transcript_id, mutation):
		self.name = name
		self.path = self.__login()
		# self.transcript_type = transcript_type
		self.transcript_id = transcript_id
		self.mutation = mutation

	def __login(self):
		client = pymongo.MongoClient("127.0.0.1", 27017)
		db = client['Denovo']
		# db.authenticate("tanxian123", "123456")
		collection = client['Denovo'][self.name]
		return collection

	def FindByID(self, ID):
		return self.path.find_one({'ENTREZ_ID': ID})

	def FindCountByID(self, ID):
		dlist = []
		for item in self.path.find({'ENTREZ_ID': ID}):
			dlist.append(item)
		return dlist

	def GetAllGeneStruceterData(self, res):
		d_list = []
		for item in res:
			# trans_ref = item.get("Trans_Ref")
			trans_genecode = item.get('Trans_Gencode')
			if trans_genecode != None:
				for item_item in trans_genecode:
					# print(item_item.get("TranscriptID"))
					if item_item.get("TranscriptID") in self.transcript_id:
						d_list.append(item_item)
			# if trans_ref != None:
			# 	for item_item in trans_ref:
			# 		# print(item_item.get["TranscriptID"])
			# 		if item_item.get("TranscriptID") in self.transcript_id:
			# 			d_list.append(item_item)
		return d_list


	def RemoveDictValueColon(self, dlist):
		for item in dlist:
			for k in item:
				item[k] = item[k].replace('"', '')
		return dlist


	def get_DNM(self, data):
		mutaion = self.mutation
		target =mutaion.split(",")
		target_dict = {}
		for item in target:
			target_dict[item.split("=")[0]] = item.split("=")[1]
		# print(target_dict)
		res = []
		for item in data:
			for item_item in item['DNM']:
				# print(item_item)
				if item_item["Position"] == target_dict["position"]:
					if item_item.get("Func refGene") == 'exonic':
						if isinstance(item_item['Exonic Func'], str):
							s = item_item['Position'] + ',' + item_item['Variant'] + ',' + item_item['Exonic Func']
						elif isinstance(item_item['Exonic Func'], list):
							s = item_item['Position'] + ',' + item_item['Variant'] + ',' + "".join(item_item['Exonic Func'])
					else:
						if isinstance(item_item['Func refGene'], str):
							s = item_item['Position'] + ',' + item_item['Variant'] + ',' + item_item['Func refGene']
						elif isinstance(item_item['Func refGene'], list):
							s = item_item['Position'] + ',' + item_item['Variant'] + ',' + "".join(
								item_item['Func refGene'])
					res.append([int(item_item['Position']), s])
			else:
				res.append([])
		# print(res)
		# print(res)
		return res

class Data_handing(object):

	def __init__(self):
		self.Sym, self.exton, self.utr3, self.utr5 = range(4)
		self.Start, self.End = range(2)

	def hb_list_2D(self, test):
		####合并相邻区间的二维数组#####
		i = 0
		l = len(test)
		while i < l - 1:
			if test[i][1] == test[i + 1][0]:
				test[i] = [test[i][0], test[i + 1][1]]
				test.pop(i + 1)
				l = l - 1
			else:
				i += 1
		return test

	def hb_list_3D(self, list1):

		for i in range(len(list1)):
			if list1[i] != []:
				list1[i] = self.hb_list_2D(list1[i])
		return list1

	def get_all_exton_region(self, list_3D):
		#####获取所有区域#####
		all_region = []
		for item in list_3D:
			for item_item in chain(item[self.exton], item[self.utr3], item[self.utr5]):
				all_region.append(item_item)
		return all_region

	def drop_duplicate(self, one_list):
		#####去除所有区域中的重复段#####
		temp_list=[]
		for one in one_list:
			if one not in temp_list:
				temp_list.append(one)
		return temp_list

	def sort_list(self, all_region):
		#####对所有的外显子区域list根据第一个元素大小进行排序#####
		l = len(all_region)
		all_region = sorted(all_region, key=lambda x: x[0])
		for ii in range(l-1):
			assert all_region[ii][self.Start]<=all_region[ii+1][self.Start]
			# assert all_exton[ii][self.End]<=all_exton[ii+1][self.End]
		return all_region

	def cut_fragment(self, all_region):
		#####将所有区域切分成若干个不重复，不交叉的小段#####
		all_s = [item[self.Start] for item in all_region]
		all_e = [item[self.End] for item in all_region]
		all_se = []
		for item in chain(all_s, all_e):
			all_se.append(item)
		all_se = sorted(set(all_se))
		a = all_se[:-1]
		b = all_se[1:]
		all_frag = []
		for x, y in zip(a,b):
			all_frag.append([x, y])
		return all_frag

	def get_sum(self, x_list, n):
		####求一个list的前n项和#####
		return sum(x_list[:n])

	def get_every_frag_dnm_numbers(self, all_frag, DNM):

		DNM_list = [item[0] for item in DNM]
		DNM_list = list(set(DNM_list))
		DNM_list = sorted(DNM_list)
		num = [0] * len(all_frag)
		i = 0
		for item in all_frag:
			kk = 0
			for item_item in DNM_list:
				if item_item >= item[self.Start] and item_item <= item[self.End]:
					num[i] += 1
				kk += 1
			i += 1

		return num

	def scale_fragment(self, all_frag, DNM):
		####规定一个新的片段，规定所有小段（包括外显子和内含子的长度均为30）#####
		ll = []
		num = self.get_every_frag_dnm_numbers(all_frag, DNM)
		for item in num:
			if item < 3:
				ll.append(22)
			else:
				ll.append(item*10+2)
		#ll = [20] * len(all_frag)
		re_a = [self.get_sum(ll, n) for n in range(len(ll))]
		re_b = [self.get_sum(ll, n) for n in range(1, len(ll)+1)]
		scale_frag = []
		for x, y in zip(re_a, re_b):
			scale_frag.append([x,y])
		return scale_frag

	def count_exton_region_in_fragment(self, list_3D, all_frag, scale_frag):
		#####遍历所有外显子区域，统计出所有小段出现在外显子的位置，并将新的小段（自定义间距后的）放到对应位置#####
		ae = list(item[self.exton] for item in list_3D)
		i = 0
		count = []
		count1 = []
		for item in ae:
			temp1 = []
			temp2 = []
			for item1 in item:
				j = 0
				for item2 in all_frag:
					if item2[self.Start] >= item1[self.Start] and item2[self.End] <= item1[self.End]:
						temp1.append(scale_frag[j])
						temp2.append(all_frag[j])
					j+=1
			count.append(temp1)
			count1.append(temp2)
			i+=1
		count= self.hb_list_3D(count)
		count1 = self.hb_list_3D(count1)
		return count, count1

	def count_utr_region_in_fragment(self, list_3D, all_frag, scale_frag):
		#####遍历所有utr区域，统计出所有小段出现在utr的位置，并将新的小段（自定义间距后的）放到对应位置#####
		ae_utr = []
		for item in list_3D:
			temp = []
			for item_item in chain(item[self.utr3], item[self.utr5]):
				temp.append(item_item)
			ae_utr.append(temp)
		count = []
		count1 = []
		for item in ae_utr:
			temp1 = []
			temp2 = []
			for item1 in item:
				j = 0
				for item2 in all_frag:
					if item2[self.Start] >= item1[self.Start] and item2[self.End] <= item1[self.End]:
						temp1.append(scale_frag[j])
						temp2.append(all_frag[j])
					j+=1
			count.append(temp1)
			count1.append(temp2)
		count= self.hb_list_3D(count)
		count1 = self.hb_list_3D(count1)
		return count, count1

	def count_to_xy(self, list_3D, count, count1):
		#####将片段准换成作画需要的坐标#####
		y = [item[0] for item in list_3D]
		xy = []
		for item, yy, z in zip(count, y, count1):
			for item_item, item_tips in zip(item, z):
				temp = [[item_item[0], yy, item_tips[0]], [item_item[1], yy, item_tips[1]]]
				xy.append(temp)
		return xy

	def DNM_sort_by_site(self, DNM):
		# print(DNM)
		for index, item in enumerate(DNM):
			if item == []:
				DNM.pop(index)
		if DNM != [[]]:
			sorted_DNM = sorted(DNM, key=lambda x: x[0])
			return sorted_DNM
		else:
			return []





	def mapping_mutation_to_frag(self, all_frag, scale_frag, DNM= []):

		DNM_list = [item[0] for item in DNM]
		DNM_list = list(set(DNM_list))
		DNM_list = sorted(DNM_list)
		DNM_tips = list(set([item[1] for item in DNM]))
		DNM_tips = sorted(DNM_tips, key=lambda x: x.split(',')[0])
		num = [0] * len(all_frag)
		i = 0
		DNM_frag = []
		for item in all_frag:
			temp = []
			kk = 0
			for item_item in DNM_list:
				if item_item >= item[self.Start] and item_item <= item[self.End]:
					num[i]+=1
					temp1= []
					temp1.append(item_item)
					temp1.append(DNM_tips[kk])
					temp.append(temp1)
				kk+=1
			DNM_frag.append(temp)
			i+=1
		DNM = []
		j = 0
		for item in num:
			if item !=0:
				start = scale_frag[j][self.Start]+2
				temp = []
				for k in range(item):
					temp1 = []
					temp1.append(start)
					temp1.append(start + 3)
					temp1.append(DNM_frag[j][k][0])
					temp1.append(DNM_frag[j][k][1])
					temp.append(temp1)
					start += 10
				DNM.append(temp)
			j+=1
		return DNM

	def sort_count_utr(self, count_utr):
		for i in range(len(count_utr)):
			count_utr[i] = sorted(count_utr[i], key=lambda x: x[0])
		return count_utr

	def get_trans_region(self, count):
		res = []
		for item in count:
			if item != []:
				res.append([item[0][self.Start], item[-1][self.End]])
			else:
				pass
		return res

	def trans_DNM(self, trans_region, DNM, list_3D):
		y = [item[self.Sym] for item in list_3D]
		res = []
		for item in DNM:
			for item2 in item:
				i = 0
				for item_item in trans_region:
					if item2[0] >= item_item[0] and item2[1] <=item_item[1]:
						# res.append([item2[0], item2[1],y[i], item2[3]])
						for item_y in y:
							res.append([item2[0], item2[1],item_y, item2[3]])

					i+=1
		fin_DNM_xy = []
		for item in res:
			# print(item)
			fin_DNM_xy.append([[item[0], item[2], item[3]], [item[1], item[2], item[3]]])
		return fin_DNM_xy

class Data_to_Plot(object):

	def __init__(self):
		pass

	def run(self, list_3D, DNM_list):

		data_treat = Data_handing()
		DNM_list = data_treat.DNM_sort_by_site(DNM_list)
		all_exon_region = data_treat.get_all_exton_region(list_3D)
		all_exon_region = data_treat.drop_duplicate(all_exon_region)
		all_exon_region = data_treat.sort_list(all_exon_region)
		all_frag = data_treat.cut_fragment(all_exon_region)
		scale_frag = data_treat.scale_fragment(all_frag, DNM_list)
		count_exon, count1_exon = data_treat.count_exton_region_in_fragment(list_3D, all_frag, scale_frag)
		count_exon_xy = data_treat.count_to_xy(list_3D, count_exon, count1_exon)
		count_utr, count1_utr = data_treat.count_utr_region_in_fragment(list_3D, all_frag, scale_frag)
		count_utr_xy = data_treat.count_to_xy(list_3D, count_utr, count1_utr)


		DNM = data_treat.mapping_mutation_to_frag(all_frag, scale_frag, DNM_list)
		count_utr = data_treat.sort_count_utr(count_utr)
		trans_region = data_treat.get_trans_region(count_utr)
		fin_DNM_xy = data_treat.trans_DNM(trans_region, DNM, list_3D)
		return count_exon_xy, count_utr_xy, fin_DNM_xy

class DrawGeneStructure(object):
	def __init__(self):
		pass


	def str_to_int(self, list_2D):
		new_list_2D = []
		for item in list_2D:
			new_item = []
			for item_item in item:
				new_item.append(int(item_item))
			new_list_2D.append(new_item)
		return new_list_2D

	def str_to_list(self, str):
		list_1D = str.split(',')
		list_2D = [item.split('_') for item in list_1D]
		return self.str_to_int(list_2D)


	def get_DNM_color(self, s_type):
		# if s_type in ['frameshift deletion', 'frameshift insertion', 'frameshift substitution',
		# 			  'splice-site mutation', 'stopgain', 'stoploss'] or s_type.startswith('frameshift'):
		# 	color = 'red'
		# elif s_type in ['nonframeshift deletion', 'nonframeshift insertion',
		# 				'nonframeshift substitution', 'nonsynonymous SNV', 'strat gain' , 'stoploss'] or s_type.startswith('nonframeshift'):
		# 	color = 'pink'
		# elif s_type in ['synonymous SNV', 'exonic', 'coding complex']:
		# 	color = 'purple'
		# elif s_type in ['unknown']:
		# 	color = 'yellow'
		# else:
		# 	color = 'blue'
		return 'red'

	def gene_structure_data_deal(self, target_dlist):
		target_df = pd.DataFrame(target_dlist)
		target_dict = target_df.to_dict(orient='records')
		records = []
		for row in target_dict:
			temp = []
			if (row['TranscriptID'] not in ['NULL', 'NaN', '']):
				TranscriptID = row['TranscriptID']
			else:
				TranscriptID = []
			if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':  # isnan(row['utr5_exon_region']) == False:
				utr5_exon_region = self.str_to_list(row['utr5_exon_region'])
			else:
				utr5_exon_region = []
			if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':  # isnan(row['utr3_exon_region']) == False:
				utr3_exon_region = self.str_to_list(row['utr3_exon_region'])
			else:
				utr3_exon_region = []
			if type(row['coding_exon_region']) == str and row['coding_exon_region'] != 'NA':  # isnan(row['coding_exon_region']) == False:
				coding_exon_region = self.str_to_list(row['coding_exon_region'])
			else:
				coding_exon_region = []
			temp.append(TranscriptID)
			temp.append(coding_exon_region)
			temp.append(utr3_exon_region)
			temp.append(utr5_exon_region)
			records.append(temp)
		return records

	def gene_structure_plot(self, exton_records, utr_records, DNM_xy, transcript_len = 6):

		trace_coding = []
		exton_num = 0
		for index, item in enumerate(exton_records):
			if index != len(exton_records)-1:
				trace_coding_item = Scatter(
					visible=True,
					hoverinfo='text',
					showlegend=False,
					mode='lines',
					x=[item[0][0], item[1][0]],
					y=[item[0][1], item[1][1]],
					text='['+str(item[0][2])+'-'+str(item[1][2])+']',
					line=dict(
						color='rgb(65,105,225)',
						# color='rgb(193,210,240)',
						shape='linear',
						width=10,
						simplify=True
					),
				)
				trace_coding.append(trace_coding_item)
				exton_num+=1
			else:
				trace_coding_item = Scatter(
					visible=True,
					hoverinfo='text',
					name='Exon',
					showlegend=False,
					mode='lines',
					x=[item[0][0], item[1][0]],
					y=[item[0][1], item[1][1]],
					text='[' + str(item[0][2]) + '-' + str(item[1][2]) + ']',
					line=dict(
						color='rgb(65,105,225)',
						# color='rgb(193,210,240)',
						shape='linear',
						width=10,
						simplify=True
					),
				)
				trace_coding.append(trace_coding_item)
				exton_num += 1

		for item in utr_records:
			trace_utr_item = Scatter(
				visible=True,
				hoverinfo='text',
				showlegend=False,
				mode='lines',
				x=[item[0][0], item[1][0]],
				y=[item[0][1], item[1][1]],
				text='['+str(item[0][2])+'-'+str(item[1][2])+']',
				line=dict(
					color='gray',
					shape='linear',
					width=5,
					simplify=True
				),
			)
			trace_coding.append(trace_utr_item)
			exton_num+=1

		for item in DNM_xy:
			type = item[0][2].split(',')[2]
			c = self.get_DNM_color(type)
			dnm_item = Scatter(
				visible=True,
				hoverinfo='text',
				showlegend=False,
				mode='lines',
				x=[item[0][0], item[1][0]],
				y=[item[0][1], item[1][1]],
				legendgroup=c,
				name=c,
				text=str(item[0][2]),
				hoverlabel={
					# 'bgcolor': None,
					'font': {
						'size': 10
					}
				},
				line=dict(
					color=c,
					shape='linear',
					width=12,
					simplify=True
				),
			)
			trace_coding.append(dnm_item)

		layouts = go.Layout(
			# paper_bgcolor='rgb(249, 249, 249)',
			# plot_bgcolor='rgb(249, 249, 249)',
			height=transcript_len*70,
			width=800,
			# title='Transcript DNM Visualizations',
			# titlefont=dict(size=25),
			hovermode='closest',
			# hoverdistance=5,
			margin=go.Margin(  # x,y轴label距离图纸四周的距离
				l=130,
				r=0,
				# b=50,
				t=25,
				pad=0
			),
			xaxis=dict(
				showgrid=False,
				zeroline=False,
				showline=False,
				showticklabels=False,
				# tickformat='r',
				# dtick=10,
				autorange=True

			),
			yaxis=dict(
				titlefont=dict(
					family='Arial, sans-serif',
					size=20,
					color='lightgrey'
				),
				showticklabels=True,
				tickangle=360,
				tickfont=dict(
					family='Old Standard TT, serif',
					size=12,
					color='black'
				),
				exponentformat='e',
				showexponent='All'
			)

		)
		figs = go.Figure(data=trace_coding, layout=layouts)
		# plotly.offline.plot(figs, show_link=False)
		try:
			return plotly.offline.plot(figs,show_link=False, output_type="div")
		except:
			return '<div>There is no corresponding data published yet, we will update it when such data available. </div>'

class PlotRun(object):
	def __init__(self, transcript_id, mutation):
		self.transcript_id = transcript_id
		self.mutation = mutation
	def run(self, id):
		a = DataQuery("Genes", self.transcript_id, self.mutation)
		transcript_len = len(a.transcript_id)
		res = a.FindCountByID(id)

		cdlist = a.GetAllGeneStruceterData(res)

		dl = a.RemoveDictValueColon(cdlist)

		dnm_list = a.get_DNM(res)

		g_d = DrawGeneStructure()

		records = g_d.gene_structure_data_deal(dl)
		dp = Data_to_Plot()
		count_exon_xy, count_utr_xy, fin_DNM_xy= dp.run(records, dnm_list)
		if transcript_len != 0:
			return g_d.gene_structure_plot(count_exon_xy, count_utr_xy, fin_DNM_xy, transcript_len)
		else:
			return '<div>There is no isoform with coding regions being impact. </div>'

def main(ID):
	mutaion = 'gene=3191,location=coding-dnm,position=39329153,chr=19'
	transcript_id = ['ENST00000221419.5', 'ENST00000601449.1', 'ENST00000600873.1']
	plot_run = PlotRun(transcript_id, mutaion)
	ID=str(ID)
	return plot_run.run(ID)# plot_run.run("7468")

	# mutaion = 'gene=29072,location=coding-dnm,position=47098932,chr=3'
	# transcript_id = ['ENST00000409792.3']
	# plot_run = PlotRun(transcript_id, mutaion)
	# ID = str(ID)
	# return plot_run.run(ID)  # plot_run.run("7468")

if __name__ == '__main__':
	main(3191)
