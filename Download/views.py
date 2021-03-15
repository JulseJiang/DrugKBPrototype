# -*- encoding: utf-8 -*-

from . import app_Download
from flask import render_template

@app_Download.route('/')
def Download():
	return render_template('Download.html')