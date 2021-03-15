# -*- encoding: utf-8 -*-

from . import app_Document
from flask import render_template

@app_Document.route('/UserGuide')
def Document():
	return render_template('Document.html')

@app_Document.route('/Instruction')
def Download():
	return render_template('Instruction.html')