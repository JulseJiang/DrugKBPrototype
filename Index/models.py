# -*- encoding: utf-8 -*-
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Graph

class Mutdraw():

	def __init__(self):
		self.attr = ["ASD", "SCZ", "BPD", "DD", "DEE", "EE", "ID", "OCD", "TS", "CHD", "control"]
		self.v1 = [173712, 1038, 69, 8336, 288, 580, 1432, 26, 441, 1900, 51093]
		self.attr2 = ["ASD", "SCZ", "BPD", "ID", "control"]
		self.v2 = [486, 66, 25, 81, 121]
		self.attr3 = ["ASD", "SCZ", "BPD", "MDD", "ADHD"]
		self.v3 = [292, 641, 84, 36, 35]
		self.pie1 = Pie("DNM",
						width=500,
						height=300,
						title_pos="center",
						title_top="bottom")
		self.pie2 = Pie("CNV",
						width=500,
						height=300,
						title_pos="center",
						title_top="bottom")
		self.pie1.add("",
					  self.attr,
					  self.v1,
					  legend_pos="left",
					  legend_text_size=8,
					  is_toolbox_show=False)
		self.pie2.add("",
					  self.attr2,
					  self.v2,
					  legend_pos="left",
					  legend_text_size=8,
					  is_toolbox_show=False)
		self.nodes = [{"name": "x"}, {"name": "y"}, {"name": "z"}]
		self.links = [{"source": "x", "target": "y"}, {"source": "x", "target": "z"}]
		self.graph = Graph("Graph", "PPI")
		self.graph.add("Pt", self.nodes, self.links)

	def drawPie(self):
		return self.pie1.render_embed()

	def drawPie2(self):
		return self.pie2.render_embed()

	def drawGraph(self):
		return self.graph.render_embed()