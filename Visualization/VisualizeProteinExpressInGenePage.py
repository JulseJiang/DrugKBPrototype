# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        pv
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-01
# @update:      2018-09-01 10:02
# @Software:    PyCharm
#-------------------------------------------------------------------------------
from Base.DBBase import DBBase
import plotly.graph_objs as go
import plotly

class ProteinExpressPlot(object):

	def __init__(self, ID, isoform="all"):
		self.ID = ID
		self.db = DBBase('ProteinExpress_Update')
		# print(isoform)
		self.isoform_list = isoform
		self.all_tissue = self.all_tissue()
		# print(self.isoform_list)

	def all_tissue(self):
		return ['adipocyte', 'adrenal gland', 'amniocyte', 'arachnoid cyst', 'ascites', 'blood', 'blood platelet', 'bone', 'bone marrow stromal cell', 'brain', 'breast', 'cardia', 'cerebral cortex', 'B-lymphocyte', 'cerebrospinal fluid', 'cerumen', 'cervical mucosa', 'colon', 'colon muscle', 'colonic epithelial cell', 'cytotoxic T-lymphocyte', 'esophagus', 'gall bladder', 'gut', 'hair follicle', 'heart', 'helper T-lymphocyte', 'ileum epithelial cell', 'kidney', 'liver', 'lung', 'lymph node', 'mesenchymal stem cell', 'milk', 'monocyte', 'myometrium', 'nasopharynx', 'natural killer cell', 'oral epithelium', 'osteosarcoma cell', 'ovary', 'pancreas', 'pancreatic islet', 'pancreatic juice', 'placenta', 'prefrontal cortex', 'prostate gland', 'proximal fluid (coronary sinus)', 'rectum', 'renal cell carcinoma cell', 'retina', 'saliva', 'salivary gland', 'seminal plasma', 'seminal vesicle', 'skin', 'spermatozoon', 'spinal cord', 'spleen', 'stomach', 'synovial fluid', 'testis', 'thyroid gland', 'tonsil', 'urinary bladder', 'urine', 'uterine cervix', 'uterus', 'vitreous humor']

	def get_express_value_from_db(self):
		result_list = []
		x_list =[]
		y_list =[]
		array_list =[]
		id_list= []
		if self.isoform_list == "all":
			for item in self.db.path.find({"Entrez_ID": self.ID}):
				if item.get('Express_Value') != {'d': {'results': []}} and '-' not in item.get('Uniprot_ID'):
					express_value = [None] * len(self.all_tissue)
					error_value = [None] * len(self.all_tissue)

					x = []
					y = []
					array =[]
					result_list.append(item.get('Express_Value').get('d').get('results'))
					# for item_tissue in self.all_tissue:
					for item_item in item.get('Express_Value').get('d').get('results'):
						for index, item_tissue in enumerate(self.all_tissue):
							if item_item['TISSUE_NAME'] == item_tissue:
								express_value[index] = item_item['NORMALIZED_INTENSITY']
								error_value[index] = (float(item_item['MAX_NORMALIZED_INTENSITY']) - float(item_item['MIN_NORMALIZED_INTENSITY']))/2
					for index, item_tissue in enumerate(self.all_tissue):
						x.append(item_tissue)
						y.append(express_value[index])
						array.append(error_value[index])
					id_list.append(item.get("Uniprot_ID"))
					x_list.append(x)
					y_list.append(y)
					array_list.append(array)
			# print(len(result_list))
			# print(result_list)
		else:
			for item in self.db.path.find({"Entrez_ID": self.ID}):
				if item.get('Express_Value') != {'d': {'results': []}}:
					x = []
					y = []
					array =[]
					# result_list.append(item.get('Express_Value').get('d').get('results'))
					for item_item in item.get('Express_Value').get('d').get('results'):
						x.append(item_item['TISSUE_NAME'])
						y.append(item_item['NORMALIZED_INTENSITY'])
						min = float(item_item['MIN_NORMALIZED_INTENSITY'])
						max = float(item_item['MAX_NORMALIZED_INTENSITY'])
						error = (max - min) / 2
						array.append(error)
					if item.get("Uniprot_ID") != None and item.get("Uniprot_ID") in self.isoform_list:
						id_list.append(item.get("Uniprot_ID"))
						x_list.append(x)
						y_list.append(y)
						array_list.append(array)
			# print(len(result_list))
			# print(result_list)
		# print(x_list)
		return x_list, y_list, array_list, id_list

	def get_weight(self, w):
		if w <= 5:
			return 200
		elif w > 5 and w <= 30:
			return w*20+300
		else:
			return w*20+300

	def plot(self):
		x_list, y_list, array_list, id_list = self.get_express_value_from_db()
		if len(x_list) == len(y_list) and len(x_list)!=0:
			trace = []
			for x_item, y_item, array_item, id_item in zip(x_list, y_list, array_list, id_list):
				for i, item in enumerate(x_item):
					if item in ["brain", 'arachnoid cyst', 'cerebral cortex', 'cerebrospinal fluid', 'prefrontal cortex', 'spinal cord']:
						x_item[i] = "<b>"+x_item[i].capitalize()+"</b>"
					else:
						x_item[i]= x_item[i].capitalize()
				trace.append(go.Bar(
					x=x_item,
					y=y_item,
					name=id_item,
					# orientation='h',
					hoverinfo='all',
					error_y=dict(
						type='data',
						array=array_item,
						visible=True
					)
				))
			layout = go.Layout(
				paper_bgcolor='rgb(249, 249, 249)',
				plot_bgcolor='rgb(249, 249, 249)',
				barmode='stack',
				height=400,
				width=1300,
				title='<br>Median protein expression</br>',
				# yaxis=dict(range=[0, 10]),
				# titlefont=dict(size=25), plot_bgcolor='#EFECEA',
				hovermode='closest',
				margin=go.Margin(  # x,y轴label距离图纸四周的距离
					l=50,
					r=20,
					b=150,
					t=40,
					pad=0
				),
				xaxis=dict(
					# autorange=True,
					# title='Diffient Brain region',
					# titlefont=dict(
					# 	family='Arial, sans-serif',
					# 	size=18,
					# 	color='lightgrey'
					# ),
					# title='log <sub>10</sub> normalized iBAQ intensit',
					titlefont=dict(
						# family='Arial, sans-serif',
						size=8,
						# color='lightgrey'
					),
					showgrid=True,
					zeroline=True,
					showline=True,
					showticklabels=True,
					tickangle=50,  # x轴刻度之间距离

					# automargin=False,
					# separatethousands=True,
				), yaxis=dict(
					title='log <sub>10</sub> normalized iBAQ intensity',
					# range=[0,],
					# weight=0.5,
					# tickmode='linear',
					# ticks='outside',
					showgrid=True,
					autorange=True,

					# gridwidth=0.5,
					showticklabels=True,
					# tickwidth=10,
					# tickangle=60,
					# tickfont=dict(
					# 	# family='Old Standard TT, serif',
					# 	# size=14,
					# 	# color='black'
					# ),
					exponentformat='e',
					showexponent='All'

				)
			)

			fig = go.Figure(data=trace, layout=layout)
			# plotly.offline.plot(fig, show_link=False)
			return plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
		else:
			return '<div> There is no corresponding data published yet, we will update it when such data available. </div>'

def main(ID):
	ID = str(ID)
	protein_express_plot = ProteinExpressPlot(ID,)
	protein_express_plot.plot()


if __name__ == '__main__':
	main("8945")
	main("7468")
	main("29072")

