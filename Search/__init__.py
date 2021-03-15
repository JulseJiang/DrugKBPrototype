# -*- encoding: utf-8 -*-

from flask import Blueprint

app_Search = Blueprint("search", __name__, template_folder="templates")

# import views
from Search import views, Gene, Mutatioin