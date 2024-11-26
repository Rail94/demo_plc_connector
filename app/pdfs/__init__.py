from flask import Blueprint


blueprint = Blueprint(
    'pdfs_blueprint',
    __name__,
    url_prefix=''
)