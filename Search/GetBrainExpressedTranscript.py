# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        GetBrainExpressedTranscript
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-07
# @update:      2018-09-07 7:46
# @Software:    PyCharm
#-------------------------------------------------------------------------------
from Base.DBBase import DBBase
import plotly.graph_objs as go
import plotly
import math
import Visualization.VisualizePartTranscriptOneDNM as VPTOM

class GetBrainExpressTranscript(object):


	def __init__(self, ID, transcript):
		self.ID = ID
		self.db = DBBase('Gtex_Trans_AllTissue_Pledged')
		for index, item in enumerate(transcript):
			transcript[index] = item.split(".")[0]
		self.transcript_list = transcript
		# print(self.transcript_list)

	def get_express_value_from_db(self):
		return self.db.find_count_by_one_condition("Entrez_id", self.ID)


	def get_columns(self):
		columns = ['Adipose - Subcutaneous', 'Adipose - Visceral (Omentum)', 'Adrenal Gland', 'Artery - Aorta',
				   'Artery - Coronary', 'Artery - Tibial', 'Bladder', 'Brain - Amygdala',
				   'Brain - Anterior cingulate cortex (BA24)', 'Brain - Caudate (basal ganglia)',
				   'Brain - Cerebellar Hemisphere', 'Brain - Cerebellum', 'Brain - Cortex',
				   'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus', 'Brain - Hypothalamus',
				   'Brain - Nucleus accumbens (basal ganglia)', 'Brain - Putamen (basal ganglia)',
				   'Brain - Spinal cord (cervical c-1)', 'Brain - Substantia nigra', 'Breast - Mammary Tissue',
				   'Cells - EBV-transformed lymphocytes', 'Cells - Transformed fibroblasts', 'Cervix - Ectocervix',
				   'Cervix - Endocervix', 'Colon - Sigmoid', 'Colon - Transverse',
				   'Esophagus - Gastroesophageal Junction', 'Esophagus - Mucosa', 'Esophagus - Muscularis',
				   'Fallopian Tube', 'Heart - Atrial Appendage', 'Heart - Left Ventricle', 'Kidney - Cortex',
				   'Liver',
				   'Lung', 'Minor Salivary Gland', 'Muscle - Skeletal', 'Nerve - Tibial', 'Ovary', 'Pancreas',
				   'Pituitary', 'Prostate', 'Skin - Not Sun Exposed (Suprapubic)', 'Skin - Sun Exposed (Lower leg)',
				   'Small Intestine - Terminal Ileum', 'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina',
				   'Whole Blood']
		return columns

	def get_brain_columns(self):
		columns = ['Brain - Amygdala', 'Brain - Anterior cingulate cortex (BA24)',
				   'Brain - Caudate (basal ganglia)',
				   'Brain - Cerebellar Hemisphere', 'Brain - Cerebellum', 'Brain - Cortex',
				   'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus', 'Brain - Hypothalamus',
				   'Brain - Nucleus accumbens (basal ganglia)', 'Brain - Putamen (basal ganglia)',
				   'Brain - Spinal cord (cervical c-1)', 'Brain - Substantia nigra']
		return columns

	def l2(self, x):
		"""
		对输入的x取log
		:param x:
		:return:
		"""
		if x != 0:
			return math.log2(x + 1)
		else:
			return 0

	def r2(self, x):
		"""
		对输入的x取小数点后两位小数的方法
		:param x:
		:return:
		"""
		return round(x, 2)

	def average(self, num_list):
		num_list = [float(item) for item in num_list]
		return self.r2(self.l2(float(sum(num_list)) / len(num_list)))

	def data_handling(self):
		express_list = self.get_express_value_from_db()
		express_average = []
		final_transcript = []
		if len(express_list) >= 1:  # 取出了多于等于一条转录本
			for item_trans in express_list:
				list_avg = [item_trans.get("transcript_id")]
				for item_colunms in self.get_columns():
					if item_trans.get(item_colunms) != None:
						list_avg.append(self.r2(self.l2(item_trans.get(item_colunms))))
					else:
						list_avg.append(None)
				temp_flag = 0
				for item_list_avg in list_avg[8:21]:  # 脑组织表达的列为8-21列
					if item_list_avg >= 1:
						temp_flag = 1
				if temp_flag == 1 and list_avg[0].split(".")[0] in self.transcript_list:
					# if list_avg[0].split(".")[0] in self.transcript_list:
					express_average.append(list_avg)
					final_transcript.append(list_avg[0])
		else:
			express_average = []
		return final_transcript, express_average

class BrainImpactExpress(object):

	def __init__(self, express_average):
		self.express_average = express_average

	def get_columns(self):
		columns = ['Adipose - Subcutaneous', 'Adipose - Visceral (Omentum)', 'Adrenal Gland', 'Artery - Aorta',
				   'Artery - Coronary', 'Artery - Tibial', 'Bladder', 'Brain - Amygdala',
				   'Brain - Anterior cingulate cortex (BA24)', 'Brain - Caudate (basal ganglia)',
				   'Brain - Cerebellar Hemisphere', 'Brain - Cerebellum', 'Brain - Cortex',
				   'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus', 'Brain - Hypothalamus',
				   'Brain - Nucleus accumbens (basal ganglia)', 'Brain - Putamen (basal ganglia)',
				   'Brain - Spinal cord (cervical c-1)', 'Brain - Substantia nigra', 'Breast - Mammary Tissue',
				   'Cells - EBV-transformed lymphocytes', 'Cells - Transformed fibroblasts', 'Cervix - Ectocervix',
				   'Cervix - Endocervix', 'Colon - Sigmoid', 'Colon - Transverse',
				   'Esophagus - Gastroesophageal Junction', 'Esophagus - Mucosa', 'Esophagus - Muscularis',
				   'Fallopian Tube', 'Heart - Atrial Appendage', 'Heart - Left Ventricle', 'Kidney - Cortex',
				   'Liver',
				   'Lung', 'Minor Salivary Gland', 'Muscle - Skeletal', 'Nerve - Tibial', 'Ovary', 'Pancreas',
				   'Pituitary', 'Prostate', 'Skin - Not Sun Exposed (Suprapubic)', 'Skin - Sun Exposed (Lower leg)',
				   'Small Intestine - Terminal Ileum', 'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina',
				   'Whole Blood']
		return columns

	def plot(self):
		express_average = self.express_average
		if express_average != []:
			trace = []
			x_columns = self.get_columns()
			for item in express_average:
				trace.append(
					go.Scatter(
						x=x_columns,
						y=item[1:-1],
						hoverinfo='all',
						# mode="line",
						name=item[0],
						ycalendar=180,
						# line=dict(shape='spline'),
						hoverlabel=dict(namelength=-1)
					)
				)
			layouts = go.Layout(
				# paper_bgcolor='rgb(249, 249, 249)',
				# plot_bgcolor='rgb(249, 249, 249)',
				height=400,
				width=1200,
				hovermode='closest',
				margin=go.Margin(  # x,y轴label距离图纸四周的距离
					l=50,
					r=100,
					b=150,
					t=10,
					pad=0
				),
				xaxis=dict(
					showgrid=True,
					zeroline=False,
					showline=False,
					showticklabels=True,
					tickangle=90,  # x轴刻度之间距离
				),
				yaxis=dict(
					autorange=True,
					title='log <sub>2</sub> (TPM+1)',
					titlefont=dict(
						family='Arial, sans-serif',
						size=18,
						color='lightgrey'
					),
					showticklabels=True,
					tickangle=90,
					tickfont=dict(
						family='Old Standard TT, serif',
						size=14,
						color='black'
					),
					exponentformat='e',
					showexponent='All'
				)
			)
			figs = go.Figure(data=trace, layout=layouts)
			# plotly.offline.plot(figs, show_link=False)
			return plotly.offline.plot(figs, show_link=False, output_type="div")
		else:
			return '<div>There is no corresponding data published yet, we will update it when such data available. </div>'

class TranscriptPlot(object):

	def __init__(self, ID, mutation, transcript=[]):
		self.transcript = transcript
		self.gtex_transcript_express_plot = GetBrainExpressTranscript(ID, transcript)
		self.ID = ID
		self.mutation = mutation
		# print(transcript)
		# self.transcript = transcript

	def run(self):
		transcript, express_avg = self.gtex_transcript_express_plot.data_handling()
		# for index, item in enumerate(transcript):
		# 	transcript[index] = item.split(".")[0]
		BIE = BrainImpactExpress(express_avg)
		express_pic = BIE.plot()

		# nm_map_enst_db = DBBase("RefSeq_Mapping_Enst")
		# for item in transcript:
		# 	if nm_map_enst_db.find_one_by_one_condition("Enst_id", item.split(".")[0]) != None:
		# 		transcript.append(nm_map_enst_db.find_one_by_one_condition("Enst_id", item.split(".")[0]).get("NM_id"))
		# final_transcript = []
		# for item in transcript:
		# 	if item in self.transcript:
		# 		final_transcript.append(item)
		plot_run = VPTOM.PlotRun(transcript, self.mutation)
		transcript_mutation_pic = plot_run.run(self.ID)
		return transcript_mutation_pic, express_pic

def main():
	TranscriptPlot_demo = TranscriptPlot("57680", "gene=57680,location=coding-dnm,position=21899618,chr=14", ['ENST00000399982.2', 'ENST00000557364.1', 'ENST00000553622.1'])
	TranscriptPlot_demo.run()


if __name__ == '__main__':
	main()
