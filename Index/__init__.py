# -*- encoding: utf-8 -*-

from flask import Blueprint

app_Index = Blueprint("index", __name__, template_folder="templates")

# import views
from Index import views