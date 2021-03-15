# -*- encoding: utf-8 -*-

from . import app_Browser
from flask import render_template
from Data import shortlist2
from Data import shortlist4

@app_Browser.route('/GeneSymbols/')
@app_Browser.route('/GeneSymbols/<name>')
def GeneSymbols(name):
	x = shortlist2.Letter
	return render_template('GeneSymbols.html', message=x, key=name)


@app_Browser.route('/Genesets/')
@app_Browser.route('/Genesets/<name>')
def Genesets(name):
	return render_template('Geneset.html', name=name, message=shortlist4.set)
