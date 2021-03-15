# -*- encoding: utf-8 -*-
from flask import Blueprint

app_Browser = Blueprint("browser", __name__, template_folder="templates")

from Browse import views