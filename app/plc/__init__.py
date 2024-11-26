from flask import Blueprint


blueprint = Blueprint(
    'plc_blueprint',
    __name__,
    url_prefix=''
)