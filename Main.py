from flask import Blueprint
from flask_mail import Mail
from flask_mail import Message
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, FileField
from wtforms.validators import Required, Email
from wtforms.fields import core
from flask_wtf.file import FileField, FileAllowed, FileRequired
from time import sleep
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)
from flask import send_file, send_from_directory
from datetime import timedelta

import element
import uuid
import os
import pathlib

import numpy as np

from flask import Flask
from Index import app_Index
from Search import app_Search
from Browse import app_Browser
from Document import app_Document
from Contact import app_Contact
from Download import app_Download

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=60) 
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.126.com'  # this is email server
app.config['MAIL_PORT'] = 25  # this is the port of email server
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = False
app.config['UPLOADED_FASTAS_DEST'] = os.getcwd()
app.config['MAIL_USERNAME'] = 'sjtubmi@126.com'
# app.config['MAIL_PASSWORD'] = 'abcdefg'
app.config['MAIL_PASSWORD'] = 'sjtubmi123'  # this is email password
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['SECRET_KEY'] = 'sjtubmi230'
mail = Mail(app)
mail.init_app(app)

FASTAS = tuple('fasta fa'.split())
fastas = UploadSet('fastas', FASTAS)
configure_uploads(app, fastas)


class FastaForm(FlaskForm):
    m_fasta = TextAreaField('Input protein sequence', validators=[],
                            render_kw={'class': 'text-body', 'rows': 13, 'columns': 30,
                                       'placeholder': u"Input Sequence\ne.g. >4n6h_A\nDLEDNWETLNDNLKVIEKADNAAQVKDALTKMRAAALDAQKATPPKLEDKSPDSPEMKDFRHGFDILVGQIDDALKLANEGKVKEAQAAAEQLKTTRNAYIQKYLGSPGARSASSLALAIAITALYSAVCAVGLLGNVLVMFGIVRYTKMKTATNIYIFNLALADALATSTLPFQSAKYLMETWPFGELLaKAVLSIDYYNMFTSIFTLTMMSVDRYIAVCHPVKALDFRTPAKAKLINICIWVLASGVGVPIMVMAVTRPRDGAVVaMLQFPSPSWYWDTVTKICVFLFAFVVPILIITVCYGLMLLRLRSVRLLSGSKEKDRSLRRITRMVLVVVGAFVVCWAPIHIFVIVWTLVDIDRRDPLVVAALHLCIALGYANSSLNPVLYAFLDENFKRCFRQLCRKPCG\n"})

    file = FileField('Upload file',
                     # validators=[FileRequired(), FileAllowed(['fasta', 'fa'], 'fasta only!')]
                     validators=[FileAllowed(fastas, 'fasta only!')]
                     )
    email = StringField('Email', [Required(),
                                  Email(message=u'That\'s not a valid email address.')])
    submit = SubmitField('Submit')


# ---------------------The_First_Class_Page----------------------

app.register_blueprint(app_Index, url_prefix="")
app.register_blueprint(app_Search, url_prefix="")
app.register_blueprint(app_Browser, url_prefix="/Browse")
app.register_blueprint(app_Document, url_prefix="/Document")
app.register_blueprint(app_Contact, url_prefix="/Contact")
app.register_blueprint(app_Download, url_prefix="/Download")

# -----------------------Error Page---------------------------
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
#

# ------------------------Future-------------------------------
if __name__ == "__main__":
    app.run(threaded=True, port=66)
