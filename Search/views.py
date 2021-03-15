# -*- encoding: utf-8 -*-

from . import app_Search
import Forms
from Base import DataStorage
from flask import render_template
from Base import compute

@app_Search.route('/Search/', methods=['GET', 'POST'])
def Search():
	
	form = Forms.SearchForm2()
	form3 = Forms.AdvancedForm2()
	form2 = Forms.AdvancedForm()
	'''
	if form2.submit2.data and form2.validate_on_submit():
		Chr = form2.Chr.data
		DNV = form2.DNV.data
		disorder = form2.disorder.data
		print(disorder)
		start = form2.start.data
		end = form2.end.data
		AIM = DataStorage.DataStorage("DNM")
		message = AIM.FindSuperD(Chr, DNV, disorder, start, end)
		return render_template('DNV.html', message=message)
		message = AIM.FindSuperD(Chr, DNV, disorder, start, end)

	if form3.submit3.data and form3.validate_on_submit():
		Chr = form3.Chr2.data
		CNV = form3.CNV.data
		disorder = form3.disorder2.data
		start = form3.start2.data
		end = form3.end2.data
		AIM = DataStorage.DataStorage("CNV")
		# print(Chr)
		# print(CNV)
		# print(disorder)
		# print(start)
		# print(end)
		message = AIM.FindSuperC(Chr, CNV, disorder, start, end)
		return render_template('CNV.html', message=message)

	if form.submit.data and form.validate_on_submit():
		name = form.name.data
		source = compute.Datafinder(name)
		message = source.FindOne()
		form.name.data = ''
		if message != None:
			return render_template('Gene.html',
								   REMOTE_HOST="static/assets-master/js",
								   message=message,
								   form=form,
								   name=name)
		else:
			return render_template('Search.html', af0=form, af=form2, af2=form3, notmatch=1)
	'''
	return render_template('Search.html', af0=form, af=form2, af2=form3)