# -*- encoding: utf-8 -*-

from pyecharts import Bar, Line, Scatter, Overlap, Page
import pandas as pd
import math
import pymongo
import pyecharts

pyecharts.configure(
	jshost=None,
	echarts_template_dir=None,
	force_js_embed=None,
	output_image=None,
	global_theme=None
)


class DataStorage:

	def __init__(self, name):
		self.name = name
		self.path = self.__login()

	def __login(self):
		client = pymongo.MongoClient("127.0.0.1", 27017)
		db = client['Denovo']
		# db.authenticate("tanxian123", "123456")
		collection = client['Denovo'][self.name]
		return collection

	def FindByID(self, ID):
		x = self.path.find_one({'ENTREZ_ID': ID})
		return x



class Brain_Dic:
	def __init__(self):
		pass

	def brain_dic(self):
		brain_list = {'10': ['13', 'amygdala', '20-39Y'], '22': ['12', 'cerebellum', '12-19Y'],
					  '100': ['8', 'cortex', '0-5M'], '179': ['2', 'striatum', '8-9PCW'], '96': ['8', 'cortex', '0-5M'],
					  '158': ['14', 'cortex', '40Y'], '117': ['10', 'cortex', '1-5Y'],
					  '137': ['12', 'cortex', '12-19Y'], '113': ['10', 'cortex', '1-5Y'],
					  '53': ['4', 'cortex', '13-15PCW'], '140': ['12', 'cortex', '12-19Y'],
					  '38': ['3', 'cortex', '10-12PCW'], '70': ['6', 'cortex', '19-23PCW'],
					  '183': ['6', 'striatum', '19-23PCW'], '55': ['4', 'cortex', '13-15PCW'],
					  '24': ['14', 'cerebellum', '40Y'], '157': ['14', 'cortex', '40Y'],
					  '73': ['6', 'cortex', '19-23PCW'], '185': ['8', 'striatum', '0-5M'],
					  '126': ['11', 'cortex', '6-11Y'], '145': ['13', 'cortex', '20-39Y'],
					  '175': ['13', 'hippocampus', '20-39Y'], '74': ['6', 'cortex', '19-23PCW'],
					  '45': ['3', 'cortex', '10-12PCW'], '88': ['7', 'cortex', '24-37PCW'],
					  '7': ['10', 'amygdala', '1-5Y'], '65': ['5', 'cortex', '16-18PCW'],
					  '78': ['6', 'cortex', '19-23PCW'], '156': ['14', 'cortex', '40Y'],
					  '119': ['10', 'cortex', '1-5Y'], '104': ['9', 'cortex', '6-11M'],
					  '76': ['6', 'cortex', '19-23PCW'], '69': ['6', 'cortex', '19-23PCW'],
					  '184': ['7', 'striatum', '24-37PCW'], '60': ['5', 'cortex', '16-18PCW'],
					  '17': ['7', 'cerebellum', '24-37PCW'], '182': ['5', 'striatum', '16-18PCW'],
					  '39': ['3', 'cortex', '10-12PCW'], '85': ['7', 'cortex', '24-37PCW'],
					  '169': ['6', 'hippocampus', '19-23PCW'], '49': ['4', 'cortex', '13-15PCW'],
					  '177': ['2', 'striatum', '8-9PCW'], '148': ['13', 'cortex', '20-39Y'],
					  '18': ['8', 'cerebellum', '0-5M'], '187': ['11', 'striatum', '6-11Y'],
					  '149': ['13', 'cortex', '20-39Y'], '142': ['12', 'cortex', '12-19Y'],
					  '13': ['3', 'cerebellum', '10-12PCW'], '97': ['8', 'cortex', '0-5M'],
					  '20': ['10', 'cerebellum', '1-5Y'], '42': ['3', 'cortex', '10-12PCW'],
					  '153': ['13', 'cortex', '20-39Y'], '12': ['2', 'cerebellum', '8-9PCW'],
					  '71': ['6', 'cortex', '19-23PCW'], '56': ['4', 'cortex', '13-15PCW'],
					  '132': ['11', 'cortex', '6-11Y'], '58': ['5', 'cortex', '16-18PCW'],
					  '164': ['14', 'cortex', '40Y'], '84': ['7', 'cortex', '24-37PCW'],
					  '26': ['2', 'cortex', '8-9PCW'], '90': ['7', 'cortex', '24-37PCW'],
					  '89': ['7', 'cortex', '24-37PCW'], '116': ['10', 'cortex', '1-5Y'],
					  '87': ['7', 'cortex', '24-37PCW'], '201': ['12', 'thalamus', '12-19Y'],
					  '44': ['3', 'cortex', '10-12PCW'], '166': ['3', 'hippocampus', '10-12PCW'],
					  '8': ['11', 'amygdala', '6-11Y'], '43': ['3', 'cortex', '10-12PCW'],
					  '32': ['2', 'cortex', '8-9PCW'], '172': ['10', 'hippocampus', '1-5Y'],
					  '25': ['2', 'cortex', '8-9PCW'], '155': ['14', 'cortex', '40Y'],
					  '167': ['4', 'hippocampus', '13-15PCW'], '129': ['11', 'cortex', '6-11Y'],
					  '122': ['11', 'cortex', '6-11Y'], '178': ['2', 'striatum', '8-9PCW'],
					  '46': ['4', 'cortex', '13-15PCW'], '165': ['2', 'hippocampus', '8-9PCW'],
					  '64': ['5', 'cortex', '16-18PCW'], '1': ['3', 'amygdala', '10-12PCW'],
					  '174': ['12', 'hippocampus', '12-19Y'], '202': ['13', 'thalamus', '20-39Y'],
					  '168': ['5', 'hippocampus', '16-18PCW'], '108': ['9', 'cortex', '6-11M'],
					  '109': ['9', 'cortex', '6-11M'], '139': ['12', 'cortex', '12-19Y'],
					  '79': ['6', 'cortex', '19-23PCW'], '198': ['9', 'thalamus', '6-11M'],
					  '147': ['13', 'cortex', '20-39Y'], '86': ['7', 'cortex', '24-37PCW'],
					  '128': ['11', 'cortex', '6-11Y'], '134': ['12', 'cortex', '12-19Y'],
					  '59': ['5', 'cortex', '16-18PCW'], '72': ['6', 'cortex', '19-23PCW'],
					  '23': ['13', 'cerebellum', '20-39Y'], '127': ['11', 'cortex', '6-11Y'],
					  '195': ['6', 'thalamus', '19-23PCW'], '162': ['14', 'cortex', '40Y'],
					  '94': ['8', 'cortex', '0-5M'], '66': ['5', 'cortex', '16-18PCW'],
					  '57': ['5', 'cortex', '16-18PCW'], '37': ['3', 'cortex', '10-12PCW'],
					  '131': ['11', 'cortex', '6-11Y'], '81': ['7', 'cortex', '24-37PCW'],
					  '152': ['13', 'cortex', '20-39Y'], '159': ['14', 'cortex', '40Y'],
					  '11': ['14', 'amygdala', '40Y'], '16': ['6', 'cerebellum', '19-23PCW'],
					  '154': ['13', 'cortex', '20-39Y'], '144': ['13', 'cortex', '20-39Y'],
					  '14': ['4', 'cerebellum', '13-15PCW'], '40': ['3', 'cortex', '10-12PCW'],
					  '31': ['2', 'cortex', '8-9PCW'], '82': ['7', 'cortex', '24-37PCW'],
					  '54': ['4', 'cortex', '13-15PCW'], '123': ['11', 'cortex', '6-11Y'],
					  '136': ['12', 'cortex', '12-19Y'], '121': ['10', 'cortex', '1-5Y'],
					  '61': ['5', 'cortex', '16-18PCW'], '110': ['9', 'cortex', '6-11M'],
					  '67': ['5', 'cortex', '16-18PCW'], '146': ['13', 'cortex', '20-39Y'],
					  '91': ['7', 'cortex', '24-37PCW'], '34': ['2', 'cortex', '8-9PCW'],
					  '193': ['4', 'thalamus', '13-15PCW'], '80': ['6', 'cortex', '19-23PCW'],
					  '192': ['3', 'thalamus', '10-12PCW'], '194': ['5', 'thalamus', '16-18PCW'],
					  '99': ['8', 'cortex', '0-5M'], '190': ['14', 'striatum', '40Y'], '93': ['8', 'cortex', '0-5M'],
					  '133': ['12', 'cortex', '12-19Y'], '19': ['9', 'cerebellum', '6-11M'],
					  '150': ['13', 'cortex', '20-39Y'], '186': ['10', 'striatum', '1-5Y'],
					  '77': ['6', 'cortex', '19-23PCW'], '63': ['5', 'cortex', '16-18PCW'],
					  '107': ['9', 'cortex', '6-11M'], '114': ['10', 'cortex', '1-5Y'],
					  '200': ['11', 'thalamus', '6-11Y'], '143': ['12', 'cortex', '12-19Y'],
					  '124': ['11', 'cortex', '6-11Y'], '120': ['10', 'cortex', '1-5Y'],
					  '112': ['10', 'cortex', '1-5Y'], '203': ['14', 'thalamus', '40Y'],
					  '191': ['2', 'thalamus', '8-9PCW'], '130': ['11', 'cortex', '6-11Y'],
					  '28': ['2', 'cortex', '8-9PCW'], '196': ['7', 'thalamus', '24-37PCW'],
					  '15': ['5', 'cerebellum', '16-18PCW'], '105': ['9', 'cortex', '6-11M'],
					  '163': ['14', 'cortex', '40Y'], '138': ['12', 'cortex', '12-19Y'],
					  '125': ['11', 'cortex', '6-11Y'], '118': ['10', 'cortex', '1-5Y'],
					  '5': ['7', 'amygdala', '24-37PCW'], '173': ['11', 'hippocampus', '6-11Y'],
					  '141': ['12', 'cortex', '12-19Y'], '160': ['14', 'cortex', '40Y'],
					  '180': ['3', 'striatum', '10-12PCW'], '36': ['3', 'cortex', '10-12PCW'],
					  '30': ['2', 'cortex', '8-9PCW'], '3': ['5', 'amygdala', '16-18PCW'],
					  '151': ['13', 'cortex', '20-39Y'], '135': ['12', 'cortex', '12-19Y'],
					  '4': ['6', 'amygdala', '19-23PCW'], '68': ['5', 'cortex', '16-18PCW'],
					  '98': ['8', 'cortex', '0-5M'], '50': ['4', 'cortex', '13-15PCW'], '115': ['10', 'cortex', '1-5Y'],
					  '106': ['9', 'cortex', '6-11M'], '75': ['6', 'cortex', '19-23PCW'],
					  '176': ['14', 'hippocampus', '40Y'], '161': ['14', 'cortex', '40Y'],
					  '171': ['8', 'hippocampus', '0-5M'], '41': ['3', 'cortex', '10-12PCW'],
					  '2': ['4', 'amygdala', '13-15PCW'], '83': ['7', 'cortex', '24-37PCW'],
					  '52': ['4', 'cortex', '13-15PCW'], '27': ['2', 'cortex', '8-9PCW'],
					  '189': ['13', 'striatum', '20-39Y'], '33': ['2', 'cortex', '8-9PCW'],
					  '181': ['4', 'striatum', '13-15PCW'], '199': ['10', 'thalamus', '1-5Y'],
					  '48': ['4', 'cortex', '13-15PCW'], '21': ['11', 'cerebellum', '6-11Y'],
					  '47': ['4', 'cortex', '13-15PCW'], '95': ['8', 'cortex', '0-5M'], '6': ['8', 'amygdala', '0-5M'],
					  '111': ['10', 'cortex', '1-5Y'], '92': ['8', 'cortex', '0-5M'], '51': ['4', 'cortex', '13-15PCW'],
					  '9': ['12', 'amygdala', '12-19Y'], '29': ['2', 'cortex', '8-9PCW'],
					  '0': ['2', 'amygdala', '8-9PCW'], '103': ['9', 'cortex', '6-11M'],
					  '188': ['12', 'striatum', '12-19Y'], '197': ['8', 'thalamus', '0-5M'],
					  '170': ['7', 'hippocampus', '24-37PCW'], '62': ['5', 'cortex', '16-18PCW'],
					  '102': ['8', 'cortex', '0-5M'], '101': ['8', 'cortex', '0-5M'], '35': ['3', 'cortex', '10-12PCW']}
		return brain_list


class dict_brainSpan():
	def dict_gene2(self, id, geneName, data, brainDic):

		"""
		??????brainSpan??????
		brainSpan_data????????????????????????
		data['BrainspanX']
		"""

		brainSpan_key = brainDic.brain_dic()
		if data.get("BrainspanX") == None:
			# print("here1")
			return False, False, False, False, False
		else:
			data_brainSpan = data['BrainspanX'][0]
			# print(data_brainSpan)
			data_brainSpan.pop('ENTREZ_ID')
			a = list(data_brainSpan.keys())
			t = [int(i) for i in a]
			b = list(data_brainSpan.values())
			c = [float(i) for i in b]
			"""
			type?????????
			"""
			others_type = ['amygdala', 'cerebellum', 'hippocampus', 'thalamus']
			"""
			????????????
			"""
			max = 0

			loc = str(id)
			dictc = {loc: c}
			xxx = pd.DataFrame(dictc, index=t)
			xxx = xxx.sort_index()
			data = xxx[loc]

			for item in data:
				if item != '' and item > max:
					max = item
			max = math.log2(max + 1.0)
			"""
			??????????????????: Period index & brain region & period info
						  ==   index & type & pi 
			"""

			new_df = pd.DataFrame(brainSpan_key, index=['#Period index', 'brain region', 'period info'])
			new_df = new_df.T

			new_df[['#Period index']] = new_df[['#Period index']].apply(pd.to_numeric)
			new_df = new_df.sort_values(by=['brain region', '#Period index'])
			# print(data)

			"""
			?????????????????????????????????????????????
			"""
			list_others_data = [['' for j in range(13)] for i in range(4)]
			for i in range(len(new_df['brain region'])):
				if new_df.iloc[i, 1] in others_type:
					loc_type = others_type.index(new_df.iloc[i, 1])
					p = new_df.iloc[i, 0]
					# list_others_data[loc_type][p - 2] = data[i]
					list_others_data[loc_type][p - 2] = math.log2(data[i] + 1.0)
			"""
			others_type, list_others_data??????????????????list??????
			"""
			list_special_cortex = [[] for j in range(13)]
			list_special_striatum = [[] for j in range(13)]
			for i in range(len(new_df['brain region'])):
				if new_df.iloc[i, 1] in "cortex":
					p = new_df.iloc[i, 0]
					# list_special_cortex[p - 2].append(data[i])
					list_special_cortex[p - 2].append(math.log2(data[i] + 1.0))

				if new_df.iloc[i, 1] in "striatum":
					p = new_df.iloc[i, 0]
					# list_special_striatum[p - 2].append(data[i])
					list_special_striatum[p - 2].append(math.log2(data[i] + 1.0))

			return others_type, list_others_data, list_special_striatum, list_special_cortex, max


class data_plot(object):
	'''
	?????????????????????????????????
	'''

	def __init__(self):
		pass

	def LineAndBox_plot(self, id, geneName, list_name_mouse, list_values_mouse, others_type, list_others_data,
						list_special_striatum, list_special_cortex, max):

		grid = Page()
		if others_type != 0:
			"""
			????????????

			"""
			overlap = Overlap()
			line_special = Line()
				# title="\tSpatio-temporal Human Developmental Brain Expression (BrainSpan)",
				# 				title_pos="left")
			i = 0
			es = Scatter(geneName)
			attr = ['Early fetal\n8-9PCW', 'Early fetal\n10-12PCW', 'Early mid-fetal\n13PCW-15PCW',
					'Early mid-fetal\n16PCW-18PCW', \
					'Late mid-fetal\n19PCW-23PCW', 'Late fetal\n24PCW-37PCW',
					'Neonatal and early infancy\n0M(birth)-5M', \
					'Late infancy\n6M-11M', 'Early childhood\n1Y-5Y', 'Middle and late childhood\n6Y-11Y', \
					'Adolescence\n12Y-19Y', 'Young adulthood\n20Y-39Y', 'Middle adulthood\n40Y']

			"""
			?????????????????????????????????
			"""
			"""
			1.?????? ???2.???????????????3.???smooth
			"""
			"""
			1-1 striatum
			"""
			list_linshi_striatum_ave = [0 for i in range(13)]
			list_linshi_striatum_num = [0 for i in range(13)]
			for i in range(13):
				if list_special_striatum[i] != []:
					for item in list_special_striatum[i]:
						list_linshi_striatum_ave[i] += item
						list_linshi_striatum_num[i] += 1
				if list_special_striatum[i] == []:
					list_linshi_striatum_ave[i] = ''
			for i in range(13):
				if list_linshi_striatum_ave[i] != '':
					list_linshi_striatum_ave[i] = list_linshi_striatum_ave[i] / list_linshi_striatum_num[i]
			line_special.add("striatum", attr, list_linshi_striatum_ave, yaxis_max=math.ceil(max), is_smooth=True,
							 xaxis_interval=0, xaxis_type="category",
							 xaxis_rotate=-30, xaxis_label_textsize=9, legend_selectedmode=False
							 , legend_pos="top", legend_orient="vertical")

			"""
			1-2 cortex
			"""
			list_linshi_cortex_ave = [0 for i in range(13)]
			list_linshi_cortex_num = [0 for i in range(13)]
			for i in range(13):
				if list_special_cortex[i] != []:
					for item in list_special_cortex[i]:
						list_linshi_cortex_ave[i] += item
						list_linshi_cortex_num[i] += 1
				if list_special_cortex[i] == []:
					list_linshi_cortex_ave[i] = ''
			for i in range(13):
				if list_linshi_cortex_ave[i] != '':
					list_linshi_cortex_ave[i] = list_linshi_cortex_ave[i] / list_linshi_cortex_num[i]

			line_special.add("cortex", attr, list_linshi_cortex_ave, yaxis_max=math.ceil(max), is_smooth=True,
							 xaxis_interval=0, xaxis_type="category",
							 xaxis_rotate=-30, xaxis_label_textsize=9,
							 legend_selectedmode=False, yaxis_name='LOG2(RPKM+1)', yaxis_name_pos='middle'
							 , legend_pos="10%", legend_orient="horizontal")
			overlap.add(line_special)

			"""
			?????????list
			"""
			max_length_striatum = 0
			for item in list_special_striatum:
				if len(item) >= max_length_striatum:
					max_length_striatum = len(item)
			for i in range(13):
				if len(list_special_striatum[i]) < max_length_striatum:
					for j in range(max_length_striatum - len(list_special_striatum[i])):
						list_special_striatum[i].append('')
			max_length_cortex = 0
			for item in list_special_cortex:
				if len(item) >= max_length_cortex:
					max_length_cortex = len(item)

			for i in range(13):
				if len(list_special_cortex[i]) < max_length_cortex:
					for j in range(max_length_cortex - len(list_special_cortex[i])):
						list_special_cortex[i].append('')

			"""
			?????????
			"""
			"""
			striatum
			"""
			for i in range(max_length_striatum):
				list_linshi_striatum = []
				for j in range(13):
					list_linshi_striatum.append(list_special_striatum[j][i])
				# print(list_linshi_striatum)
				es.add("striatum", attr, list_linshi_striatum, xaxis_type="category", xaxis_rotate=-30,
					   xaxis_interval=0,
					   legend_selectedmode=False, yaxis_max=math.ceil(max), symbol_size=3,
					   is_legend_show=False, xaxis_label_textsize=9
					   , legend_pos="right", legend_orient="vertical")

			"""
			cortex
			"""
			for i in range(max_length_cortex):
				list_linshi_cortex = []
				for j in range(13):
					list_linshi_cortex.append(list_special_cortex[j][i])
				# print(list_linshi_cortex)
				es.add("cortex", attr, list_linshi_cortex, xaxis_type="category", xaxis_rotate=-30, xaxis_interval=0,
					   legend_selectedmode=False, yaxis_max=max, symbol_size=3,
					   is_legend_show=False, xaxis_label_textsize=9, legend_pos="right", legend_orient="vertical")
			overlap.add(es)

			"""
			???????????????
			"""
			k = 0
			for item in others_type:
				line = Line()
				line.add(str(item), attr, list_others_data[k], is_smooth=True, is_symbol_show=False, xaxis_interval=0,
						 legend_selectedmode=False, xaxis_type="category", yaxis_max=max, xaxis_rotate=-30,
						 xaxis_label_textsize=9
						 , legend_pos="right", legend_orient="vertical")
				overlap.add(line)
				k += 1
			grid.add(overlap)

		# grid.render()
		try:
			return grid.render_embed()
		except:
			return '<div><p>There is no corresponding data published yet,we will update it when such data available.</p></div>'


class Main:
	def __init__(self):
		pass

	def run(self, id):
		brainSpan = dict_brainSpan()
		draw = data_plot()
		"""
		******************************????????????**********************************************
		"""

		f = DataStorage("JR")
		data = f.FindByID(str(id))
		geneName = data['Symbol']

		"""
		???????????????
		*****************"cortex" & "hippocampus"??????****************
		data_people_*???????????????list_name3 ??????????????????list_avg ???????????? ??????????????????list?????????
		*******************???????????????1???list_name3    2???list_avg*************************
		"""


		"""
		?????????????????????
		"""
		brainDic = Brain_Dic()

		others_type, list_others_data, list_special_striatum, list_special_cortex, max = brainSpan.dict_gene2(id=id,
																											  geneName=geneName,
																											  data=data,
																											  brainDic=brainDic)

		if others_type == False and list_others_data == False and list_special_striatum == False and list_special_cortex ==False and max == False:
			# print("here2")
			return '<div><p>There is no corresponding data published yet, we will update it when such data available. </p></div>'
		else:
			"""
			??????????????? 
			*********************"barreslab"??????************************
			x?????????????????????pop????????????????????????????????????str--->float???
			*******************???????????????1???list_name_mouse    2???list_values_mouse*************************
			"""

			if 'barreslab' in data.keys():
				x = data['barreslab'][0]
				x.pop('ENTREZ_ID')
				list_name_mouse = list(x.keys())
				list_values_mouse = list(x.values())
				# print("afsgdfg", list_values_mouse)
				list_values_mouse = [math.log2(float(i) + 1.0) for i in list_values_mouse]
			else:
				list_name_mouse = 0
				list_values_mouse = 0

			"""
			?????? ??????0??????????????????????????????????????????????????????
			"""
			return draw.LineAndBox_plot(id, geneName, list_name_mouse, list_values_mouse, others_type, list_others_data,
										list_special_striatum, list_special_cortex, max)


def main(ID):
	mainer = Main()
	# 996
	ID = str(ID)
	# print(mainer.run(ID))
	return mainer.run(ID)

if __name__ == '__main__':
    main("720")
