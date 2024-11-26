from flask import Blueprint


blueprint = Blueprint(
    'socket_blueprint',
    __name__,
    url_prefix=''
)

