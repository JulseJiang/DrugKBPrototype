# -*- encoding: utf-8 -*-

from flask import Blueprint

app_Download = Blueprint("download", __name__, template_folder="templates")

from Download import views