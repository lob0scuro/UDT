from flask import Blueprint, render_template


second = Blueprint("second", __name__, static_folder="static", template_folder="template")

@second.route("/home")
@second.route("/")
def home():
    return "<H1>Test Page</h1"

