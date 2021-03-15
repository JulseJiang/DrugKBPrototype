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

	def __init__(self, ID):
		self.ID = ID
		self.db = DBBase('ProteinExpression')

	def get_express_value_from_db(self):
		return self.db.find_one_by_one_condition("ENTREZ_ID", self.ID).get('ProteinExpressData')

	def plot(self):
		express_list = self.get_express_value_from_db()
		if express_list != None:
			x = []
			y = []
			array = []
			for item in express_list:
				x.append(item['TISSUE_NAME'])
				y.append(item['NORMALIZED_INTENSITY'])
				min = float(item['MIN_NORMALIZED_INTENSITY'])
				max = float(item['MAX_NORMALIZED_INTENSITY'])
				error = (max - min) / 2
				array.append(error)
			trace1 = go.Bar(
				x=x,
				y=y,
				# name='NSD2',
				error_y=dict(
					type='data',
					array=array,
					visible=True
				)
			)

			data = [trace1]
			layout = go.Layout(
				paper_bgcolor='rgb(249, 249, 249)',
				plot_bgcolor='rgb(249, 249, 249)',
				barmode='group',
				height=500,
				width=600,
				title='<br>Median protein expression</br>',
				# yaxis=dict(range=[0, 10]),
				# titlefont=dict(size=25), plot_bgcolor='#EFECEA',
				hovermode='closest',
				margin=go.Margin(  # x,y轴label距离图纸四周的距离
					l=70,
					r=30,
					b=100,
					t=10,
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

					showgrid=True,
					zeroline=False,
					showline=False,
					showticklabels=True,
					tickangle=20,  # x轴刻度之间距离
					# automargin=False,
					# separatethousands=True,
				), yaxis=dict(
					# range=[0,],
					autorange=True,
					title='log <sub>10</sub> normalized iBAQ intensity',
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

			fig = go.Figure(data=data, layout=layout)
			# plotly.offline.plot(fig, show_link=False)
			return plotly.offline.plot(fig, show_link=False, output_type="div",include_plotlyjs=False)
		else:
			return '<div>There is no corresponding data published yet, we will update it when such data available. </div>'

def main():
	protein_express_plot = ProteinExpressPlot("7468")
	protein_express_plot.plot()


if __name__ == '__main__':
	main()

