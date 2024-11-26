from flask_login import login_required
from app.manuals import blueprint
from flask import render_template

@login_required
@blueprint.route('/test_analisi')
def test_analisi():
    return render_template('manuals/testanalisis.html')

@login_required
@blueprint.route('/movimento_elettrovalvole')
def movimento_elettrovalvole():
    return render_template('manuals/electrovalvemovement.html')
