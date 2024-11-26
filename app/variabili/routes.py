from flask_login import login_required
from app import db
from app.variabili import blueprint
from flask import flash, jsonify, redirect, render_template, url_for, request
from app.models import PLC, Gruppi, Marche, Servizi, Tipi_Var, Variabili


'''

    G R U P P I

'''


# ------------- L I S T A  G R U P P I  ------------- #
@blueprint.route('/gruppi', methods=['GET'])
def gruppi():
    lista_gruppi =  Gruppi.query.all()
    return render_template('gruppi/gruppi.html', lista_gruppi = lista_gruppi, segment = "gruppi")


# ------------- C R E A  G R U P P O  ------------- #
@blueprint.route('/crea-gruppo', methods=['GET', 'POST'])
def crea_gruppo():
    if request.method == 'POST':
        name = request.form['name']
        servizio_id = request.form.get('servizi')
        servizio = Servizi.query.get(servizio_id)
        
        if not servizio:
            flash('Servizio non trovato o inesistente', 'danger')
            return redirect(url_for('variabili_blueprint.gruppi'))
            
        
        nuovo_gruppo = Gruppi(name=name,
                                servizio_id=servizio_id,
                                servizio=servizio)
        db.session.add(nuovo_gruppo)
        db.session.commit()
        
        flash('Gruppo creato con successo!', 'success')
        return redirect(url_for('variabili_blueprint.gruppi'))
    
    servizi = Servizi.query.all()
    
    return render_template('gruppi/crea_gruppo.html', servizi=servizi, segment = "gruppi")


# ------------- M O D I F I C A  G R U P P O  ------------- #
@blueprint.route('/modifica-gruppo', methods=['GET', 'POST'])
def modifica_gruppo():
    
    servizi = Servizi.query.all()
    
    gruppo_id = request.args.get('gruppo_id')
    gruppo = Gruppi.query.get(gruppo_id)
    if not gruppo:
        flash('Gruppo non trovato, potrebbe essere stato cancellato', 'danger')
        return redirect(url_for('variabili_blueprint.gruppi'))
    
    if request.method == 'POST':

        servizio_id = request.form.get('servizi')
        servizio = Servizi.query.get(servizio_id)
        
        if not servizio:
            flash('Servizio non trovato o inesistente', 'danger')
            return redirect(url_for('variabili_blueprint.gruppi'))
        
        # Modifica il nome del gruppo ed il servizio assegnato
        gruppo.name = request.form.get('name')
        gruppo.servizio_id = servizio_id
        gruppo.servizio = servizio
        
        db.session.commit()
        
        flash('Modifica avvenuta con successo!', 'success')
        return redirect(url_for('variabili_blueprint.gruppi'))
    
    return render_template('gruppi/modifica_gruppo.html', servizi=servizi, gruppo=gruppo, segment = "gruppi")


# ------------- E L I M I N A  G R U P P O ------------- #
@blueprint.route('/elimina-gruppo', methods=['POST', 'GET'])
def elimina_gruppo():
    gruppo_id = request.args.get('gruppo_id')
    gruppo = Gruppi.query.get(gruppo_id)
    
    if not gruppo:
        flash('Gruppo non trovato', 'danger')
        return redirect(url_for('variabili_blueprint.gruppi'))
    
    # Eliminando il gruppo elimino anche tutte le variabili e logiche assegnate
    for logica in gruppo.logiche:
        db.session.delete(logica)
    
    for variabile in gruppo.variabili:
        db.session.delete(variabile)
    db.session.commit()
    
    
    # Eliminiamo il gruppo
    db.session.delete(gruppo)
    db.session.commit()
    
    flash('Gruppo eliminato con successo', 'success')
    return redirect(url_for('variabili_blueprint.gruppi'))



'''

    V A R I A B I L I

'''


# ------------- L I S T A  V A R I A B I L I  ------------- #
@blueprint.route('/variabili', methods=['GET'])
def variabili():
    lista_variabili =  Variabili.query.all()
    return render_template('variabili/variabili.html', lista_variabili = lista_variabili, segment = "variabili")



# ------------- R E G I S T R A  V A R I A B I L E  ------------- #
@blueprint.route('/registra-variabile', methods=['GET', 'POST'])
def registra_variabile():
    
    if request.method == 'POST':
        
        # SCELTA GRUPPO E/O PLC
        plc_pre_selezionato = request.form.get('plc')
        gruppo_pre_selezionato = request.form.get('gruppo')
                    
        plc_id = request.form.get('lista_plc')
        gruppo_id = request.form.get('gruppi')
        
        if not gruppo_pre_selezionato and plc_pre_selezionato:
            
            plc = PLC.query.filter_by(name = plc_pre_selezionato).first()
            
            if not Gruppi.query.get(gruppo_id) is None:
                gruppo = Gruppi.query.get(gruppo_id)
            else:
                flash('Gruppo non trovato', 'danger')
                return redirect(url_for('variabili_blueprint.variabili'))
            
        elif gruppo_pre_selezionato and not plc_pre_selezionato:
            
            gruppo = Gruppi.query.filter_by(name = gruppo_pre_selezionato).first()
            
            if not PLC.query.get(plc_id) is None:
                plc = PLC.query.get(plc_id)    
            else:
                flash('PLC non trovato', 'danger')
                return redirect(url_for('variabili_blueprint.variabili'))
        else:
            
            if not Gruppi.query.get(gruppo_id) is None:
                gruppo = Gruppi.query.get(gruppo_id)
            else:
                flash('Gruppo non trovato', 'danger')
                return redirect(url_for('variabili_blueprint.variabili'))
            
            if not PLC.query.get(plc_id) is None:
                plc = PLC.query.get(plc_id)
            else:
                flash('PLC non trovato', 'danger')
                return redirect(url_for('variabili_blueprint.variabili'))
        
        # LETTURA E SCRITTURA
        lettura = request.form.get('lettura') == 'on'
        scrittura = request.form.get('scrittura') == 'on'
        tipo = Tipi_Var.query.get(request.form.get('tipi'))
        
        if not Variabili.query.get("Read_" + request.form['name']) or not Variabili.query.get("Write_" + request.form['name']):
            if lettura:
                nuova_variabile = Variabili(name="Read_" + request.form['name'],
                                        plc_id = plc_id,
                                        plc = plc,
                                        tipo=tipo,
                                        lettura = lettura,
                                        scrittura = False,
                                        gruppo_id = gruppo_id,
                                        gruppo = gruppo)
                db.session.add(nuova_variabile)
                db.session.commit()
            if scrittura:
                nuova_variabile = Variabili(name="Write_" + request.form['name'],
                                        plc_id = plc_id,
                                        plc = plc,
                                        tipo=tipo,
                                        lettura = False,
                                        scrittura = scrittura,
                                        gruppo_id = gruppo_id,
                                        gruppo = gruppo)
                db.session.add(nuova_variabile)
                db.session.commit()
        else:
            flash('Questa variabile è già registrata', 'error')
            return redirect(url_for('variabili_blueprint.variabili'))

        
        
        flash('Variabile registrata con successo!', 'success')
        return redirect(url_for('variabili_blueprint.variabili'))
    
    lista_gruppi = Gruppi.query.all()
    lista_plc = PLC.query.all()
    
    plc_selezionato = PLC.query.get(request.args.get('plc_id'))
    gruppo_selezionato = Gruppi.query.get(request.args.get('gruppo_id'))
    
    tipi = []
    tipi_info = {}
    
    # Controllo se il PLC esiste 
    if plc_selezionato:
        tipi = plc_selezionato.marca.tipi_var
        tipi_info = {tipo.id: {'lettura': tipo.lettura, 'scrittura': tipo.scrittura} for tipo in tipi}

    return render_template('variabili/registra_variabile.html', tipi = tipi, tipi_info=tipi_info, lista_plc=lista_plc, lista_gruppi=lista_gruppi, plc_selezionato=plc_selezionato, gruppo_selezionato=gruppo_selezionato, segment="variabili")


# ------------- M O D I F I C A  V A R I A B I L E  ------------- #
@blueprint.route('/modifica-variabile', methods=['GET', 'POST'])
def modifica_variabile():
    variabile = Variabili.query.get(request.args.get('variabile_id'))
    if not variabile:
        flash('Variabile non trovata','danger')
        return redirect(url_for('variabili_blueprint.variabili'))
    if request.method == 'POST':
        
        if Variabili.query.filter_by(name = request.form.get('name')).first():
            flash('Questa variabile è già registrata, per favore scegli un altro nome','danger')
            return redirect(url_for('variabili_blueprint.variabili'))
        
        variabile.name = request.form.get('name')
        
        db.session.commit()
        flash('Variabile modificata con successo!','success')
        return redirect(url_for('variabili_blueprint.variabili'))
    
    return render_template('variabili/modifica_variabile.html', variabile=variabile, segment = "variabili")