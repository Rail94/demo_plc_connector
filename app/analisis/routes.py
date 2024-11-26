from flask_login import login_required
from app.analisis import blueprint
from flask import render_template

@login_required
@blueprint.route('/sessione_analisi')
def sessione_analisi():
    return render_template('analisis/session_analisis.html', segment = "Sessione Analisi")
