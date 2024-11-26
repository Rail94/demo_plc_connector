from flask import Blueprint


blueprint = Blueprint(
    'files_blueprint',
    __name__,
    url_prefix=''
)