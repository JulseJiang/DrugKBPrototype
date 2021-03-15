# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        Pie
# @Author:      GuoSijia
# @Purpose:
# @Created:     2018-10-28
# @update:      2018-10-28 14:14
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import chart_studio as py
import plotly.graph_objs as go
import plotly


class CNVPie(object):

	def __init__(self):
		pass

	def get_pie(self):
		fig = {
			'data': [
				{
					'labels': ["ADHD (Attention Deficit Hyperactivity Disorder)",
							   "ASD (Autism)",
							   "BD (Bipolar Disorder)",
							   "ID/DD (Intellectual Disability / Developmental Delay)",
							   "SCZ (Schizophrenia)",
							   "OCD (Obsessive-Compulsive Disorder)",
							   "TD (Tourette Disorder)",
							   "Control"],
					'values': [4, 301, 15, 60, 43, 10, 16, 69],
					'type': 'pie',
					'name': 'CNV Deletion',
					# 'marker': {'colors': ['rgb(56, 75, 126)',
					#                       'rgb(18, 36, 37)',
					#                       'rgb(34, 53, 101)',
					#                       'rgb(36, 55, 57)',
					#                       'rgb(6, 4, 4)']},
					'domain': {'x': [0, .48]},
					'hoverinfo': 'label+value+name',
					'textinfo': 'none',
					"hole": .4,
				},
				{
					'labels': ["ADHD (Attention Deficit Hyperactivity Disorder)",
							   "ASD (Autism)",
							   "BD (Bipolar Disorder)",
							   "ID/DD (Intellectual Disability / Developmental Delay)",
							   "SCZ (Schizophrenia)",
							   "OCD (Obsessive-Compulsive Disorder)",
							   "TD (Tourette Disorder)",
							   "Control"],
					'values': [5, 185, 12, 21, 23, 3, 24, 52],
					# 'marker': {'colors': ['rgb(177, 127, 38)',
					#                       'rgb(205, 152, 36)',
					#                       'rgb(99, 79, 37)',
					#                       'rgb(129, 180, 179)',
					#                       'rgb(124, 103, 37)']},
					'type': 'pie',
					'name': 'CNV Duplication',
					'domain': {'x': [.52, 1]},
					'hoverinfo': 'label+value+name',
					'textinfo': 'none',
					"hole": .4,

				},
			],
			'layout': {
				"height": 220,
				"width": 500,
				"margin": {
					"l": 1,
					"r": 1,
					"b": 1,
					"t": 38
				},
				# "legend": {
				# 	"orientation": "h"
				# },
				'title': '<b>CNV Statistics</b>',
				'showlegend': False,
				"annotations": [
					{
						"font": {
							"size": 12
						},
						"showarrow": False,
						"text": "<b>CNV<br>Deletion<br>Total:325</b>",
						"x": 0.17,
						"y": 0.49
					},
					{
						"font": {
							"size": 12
						},
						"showarrow": False,
						"text": "<b>CNV<br>Duplication<br>Total:518</b>",
						"x": 0.84,
						"y": 0.49
					},
				]
			}
		}

		# plotly.offline.plot(fig, show_link=False)
		return plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)


if __name__ == '__main__':
	pie = CNVPie()
	pie.get_pie()
