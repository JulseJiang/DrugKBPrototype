# -*- encoding: utf-8 -*-

from flask import Blueprint

app_Contact = Blueprint("contact", __name__, template_folder="templates")

from Contact import views