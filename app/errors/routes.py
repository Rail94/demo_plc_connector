from flask_login import login_required
from app.errors import blueprint
from flask import render_template, request
from werkzeug.exceptions import Forbidden



@blueprint.route('/pagina_segnalazioni')
@login_required
def pagina_segnalazioni():
    return render_template('errors/errors_page.html', segment='Pagina Segnalazioni')

@blueprint.errorhandler(Forbidden)
def access_forbidden(e):
    return render_template('errors/800_login.html'), 800

@blueprint.errorhandler(404)
def not_found_error(e):
    return render_template('errors/404.html',segment = "Errore"), 404

@blueprint.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html', segment = "Errore"), 500
