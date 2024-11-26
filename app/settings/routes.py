from flask_login import login_required
from app.settings import blueprint
from flask import render_template

@login_required
@blueprint.route('/impostazioni_generali')
def impostazioni_generali():
    return render_template('settings/generalsettings.html', segment='Impostazioni Generali')


@login_required
@blueprint.route('/impostazioni_pagina_campione')
def impostazioni_pagina_campione():
    return render_template('settings/samplepage.html', segment='Impostazioni Campioni')

@login_required
@blueprint.route('/oxysxsettings', methods=['GET'])
def oxysxsettings():
    segment='Impostazioni Oxymat SX'
    return render_template('settings/oxysxsettings.html', segment = segment)

@login_required
@blueprint.route('/oxydxsettings', methods=['GET'])
def oxydxsettings():
    segment='Impostazioni Oxymat DX'
    return render_template('settings/oxydxsettings.html', segment = segment)

@login_required
@blueprint.route('/tsisxsettings', methods=['GET'])
def tsisxsettings():
    segment='Impostazioni TSI SX'
    return render_template('settings/tsisxsettings.html', segment = segment)

@login_required
@blueprint.route('/tsidxsettings', methods=['GET'])
def tsidxsettings():
    segment='Impostazioni TSI DX'
    return render_template('settings/tsidxsettings.html', segment = segment)
