from flask import Blueprint
from hiddifypanel.panel.database import db

# from .resources import ProductItemResource, ProductResource
from .user import *
bp = Blueprint("user2", __name__, url_prefix="/user/<secret>",template_folder="templates")


from flask import send_from_directory


def send_static(secret,path):
    return send_from_directory('static/assets', path)

def init_app(app):
    bp.add_url_rule("/", view_func=index)
    bp.add_url_rule("/<lang>", view_func=index)
    bp.add_url_rule("/clash/<meta_or_normal>/<mode>.yml", view_func=clash_config)
    bp.add_url_rule("/clash/<mode>.yml", view_func=clash_config)
    bp.add_url_rule("/clash/<meta_or_normal>/proxies.yml", view_func=clash_proxies)
    bp.add_url_rule("/clash/proxies.yml", view_func=clash_proxies)
    bp.add_url_rule("/all.txt", view_func=all_configs)
    bp.add_url_rule('/static/<path:path>',view_func=send_static)
    app.register_blueprint(bp)