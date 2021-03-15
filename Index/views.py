# -*- encoding: utf-8 -*-

from . import app_Index
from flask import render_template
from Index.models import Mutdraw
import Forms
from Base import compute
from Index.DNM_Pie import DNMPie
from Index.CNV_pie import CNVPie

@app_Index.route("/", methods=['GET', 'POST'])
def Index():
	
	name = None
	a = Mutdraw()
	# x=plot1.main()
	form = Forms.SearchForm()
	DNMPIE = DNMPie()
	CNVPIE = CNVPie()
	dnm_pie = DNMPIE.get_pie()
	cnv_pie = CNVPIE.get_pie()
	'''
	if form.validate_on_submit():
		name = form.name.data
		source = compute.Datafinder(name)
		message = source.FindOne()
		form.name.data = ''
		if message != None:
			return render_template('Gene.html',
								   REMOTE_HOST="../static/assets-master/js",
								   message=message,
								   form=form,
								   name=name)
		else:
			return render_template('Index.html',
								   notmatch=1,
								   dnm_pie = dnm_pie,
								   cnv_pie = cnv_pie,
								   # myechart=a.drawPie(),
								   # myechart2=a.drawPie2(),
								   REMOTE_HOST="../static/assets-master/js",
								   script_list=a.pie1.get_js_dependencies(),
								   form=form
								   # ,div=x
								   )
								   '''
	return render_template('Index.html',
						   # myechart=a.drawPie(),
						   # myechart2=a.drawPie2(),
						   dnm_pie=dnm_pie,
						   cnv_pie=cnv_pie,
						   REMOTE_HOST="../static/assets-master/js",
						   script_list=a.pie1.get_js_dependencies(),
						   form=form
						   # ,div=x
						   )
						   