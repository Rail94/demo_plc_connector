from flask_login import login_required
from app.admin import blueprint
from flask import render_template, request
from app.models import Users

@login_required
@blueprint.route('/utenti')
def utenti():
    utenti = Users.query.all()
    return render_template('admin/users.html', utenti = utenti, segment='Gestione Utenti')

#TEST PAGINAZIONE

#@login_required
#@blueprint.route('/utenti', defaults={'page': 0})
#@blueprint.route('/utenti/page/<int:page>')
#def utenti(page):
#    offset = page * 5
#    utenti = Users.query.all()
#    return render_template('admin/users.html', page=page, utenti = utenti, segment='Gestione Utenti')

#TEST PAGINAZIONE

@login_required
@blueprint.route('/permessi')
def permessi():
    return render_template('admin/roles.html', segment='Gestione Permessi')

@login_required
@blueprint.route('/aggiungi_utente')
def aggiungi_utente():
    return render_template('admin/add_user.html', segment='Aggiungi Utente')

@login_required
@blueprint.route('/aggiungi_ruolo')
def aggiungi_ruolo():
    return render_template('admin/add_role.html', segment='Aggiungi Ruolo')

@login_required
@blueprint.route('/modifica_utente')
def modifica_utente():
    return render_template('admin/edit_user.html', segment='Modifica Utente')

@login_required
@blueprint.route('/modifica_ruolo')
def modifica_ruolo():
    return render_template('admin/edit_role.html', segment='Modifica Ruolo')


@blueprint.route('/audit_trail')
@login_required
def audit_trail():
    return render_template('home/audit_trail.html', segment='Audit Trail')
