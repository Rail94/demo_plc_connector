from flask_login import login_required
from app import db
from app.plc import blueprint
from flask import flash, jsonify, redirect, render_template, url_for, request
from app.models import PLC, Marche, Tipi_Var


'''

    M A R C H E

'''

# ------------- L I S T A  M A R C H E  ------------- #
@blueprint.route('/marche', methods=['GET'])
def marche():
    lista_marche =  Marche.query.all()
    return render_template('marche/marche.html', lista_marche = lista_marche, segment = "marche")

# ------------- V I S U A L I Z Z A  M A R C A ------------- #
@blueprint.route('/visualizza-marca', methods=['GET'])
def visualizza_marca():
    marca_id = request.args.get('marca_id')
    marca = Marche.query.get(marca_id)
    if not marca:
        flash('Marca non trovata', 'danger')
        return redirect(url_for('plc_blueprint.marche'))
    caratteristiche = marca.caratteristiche.split('||') if marca.caratteristiche else []
    
    return render_template('marche/visualizza_marca.html', marca=marca, caratteristiche = caratteristiche, segment = "marche")

    
'''

    P L C

'''


# ------------- L I S T A  P L C  ------------- #
@blueprint.route('/plc', methods=['GET'])
def plc():
    lista_plc =  PLC.query.all()
    return render_template('plc/plc.html', lista_plc = lista_plc, segment = "plc")


# ------------- R E G I S T R A  P L C  ------------- #
@blueprint.route('/registra-plc', methods=['GET', 'POST'])
def registra_plc():
    if request.method == 'POST':
        
        marca_id = request.form.get('marca')
        caratteristiche = request.form.getlist('caratteristiche')  # Ottieni la lista delle caratteristiche
        for caratteristica in caratteristiche:
            caratteristica = (caratteristica).replace(" ", "_") 
        caratteristiche_str = "||".join(caratteristiche)  # Converti la lista in una stringa con "||" come separatore

        nuovo_plc = PLC(name=request.form['name'], caratteristiche = caratteristiche_str)
        
        if marca_id:
            marca_id = int(marca_id)

        if marca_id:
            marca = Marche.query.get(marca_id)
            if marca:
                nuovo_plc.marca_id = marca_id
                nuovo_plc.marca = marca  # Assign the group directly
        else:
            flash('Marca non trovata', 'danger')
            return redirect(url_for('plc_blueprint.plc'))
        db.session.add(nuovo_plc)
        db.session.commit()
        
        flash('PLC creato con successo!', 'success')
        return redirect(url_for('plc_blueprint.plc'))
    marche = Marche.query.all()
    return render_template('plc/registra_plc.html', marche = marche, segment = "plc")

# ------------- M O D I F I C A  P L C  ------------- #
@blueprint.route('/modifica-plc', methods=['GET', 'POST'])
def modifica_plc():
    if request.method == 'POST':
        plc_id = request.form.get('plc_id')
        plc = PLC.query.get(plc_id)
        caratteristiche = request.form.getlist('caratteristiche')  # Ottieni la lista delle caratteristiche
        caratteristiche_str = "||".join(caratteristiche)  # Converti la lista in una stringa con "||" come separatore

        if not plc:
            flash('PLC non trovato', 'danger')
            return redirect(url_for('plc_blueprint.plc'))
        
        # Modifica il nome del gruppo
        plc.name = request.form.get('name')
        plc.caratteristiche = caratteristiche_str
        
        # ----- C A M B I O  M A R C A ----- #
        '''
        
        ATTENZIONE! Scommentare solo se gestita correttamente
        
        
        if marca_id:
            marca_id = int(marca_id)

        if marca_id:
            marca = Marche.query.get(marca_id)
            if marca:
                plc.marca_id = marca_id
                plc.marca = marca  # Assign the group directly
        else:
            flash('Marca non trovata', 'danger')
            return redirect(url_for('plc_blueprint.plc'))
        
        '''
        db.session.commit()
        
        flash('Modifica avvenuta con successo!', 'success')
        return redirect(url_for('plc_blueprint.plc'))
        
        
    plc_id = request.args.get('plc_id')
    plc = PLC.query.get(plc_id)
    if not plc:
        flash('PLC non trovato, potrebbe essere stato cancellato', 'danger')
        return redirect(url_for('plc_blueprint.plc'))
    chiavi_caratteristiche = plc.marca.caratteristiche.split('||') if plc.marca.caratteristiche else []
    val_caratteristiche = plc.caratteristiche.split('||') if plc.caratteristiche else []
    chiavi_caratteristiche = [k.replace("_", " ") for k in chiavi_caratteristiche]

    caratteristiche = dict(zip(chiavi_caratteristiche, val_caratteristiche))
    
    return render_template('plc/modifica_plc.html', plc = plc, caratteristiche=caratteristiche, segment = "plc")
 

# ------------- E L I M I N A  P L C ------------- #


@blueprint.route('/elimina-plc', methods=['POST', 'GET'])
def elimina_plc():
    plc_id = request.args.get('plc_id')
    plc = PLC.query.get(plc_id)
    
    if not plc:
        flash('PLC non trovato', 'danger')
        return redirect(url_for('plc_blueprint.plc'))
    
    # Eliminiamo il plc
    if plc.variabili and len(plc.variabili) > 0:
        flash('PLC è ancora in uso', 'danger')
        return redirect(url_for('plc_blueprint.plc'))
    
    db.session.delete(plc)
    db.session.commit()
    
    flash('PLC eliminato con successo', 'success')
    return redirect(url_for('plc_blueprint.plc'))
