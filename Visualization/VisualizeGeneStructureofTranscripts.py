# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        all
# @Author:      GuoSijia
# @Purpose:     没加突变的基因结构可视化
# @Created:     2018-04-26
# @update:      2018-04-26 23:05
# @Software:    PyCharm
#-------------------------------------------------------------------------------
import pymongo
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly

class DataQuery(object):

	def __init__(self, name):
		self.name = name
		self.path = self.__login()

	def __login(self):
		client = pymongo.MongoClient("127.0.0.1", 27017)
		db = client['Denovo']
		# db.authenticate("tanxian123", "123456")
		collection = client['Denovo'][self.name]
		return collection

	def Storage(self, dic):
		return self.path.insert(dic)

	def FindByID(self, ID):
		return self.path.find_one({'ENTREZ_ID': ID})

	def FindCountByID(self, ID):
		dlist = []
		for item in self.path.find({'ENTREZ_ID': ID}):
			dlist.append(item)
		return dlist
	def GetAllGeneStruceterData(self, res):
		for item in res:
			if 'Trans_Ref' in item.keys():
				dlist = [item_item for item_item in item['Trans_Ref']]
			else:
				dlist = []
			if 'Trans_Gencode' in item.keys():
				for item_item in item['Trans_Gencode']:
					dlist.append(item_item)
		return dlist

	def RemoveDictValueColon(self, dlist):
		for item in dlist:
			for k in item:
				item[k] = item[k].replace('"', '')
		return dlist

	def UpdataByID(self, dic, key, ID):
		i = self.path.find_one({'ENTREZ_ID': ID})
		if i != None:
			if key not in i:
				lis = []
				lis.append(dic)
			else:
				if isinstance(i[key], list):
					lis = i[key]
					lis.append(dic)
				else:
					lis = []
					lis.append(dic)
			return self.path.update_one({"_id": i["_id"]}, {"$set": {key: lis}})
		else:
			print("Updata false")
class DataPretreatment(object):

	def __init__(self):
		pass

	def get_region(self, xlist):
		min_l = []
		max_l = []
		for item in xlist:
			min_l.append(min(item))
			max_l.append(max(item))
		min_value = min(min_l)
		max_value = max(max_l)
		return min_value, max_value

	def get_many_region(self, xlist, ylist, zlist):
		count_list = []
		count = []
		if len(xlist) == 0:
			for item in ylist:
				count_list.append(item)
			for item in zlist:
				count_list.append(item)
			count.append(0)
			count.append(len(ylist))
			count.append(len(zlist))
		elif len(zlist) == 0:
			for item in xlist:
				count_list.append(item)
			for item in ylist:
				count_list.append(item)
			count.append(len(xlist))
			count.append(len(ylist))
			count.append(0)
		else:
			for item in xlist:
				count_list.append(item)
			for item in ylist:
				count_list.append(item)
			for item in zlist:
				count_list.append(item)
			count.append(len(xlist))
			count.append(len(ylist))
			count.append(len(zlist))
		count_min, count_max = self.get_region(count_list)
		return [count_min, count_max], count_list, count

	# return count_list, count

	def get_all_region(self, list_3D):
		min_l = []
		max_l = []
		for item in list_3D:
			a, b, c = self.get_many_region(item[3], item[4], item[5])
			min_l.append(a[0])
			max_l.append(a[1])
		return min_l, max_l

	def mapping_x(self, x, min, max):
		return ((x - min) / (max - min) * 100 + 1)

	def mapping_xlist(self, x_list, min, max):
		'''
			根据区间边界x,y，将这个区间内二维数组映射到0-100之间
			:param list_2D: 二维list
			:param x: 区间边界，最小值
			:param y: 区间边界，最大值
			:return:  映射后的0-100之间的数组，以及边界
			'''
		a = []
		for item in x_list:
			b = []
			for item_item in item:
				b.append((item_item - min) / (max - min) * 100 + 1)
			a.append(b)
		return a

	def mapping_region(self, x_list, min_value):
		# region = end - start
		l = len(x_list)
		step = 5
		l_list = list(map(lambda x: x[0] - x[1], zip([item[1] for item in x_list], [item[0] for item in x_list])))
		flag = True
		for ttem in l_list:
			if ttem < 5:
				flag = False
		if flag == False:
			for t in range(len(l_list)):
				l_list[t] += 5
		sum = 0
		for item_l in l_list:
			sum += item_l
		scale = (100 - (l + 1) * step) / sum

		new_list = []
		i = 0
		for item_l in l_list:
			# new_list.append([start+(i+1)*step, ])
			new_sum = 0
			for ii in range(i):
				new_sum += l_list[ii]
			# new_sum = new_sum * scale
			new_list.append(
				[int(min_value + 1 + (i + 1) * step + new_sum), int(min_value + 1 + (i + 1) * step + new_sum + item_l)])
			i += 1
		return new_list
class DrawGeneStructure(object):
	def __init__(self):
		# data_handle = DataPretreatment()
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

	def gene_structure_data_deal(self, target_dlist):

		#####此处假设从数据库中取出的数据为target_list#####
		# target_df = pd.DataFrame(target_dlist)
		# gencode_df = pd.read_csv('4-16\\gencode_hg19_v27_cds_utrexon.bed',delimiter='\t', )
		target_df = pd.DataFrame(target_dlist)
		# target_df = gencode_df[gencode_df['Sym'] == 'SGIP1']  # 备选测试基因：SGIP1, CSNK2A1, SETD2, NSD2

		target_dict = target_df.to_dict(orient='records')
		strand = []
		for item in target_dict:
			strand.append(item['strand'])
		gene_sym = target_dict[0]['Sym']

		#####判断正反链#####
		strand = list(set(strand))
		assert len(strand) == 1
		if strand == ['+']:
			strand_str = '+'
		elif strand == ['-']:
			strand_str = '-'
		else:
			strand_str = '无法判断正反链！'

		##########
		records = []
		for row in target_dict:
			temp = []
			if (row['TranscriptID'] not in ['NULL', 'NaN', '']):
				TranscriptID = row['TranscriptID']
			else:
				TranscriptID = []
			if type(row['utr5_exon_region']) == str:  # isnan(row['utr5_exon_region']) == False:
				utr5_exon_region = self.str_to_list(row['utr5_exon_region'])
			else:
				utr5_exon_region = []
			if type(row['utr3_exon_region']) == str:  # isnan(row['utr3_exon_region']) == False:
				utr3_exon_region = self.str_to_list(row['utr3_exon_region'])
			else:
				utr3_exon_region = []
			if type(row['coding_exon_region']) == str:  # isnan(row['coding_exon_region']) == False:
				coding_exon_region = self.str_to_list(row['coding_exon_region'])
			else:
				coding_exon_region = []
			if type(row['utr5']) == str:
				utr5 = [int(row['utr5'].split('_')[0]), int(row['utr5'].split('_')[1])]
			else:
				utr5 = []
			if type(row['utr3']) == str:
				utr3 = [int(row['utr3'].split('_')[0]), int(row['utr3'].split('_')[1])]
			else:
				utr3 = []
			temp.append(TranscriptID)
			temp.append(utr5)
			temp.append(utr3)
			temp.append(utr5_exon_region)
			temp.append(utr3_exon_region)
			temp.append(coding_exon_region)
			records.append(temp)

		return strand_str, records, gene_sym

	def gene_structure_plot(self, strand_str, records, gene_sym=''):

		#####定义绘图的Data######
		if gene_sym=='':
			customize_title = 'Visualize Gene Structure of Transcripts ，' + strand_str+'链',
		else:
			customize_title = 'Visualize Gene[' +gene_sym +'] Structure of Transcripts ，' + strand_str+'链',
		trace = []
		data_handle = DataPretreatment()
		min_l, max_l = data_handle.get_all_region(records)
		min_value = min(min_l)
		max_value = max(max_l)
		min_list = []
		for item in min_l:
			min_list.append(data_handle.mapping_x(item, min_value, max_value))

		rec = 0
		for item in records:
			#####确定基因区间#####
			# records_num = 0
			if strand_str == '-':  # '负链，从UTR3开始！'，即方向为UTR3，coding_exon_region，UTR5
				region, count_list, count = data_handle.get_many_region(item[4], item[5], item[3])
				mapping_count_list = data_handle.mapping_xlist(count_list, min_value, max_value)
				scale_count_list = data_handle.mapping_region(mapping_count_list, min_list[rec])

				tips = item[0]
				trace_UTR3_list = []
				utr3_num = 0
				for item_UTR3 in scale_count_list[:count[0]]:
					trace_UTR3 = Scatter(
						name='UTR3',
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						x=[item_UTR3[0], item_UTR3[1]],
						y=[tips, tips],
						mode='lines',
						text='UTR3，lie in'+str(item[3][utr3_num]),
						line=dict(
							color='blue',
							# shape='spline',
							width=15
						)
					)
					trace_UTR3_list.append(trace_UTR3)
					utr3_num+=1

				trace_UTR5_list = []
				utr5_num = 0
				for item_UTR5 in scale_count_list[-count[2]:]:
					trace_UTR5 = Scatter(
						name='UTR5',
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						x=[item_UTR5[0], item_UTR5[1]],
						y=[tips, tips],
						mode='lines',
						text='UTR5，lie in'+str(item[5][utr5_num]),
						line=dict(
							color='blue',
							# shape='spline',
							width=15
						)
					)
					trace_UTR5_list.append(trace_UTR5)
					utr5_num+=1

				trace_gene = Scatter(
					visible=True,
					hoverinfo='y',
					showlegend=False,
					mode='lines',
					x=[scale_count_list[:count[0]][0][0], scale_count_list[-count[2]:][-1][1]],
					y=[tips, tips],
					# mode='line',
					# text='gene',
					line=dict(
						color='rgb(144, 144, 144)',
						# shape='spline',
						width=3,
					)
				)

				trace_coding = []
				exton_num = 0
				for item_item in scale_count_list[count[0]:-count[2]]:
					trace_coding_item = Scatter(
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						mode='lines',
						x=[item_item[0], item_item[1]],
						y=[tips, tips],
						legendgroup='coding_exon_region',
						name='coding_exon_region',
						text='coding_exon，lie in'+str(item[5][exton_num]),
						line=dict(
							color='red',
							shape='linear',
							width=20,
							simplify=True
						),
					)
					trace_coding.append(trace_coding_item)
					exton_num+=1

				for i_5 in trace_UTR5_list:
					trace.append(i_5)
				for i_3 in trace_UTR3_list:
					trace.append(i_3)
				trace.append(trace_gene)
				for ii in trace_coding:
					trace.append(ii)

			elif strand_str == '+':  # '正链，从UTR5开始！'，即方向为UTR5，coding_exon_region，UTR3

				region, count_list, count = data_handle.get_many_region(item[3], item[5], item[4])
				mapping_count_list = data_handle.mapping_xlist(count_list, min_value, max_value)
				scale_count_list = data_handle.mapping_region(mapping_count_list, min_list[rec])



				tips = item[0]
				trace_UTR5_list = []
				bh = 0
				for item_UTR5 in scale_count_list[:count[0]]:
					trace_UTR5 = Scatter(
						name='UTR5',
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						x=[item_UTR5[0], item_UTR5[1]],
						y=[tips, tips],
						mode='lines',
						text='UTR5，lie in '+str(item[3][bh]),
						line=dict(
							color='blue',
							# shape='spline',
							width=15
						)
					)
					trace_UTR5_list.append(trace_UTR5)
					bh+=1

				utr3_bh = 0
				trace_UTR3_list = []
				for item_UTR3 in scale_count_list[-count[2]:]:
					trace_UTR3 = Scatter(
						name='UTR3',
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						x=[item_UTR3[0], item_UTR3[1]],
						y=[tips, tips],
						mode='lines',
						text='UTR3，lie in '+str(item[4][utr3_bh]),
						line=dict(
							color='blue',
							# shape='spline',
							width=15
						)
					)
					trace_UTR3_list.append(trace_UTR3)
					utr3_bh+=1

				trace_gene = Scatter(
					visible=True,
					hoverinfo='y',
					showlegend=False,
					mode='lines',
					x=[scale_count_list[:count[0]][0][0], scale_count_list[-count[2]:][-1][1]],
					y=[tips, tips],
					# mode='line',
					# text='gene',
					line=dict(
						color='rgb(144, 144, 144)',
						# shape='spline',
						width=3,
					)
				)

				exton_bh = 0
				trace_coding = []
				for item_item in scale_count_list[count[0]:-count[2]]:
					j = 0
					trace_coding_item = Scatter(
						visible=True,
						hoverinfo='y+text',
						showlegend=False,
						mode='lines',
						x=[item_item[0], item_item[1]],
						y=[tips, tips],
						legendgroup='coding_exon_region',
						name='coding_exon_region',
						text='coding exton，lie in'+str(item[5][exton_bh]),
						line=dict(
							color='red',
							shape='linear',
							width=20,
							simplify=True
						),
					)
					trace_coding.append(trace_coding_item)
					exton_bh+=1
					j += 1
				# i += 1

				for i_5 in trace_UTR5_list:
					trace.append(i_5)
				for i_3 in trace_UTR3_list:
					trace.append(i_3)
				trace.append(trace_gene)
				for ii in trace_coding:
					trace.append(ii)
			rec+=1
		layouts = go.Layout(
			paper_bgcolor='rgb(249, 249, 249)',
			plot_bgcolor='rgb(249, 249, 249)',
			height=700,
			width=900,
			title='Visualize Gene Structure of Transcripts ',#，' + strand_str+'链',
			titlefont=dict(size=25),  hovermode='closest',
			xaxis=dict(
				# autorange=True,
				showgrid=False,
				zeroline=False,
				showline=False,
				showticklabels=False,
				# automargin=False,
				# separatethousands=True,
				tickformat='r',
				dtick=10,
			),
			yaxis=dict(
				title='Transcripts ID',
				titlefont=dict(
					family='Arial, sans-serif',
					size=18,
					color='lightgrey'
				),
				showticklabels=True,
				tickangle=90,
				tickfont=dict(
					family='Arial, serif',
					size=14,
					color='black'
				),
				exponentformat='e',
				showexponent='All'
			)

		)
		figs = go.Figure(data=trace, layout=layouts)
		#
		# # Take 2: extend the traces on the plot with the data in the order supplied.
		# # plot_url = py.plot(data, filename='extend plot', fileopt='extend')
		return plotly.offline.plot(figs,output_type="div",show_link=False,include_plotlyjs=False)
class Main(object):
	def __init__(self):
		pass
	def run(self, id):
		a = DataQuery("Genes")
		res = a.FindCountByID(id)
		cdlist = a.GetAllGeneStruceterData(res)
		dlist = a.RemoveDictValueColon(cdlist)
		g_d = DrawGeneStructure()
		strand_str, records, gene_name = g_d.gene_structure_data_deal(dlist)
		return g_d.gene_structure_plot(strand_str, records, gene_name)

def main():
	mainer = Main()
	mainer.run('2')
if __name__ == '__main__':
	main()
