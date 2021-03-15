# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        VisualizeGtexGeneExpress
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-02
# @update:      2018-09-02 1:17
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import chart_studio
from Visualization.DBBase import DBBase
import plotly.graph_objs as go
import math


class gtex_gene_plot(object):

	def __init__(self, id):
		self.id = id
		self.db = DBBase('Gtex_Gene_AllTissue')
		self.colors = ['rgb(255,255,0)', 'rgb(31,119,180)', 'rgb(215,42,43)', 'rgb(140,140,140)', 'rgb(44,160,44)',
					   'rgb(0,0,0)',
					   'rgb(188,188,34)', 'rgb(144,238,144)',
					   'rgb(140,86,75)', 'rgb(255,127,14)', 'rgb(188,189,34)', 'rgb(255,193,193)',
					   'rgb(238,16,118)', 'rgb(0,245,255)', 'rgb(139,0,0)'
			, 'rgb(122,197,205)', 'rgb(255,218,185)', 'rgb(84,255,159)', 'rgb(154,205,50)', 'rgb(238,180,34)'
			, 'rgb(139,115,85)', 'rgb(153,50,204)', 'rgb(205,197,191)', 'rgb(131,139,131)'
			, 'rgb(255,222,173)'
			, 'rgb(0, 0,139 )', 'rgb(155, 48, 255)', 'rgb(79, 48, 205)', 'rgb(139, 102, 139)', 'rgb(139, 34, 82)',
					   'rgb(131, 139, 131)', 'rgb(139,99 ,108 )'
			, 'rgb(205, 0, 0)', 'rgb(238, 207, 161)', 'rgb(139, 134, 130)', 'rgb(139, 90, 0)', 'rgb(16, 78, 139)',
					   'rgb(139, 76, 57)'
			, 'rgb(238, 44, 44)', 'rgb(255, 20, 147)', 'rgb(255, 99, 71)', 'rgb(255, 140, 0)', 'rgb(210, 105, 30)',
					   'rgb(139, 105, 105)'
			, 'rgb(34, 139, 34)', 'rgb(124, 252, 0)', 'rgb(205, 190, 112)', 'rgb(162, 205, 90)', 'rgb(0, 139, 69)',
					   'rgb(100, 149, 237)', 'rgb(47, 79, 79)'
			, 'rgb(255, 218, 185)', 'rgb(0, 134, 139)', 'rgb(155, 205, 155)', 'rgb(205, 255, 112)',
					   'rgb(102, 205, 170)']

	def get_x_columns(self):

		x_columns = ['Adipose - Subcutaneous', 'Adipose - Visceral (Omentum)', 'Adrenal Gland', 'Artery - Aorta',
					 'Artery - Coronary', 'Artery - Tibial', 'Bladder', 'Brain - Amygdala',
					 'Brain - Anterior cingulate cortex (BA24)', 'Brain - Caudate (basal ganglia)',
					 'Brain - Cerebellar Hemisphere',
					 'Brain - Cerebellum', 'Brain - Cortex', 'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus',
					 'Brain - Hypothalamus', 'Brain - Nucleus accumbens (basal ganglia)',
					 'Brain - Putamen (basal ganglia)',
					 'Brain - Spinal cord (cervical c-1)', 'Brain - Substantia nigra','Breast - Mammary Tissue',
					 'Cells - EBV-transformed lymphocytes', 'Cells - Transformed fibroblasts', 'Cervix - Ectocervix',
					 'Cervix - Endocervix', 'Colon - Sigmoid', 'Colon - Transverse',
					 'Esophagus - Gastroesophageal Junction',
					 'Esophagus - Mucosa', 'Esophagus - Muscularis', 'Fallopian Tube', 'Heart - Atrial Appendage',
					 'Heart - Left Ventricle', 'Kidney - Cortex', 'Liver', 'Lung',
					 'Minor Salivary Gland','Muscle - Skeletal', 'Nerve - Tibial', 'Ovary', 'Pancreas',
					 'Pituitary', 'Prostate', 'Skin - Not Sun Exposed (Suprapubic)', 'Skin - Sun Exposed (Lower leg)',
					 'Small Intestine - Terminal Ileum', 'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina',
					 'Whole Blood']
		return x_columns

	def normalized(self, alist):
		result = []
		for item in alist:
			if item != 0:
				result.append(round(math.log2(float(item)+1.0), 2))
			else:
				result.append(0)
		return result

	# def get_averge(self, alist, normaliaze = False):
	#
	# 	float_alist = []
	# 	for item in alist:
	# 		float_alist.append(float(item))
	# 	result = sum(float_alist)/len(float_alist)
	# 	if normaliaze == False:
	# 		return round(result, 2)
	# 	else:
	# 		return round(math.log10(result +1), 2)
		# else:
		# 	float_alist = []
		# 	for item in alist:
		# 		float_alist.append(round(math.log2(float(item)+1.0), 2))
		# 	result = sum(float_alist)/len(float_alist)
		# return result

	def plot(self):
		y_data = []
		y_normalized_data = []
		# y_normalized_line_data = []
		# y_line_data = []
		data = self.db.find_one_by_one_condition('Entrez_id', self.id)
		if data != None:
			x_data = self.get_x_columns()
			x_temp = []
			for item in x_data:
				x_temp.append(item.split("-")[0])
			x_before = sorted(list(set(x_temp)))
			colors = []
			for item in x_data:
				# print(data[item])
				y_data.append(data[item])
				y_normalized_data.append(self.normalized(data[item]))
				# y_line_data.append(self.get_averge(data[item]))
				# y_normalized_line_data.append(self.get_averge(data[item], True))
				for index, item_item in enumerate(x_before):
					if item.startswith(item_item):
						colors.append(self.colors[index])
			traces = []
			for xd0, yd0, cls0 in zip(x_data, y_data, colors):
				# print(yd0)
				traces.append(go.Box(
					y=yd0,
					name=xd0,
					boxpoints='outliers',
					marker=dict(
						# size=2,
						color=cls0,
					),
					line=dict(width=1),
				))
			# print('----------------------')
			for xd, yd, cls in zip(x_data, y_normalized_data, colors):
				# print(yd)
				traces.append(go.Box(
					y=yd,
					name=xd,
					boxpoints='outliers',
					visible=False,
					# jitter=0.5,
					# whiskerwidth=0.2,
					# fillcolor=cls,
					marker=dict(
						# size=2,
						color=cls,
					),
					line=dict(width=1),
				))
			# traces.append(
			# 	go.Scatter(
			# 		x=x_data,
			# 		y=y_line_data,
			# 		visible=False,
			# 		text='Unnormalized'
			# ))
			# traces.append(
			# 	go.Scatter(
			# 		x=x_data,
			# 		y=y_normalized_line_data,
			# 		visible=False,
			# 		text='Normalized'
			# 	))
			visible_list_1 = [True]*len(y_data)
			visible_list_2 = [False]*len(y_data)
			# visible_list_3 = [False] * len(y_data)
			for i in range(len(y_data)):
				visible_list_1.append(False)
				visible_list_2.append(True)
				# visible_list_3.append(False)
			# for j in range(2):
			# 	visible_list_1.append(False)
			# 	visible_list_2.append(False)
			# 	visible_list_3.append(True)

			# print(visible_list_1)
			# print(visible_list_2)
			updatemenus = list([
				dict(type="buttons",
					 active=-1,
					 # direction='left',
					 pad=dict(
						 # l=500,
						 r=30,
						 # b=250,
						 t=20,
					 ),
					 buttons=list([
						 dict(label='original TPM',
							  method='update',
							  args=[{'visible': visible_list_1},
									{'title': 'TPM without normalization',
									 # 'annotations': high_annotations
									 }]),
						 dict(label='log<sub>2</sub>( TPM + 1 )',
							  method='update',
							  args=[{'visible': visible_list_2},
									{'title': 'Normalized TPM',
									 # 'annotations': low_annotations
									 }]),
						 # dict(label='Average Line',
							#   method='update',
							#   args=[{'visible': visible_list_3},
							# 		{'title': 'Normalized and Unnormalized average TPM',
							# 		 # 'annotations': low_annotations
							# 		 }])
			]))])
			layout = go.Layout(
				updatemenus=updatemenus,
				paper_bgcolor='rgb(249, 249, 249)',
				plot_bgcolor='rgb(249, 249, 249)',
				height=400,
				width=1000,
				# title='Gene Express from GTEx(Release V7)',
				hovermode='closest',
				yaxis=dict(
					autorange=True,
					showgrid=True,
					zeroline=False,
					# dtick=10,
					# title='TPM',
					titlefont=dict(
						family='Arial',
					),
				),
				xaxis=dict(
					showgrid=True,
					zeroline=False,
					showline=False,
					showticklabels=True,
					tickangle=70,  # x轴刻度之间距离
					titlefont=dict(
						family='Arial',
					)
				),
				margin=dict(
					l=20,
					r=20,
					b=230,
					t=60,
				),
				showlegend=False
			)

			fig = go.Figure(data=traces, layout=layout)
			# plotly.offline.plot(fig, show_link=False)
			return plotly.offline.plot(fig, show_link=False, output_type="div",
									   # include_plotlyjs=False
									   )
		else:
			return '<div>There is no corresponding data published yet, we will update it when such data available. </div>'


if __name__ == '__main__':
	ggp = gtex_gene_plot("29072")
	ggp.plot()