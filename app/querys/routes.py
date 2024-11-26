from app import db
from app.logiche import blueprint
from flask import flash, jsonify, redirect, url_for, request

from app.models import PLC, Marche

# -------------  C A R A T T E R I S T I C H E   P L C  ------------- #
@blueprint.route('/get-caratteristiche')
def get_caratteristiche():
    marca = Marche.query.get(request.args.get('marca_id'))
    if not marca:
        flash('Marca non trovata', 'danger')
        return redirect(url_for('plc_blueprint.plc'))
    caratteristiche = marca.caratteristiche.split('||') if marca.caratteristiche else []
    print(caratteristiche)
    return jsonify(caratteristiche=caratteristiche)


# -------------  T I P I   V A R I A B I L I  ------------- #
@blueprint.route('/get-tipi')
def get_tipi():
    plc_id = request.args.get('plc_id')
    plc = PLC.query.get(plc_id)
    if not plc:
        return jsonify({'error': 'PLC non trovato'}), 404  # Restituire un errore e uno status code appropriato
    
    # Crea una lista di dizionari contenenti le informazioni che ti servono
    tipi = [
        {'id': tipo.id, 'name': tipo.name, 'lettura': tipo.lettura, 'scrittura': tipo.scrittura}
        for tipo in plc.marca.tipi_var
    ]
    
    # Restituisce questo come oggetto JSON
    return jsonify({'tipi': tipi})
