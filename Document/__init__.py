# -*- encoding: utf-8 -*-

from flask import Blueprint

app_Document = Blueprint("document", __name__, template_folder="templates")

from Document import views