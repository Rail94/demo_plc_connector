from flask_login import login_required
from app import db
from app.logiche import blueprint
from flask import flash, redirect, render_template, url_for, request
from app.models import Gruppi, Logiche


# ------------- L I S T A  L O G I C H E  ------------- #
@blueprint.route('/logiche', methods=['GET'])
def logiche():
    lista_logiche =  Logiche.query.all()
    return render_template('logiche/logiche.html', lista_logiche = lista_logiche, segment = "logiche")



# ------------- C R E A  L O G I C A  ------------- #
@blueprint.route('/registra-logica', methods=['GET', 'POST'])
def registra_logica():
    if request.method == 'POST':
        name = request.form['name']
        gruppo_id = request.args.get('gruppo')
        if gruppo_id:
            gruppo_id = int(gruppo_id)

        nuova_logica = Logiche(name=name, )

        if gruppo_id:
            gruppo = Gruppi.query.get(gruppo_id)
            if gruppo:
                nuova_logica.gruppo_id = gruppo_id
                nuova_logica.gruppo_variabile = gruppo  # Assign the group directly
        else:
            flash('Gruppo non trovato', 'danger')
            return redirect(url_for('logiche_blueprint.logiche'))
        db.session.add(nuova_logica)
        db.session.commit()
        
        flash('Logica registrata con successo!', 'success')
        return redirect(url_for('logiche_blueprint.logiche'))

    return render_template('logiche/registra_logica.html', gruppo=gruppo, segment="logiche")


# ------------- M O D I F I C A  L O G I C A  ------------- #
@blueprint.route('/modifica-logica', methods=['GET', 'POST'])
def modifica_logica():
    if request.method == 'POST':
        logica_name = request.form.get('name')
        logica = Logiche.query.filter_by(name = logica_name).first()
        if not logica:
            flash('Logica non trovata','danger')
            return redirect(url_for('logiche_blueprint.logiche'))


        # Modifica i campi della logica
        logica.name = logica_name
        # Se hai altri campi, come 'sincronizzata' o 'eseguita', aggiorna anche quelli

        # Modifica i gruppi associati
        gruppo_id = request.form.get('gruppi')
        if gruppo_id:
            gruppo_id = int(gruppo_id)
        if gruppo_id:
            gruppo = Gruppi.query.get(gruppo_id)
            if gruppo:
                logica.gruppo_id = gruppo_id
                logica.gruppo_variabile = gruppo  # Assign the group directly
        else:
            flash('Gruppo non trovato', 'danger')
            return redirect(url_for('logiche_blueprint.logiche'))

        db.session.commit()
        flash('Logica modificata con successo!','success')
        return redirect(url_for('logiche_blueprint.logiche'))

    logica_id = request.args.get('logica_id')
    logica = Logiche.query.get(logica_id)
    if not logica:
        flash('Logica non trovata','danger')
        return redirect(url_for('logiche_blueprint.logiche'))


    gruppi = Gruppi.query.all()
    return render_template('logiche/modifica_logiche.html', logica=logica, gruppi=gruppi, segment = "logiche")



# ------------- E L I M I N A  L O G I C A  ------------- #
@blueprint.route('/elimina-logica', methods=['POST'])
def elimina_logica():
    logica_id = request.form.get('logica_id')
    logica = Logiche.query.get(logica_id)
    if not logica:
        flash('Logica non trovata','danger')
        return redirect(url_for('logiche_blueprint.logiche'))

    # Disassocia la logica dai gruppi
    logica.gruppi = []

    # Elimina la logica dal database
    db.session.delete(logica)
    db.session.commit()

    flash('Logica eliminata con successo!','success')
    return redirect(url_for('logiche_blueprint.logiche'))
