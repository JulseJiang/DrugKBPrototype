# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# @file:        Mutatioin
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-09-24
# @update:      2018-09-24 22:33
# @Software:    PyCharm
#-------------------------------------------------------------------------------
from . import app_Search
import Forms
from Base import compute
from flask import render_template, request, redirect, url_for
import json
from flask import jsonify
from Search.MutationQuery import MutationQuery
from Search.Convert_Enst_to_Isoform import GetIsoformAndEnst
from Visualization import VisualiazeOneDnmOnAllTranscript, VisualizeGtexTranscriptExprss
from Visualization import VisualizeProteinExpress_old
from Visualization.VisualizeGtexTranscriptExprss import GtexTranscriptExpressPlot
from Search.GetBrainExpressedTranscript import TranscriptPlot
import Visualization.VisualizeProteinExpress as VAPE
import Search.MutationImpactTranscript as MIT
import Visualization.VisualizePartTranscriptOneDNM as VPTOM
import Visualization.VisualizeProteinImpactBrainExpress as VBPE
from Search.MutationScore import MutationScore

@app_Search.route('/Mutations/')
@app_Search.route('/Mutations/<name>')
def Mutations(name):
	source = compute.Datafinder(name)
	message = source.FindOne()
	# for item in message:
	# 	print(item)
	if source.is_type(name) == "symbol":
		return render_template('MutationResults.html', message=message )

	elif source.is_type(name) == "ID":
		mutation_score = MutationScore(message)
		mutation_score_list = mutation_score.get_score()
		return render_template('MutationResults.html',
							   message=message, mutation_score_list = mutation_score_list, entrez_id=name)


# @app_Search.route('/getselect', methods=['POST'])
# def getselect():  #在这里获取的后台post过来的参数
# 	data = request.get_data()
# 	data_dict = json.loads(data.decode("utf-8"))
# 	if data_dict.get('location') == 'cnv':
# 		datas = 'gene=' + str(data_dict['Gene']) + ',location=' + str(data_dict.get('location')) \
# 				+ ',start=' + str(data_dict.get('start')) + ',end=' + str(data_dict.get('end'))
# 	else:
# 		datas = 'gene='+str(data_dict['Gene'])+',location='+str(data_dict.get('location'))\
# 				+',position='+str(data_dict['Position'])+',chr='+str(data_dict['chr'])
# 	# print("从前端接收到data!  "+ datas)
# 	return redirect(url_for('search.MutationDetails', datas=datas))
# ii = 0
@app_Search.route('/MutationDetails/<datas>', methods=['GET', 'POST'])
def MutationDetails(datas):

	name = datas.split(",")[0].split("=")[1]
	source = compute.Datafinder(name)
	mrna_form = Forms.MutationsMrnaForm()
	protein_form = Forms.MutationProteinForm()
	mutation_query = MutationQuery(datas)
	select_mutation = mutation_query.get_mutation()
	if source.is_type(name) == "ID":
		get_uniprot_ensmbl = GetIsoformAndEnst(name)
		# print(ensmbel_list)
		try:
			plot_run = VisualiazeOneDnmOnAllTranscript.PlotRun(datas)
			ID = str(name)
			mrna_mutation_pic = plot_run.run(ID)  # plot_run.run("7468")
		except:
			mrna_mutation_pic = None
		try:
			gtex_transcript_express_plot = GtexTranscriptExpressPlot(name, "all")
			mrna_express_pic = gtex_transcript_express_plot.plot()
		except:
			mrna_express_pic = None
		try:
			protein_express_plot = VAPE.ProteinExpressPlot(name, "all")
			protein_express_pic = protein_express_plot.plot()
			# print(ii)
			# ii+=1
		except:
			protein_express_pic = None
			# print("Error!")
		try:
			ensmbel_list = get_uniprot_ensmbl.get_isoform_and_enst()
		except:
			ensmbel_list = None

		if mrna_form.mrna_submit.data and mrna_form.validate_on_submit():
			if mrna_form.mrna_radio.data == "m1":
				try:
					plot_run = VisualiazeOneDnmOnAllTranscript.PlotRun(datas)
					ID = str(name)
					mrna_mutation_pic = plot_run.run(ID)  # plot_run.run("7468")
				except:
					mrna_mutation_pic = None
				# mrna_express_pic = None
				try:
					gtex_transcript_express_plot = GtexTranscriptExpressPlot(name, "all")
					mrna_express_pic = gtex_transcript_express_plot.plot()
				except:
					mrna_express_pic = None
			elif mrna_form.mrna_radio.data == "m2":
				try:
					mutation_impact_transcript = MIT.MutationTrancript(name, datas)
					# print(mutation_impact_transcript.get_mutation_impact_transcript())
					plot_run = VPTOM.PlotRun(mutation_impact_transcript.get_mutation_impact_transcript(), datas)
					ID = str(name)
					mrna_mutation_pic = plot_run.run(ID)  # plot_run.run("7468")
				except:
					mrna_mutation_pic = "<div>Sorry, the drawing program may have encountered abnormal data!</div>"
				# try:
				# 	gtex_transcript_express_plot = GtexTranscriptExpressPlot(name, "all")
				# 	mrna_express_pic = gtex_transcript_express_plot.plot()
				# except:
				mrna_express_pic = None
			elif mrna_form.mrna_radio.data == "m3":
				# try:
				# 	plot_run = VisualiazeOneDnmOnAllTranscript.PlotRun(datas)
				# 	ID = str(name)
				# 	mrna_mutation_pic = plot_run.run(ID)  # plot_run.run("7468")
				# except:
				# 	mrna_mutation_pic = None
				mrna_mutation_pic = None
				try:
					gtex_transcript_express_plot = GtexTranscriptExpressPlot(name, "all", 1)
					mrna_express_pic = gtex_transcript_express_plot.plot()
				except:
					mrna_express_pic = None
			elif mrna_form.mrna_radio.data == "m4":
				try:
					mutation_impact_transcript = MIT.MutationTrancript(name, datas)
					# print("------------")
					# print(mutation_impact_transcript.get_mutation_impact_transcript())
					TranscriptPlot_demo = TranscriptPlot(str(name), datas, mutation_impact_transcript.get_mutation_impact_transcript())
					mrna_mutation_pic, mrna_express_pic = TranscriptPlot_demo.run()
				except:
					mrna_mutation_pic = None
					mrna_express_pic = None
		if protein_form.protein_submit.data and protein_form.validate_on_submit():
			if protein_form.protein_radio.data == "p1":
				try:
					protein_express_plot = VAPE.ProteinExpressPlot(name)
					protein_express_pic = protein_express_plot.plot()
				except:
					protein_express_pic = None
				try:
					ensmbel_list = get_uniprot_ensmbl.get_isoform_and_enst()
				except:
					ensmbel_list = None
			elif protein_form.protein_radio.data == "p2":
				# try:
				# 	protein_express_plot = VAPE.ProteinExpressPlot(name)
				# 	protein_express_pic = protein_express_plot.plot()
				# except:
				# 	protein_express_pic = None
				protein_express_pic = None
				try:
					ensmbel_list = get_uniprot_ensmbl.get_isoform_and_enst()
					mutation_impact_transcript = MIT.MutationTrancript(name, datas)
					ensmbel_trans = mutation_impact_transcript.get_mutation_impact_transcript()
					for index, item in enumerate(ensmbel_trans):
						ensmbel_trans[index] = item.split(".")[0]
					final_ensmbel_list = []
					if ensmbel_list != None and ensmbel_list != []:
						for item in ensmbel_list:
							if item[0] in ensmbel_trans:
								final_ensmbel_list.append(item)
						ensmbel_list = final_ensmbel_list
					else:
						ensmbel_list = []
				except:
					ensmbel_list = None
				# print(ensmbel_list)
			elif protein_form.protein_radio.data == "p3":
				try:
					protein_express_plot = VBPE.ProteinExpressPlot(name)
					protein_express_pic = protein_express_plot.plot()
				except:
					protein_express_pic = None
				ensmbel_list = None
				# try:
				# 	ensmbel_list = get_uniprot_ensmbl.get_isoform_and_enst()
				# except:
				# 	ensmbel_list = None
			elif protein_form.protein_radio.data == "p4":
				try:
					impacted_isoform = MIT.MutationTrancript(name, datas)
					impacted_isoform_list = impacted_isoform.get_mutation_impact_isoforms()
					# print(impacted_isoform_list)
					protein_express_plot = VBPE.ProteinExpressPlot(name, impacted_isoform_list)
					protein_express_plot1 = VBPE.ProteinExpressPlot(name, impacted_isoform_list)
					_, _, _, id_list = protein_express_plot1.get_express_value_from_db()

					protein_express_pic = protein_express_plot.plot()
				except:
					protein_express_pic = None
				try:
					impacted_trans = MIT.MutationTrancript(name, datas)
					impact_trans_list = impacted_trans.get_mutation_impact_transcript()
					impact_trans_list = [item.split(".")[0] for item in impact_trans_list]
					# print(impact_trans_list)
					# print(id_list)
					ensmbel_list = get_uniprot_ensmbl.get_isoform_and_enst()
					final_ensmbel_list = []
					if ensmbel_list != None and ensmbel_list != []:
						for item in ensmbel_list:
							# print(item)
							if item[0] in impact_trans_list and item[3] in id_list:
								final_ensmbel_list.append(item)
						ensmbel_list = final_ensmbel_list
					else:
						ensmbel_list = []
				except:
					ensmbel_list = None

		# print(datas)  # 后台选中的单选框结果，这就是传过来的那个参数
		return render_template('MutationDetail.html',datas=datas, mrna_form=mrna_form, protein_form=protein_form,
							   mrna_mutation_pic=mrna_mutation_pic, mrna_express_pic=mrna_express_pic,
							    protein_express_pic=protein_express_pic,
							   select_mutation=select_mutation, ensmbel_list = ensmbel_list)
		# return redirect(url_for())
