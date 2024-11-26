from flask_login import login_required
from app.calibration import blueprint
from flask import render_template, request

from app.models import Variabili

@login_required
@blueprint.route('/oxymat-sx', methods=['GET'])
def oxymat_sx():
    selector = request.args.get('selector')
    segment='Calibrazione Oxymat '+ selector
    return render_template('calibration/oxymat-sx.html', selector=selector, segment = segment,)

@login_required
@blueprint.route('/oxymat-dx', methods=['GET'])
def oxymat_dx():
    selector = request.args.get('selector')
    segment='Calibrazione Oxymat '+ selector
    non_calibrato = Variabili.query.filter_by(nome = "Errore_OXYMAT-DX_nonCALIBRATO").first()
    
    tipi_calibrazione = Variabili.query.filter(Variabili.nome.like('Calibrazione_%_DX')).all()
    attesa_report = Variabili.query.filter(Variabili.nome.like('Oxymat-DX_Genera_Report'),Variabili.w_r.like("R")).first()
    calibrazione_max_min = Variabili.query.filter(Variabili.nome.like('InCalibrazione%_DX')).all()
    
    print(tipi_calibrazione, attesa_report, calibrazione_max_min)
    
    lista_valori_tipo = []
    lista_valori_max_min = []
    lista_valori_max_min.append(attesa_report.valore_appoggio)
    
    lista_valori_tipo = [True if item.valore_appoggio == "True" else False for item in tipi_calibrazione]
    
    lista_valori_max_min.append(True if attesa_report.valore_appoggio == 'True' else False)
    lista_valori_max_min = [True if item.valore_appoggio == "True" else False for item in calibrazione_max_min]
    
    print(lista_valori_max_min, lista_valori_tipo)
    
    return render_template('calibration/oxymat-dx.html', selector=selector, segment = segment, non_calibrato = non_calibrato, lista_valori_tipo = lista_valori_tipo, lista_valori_max_min = lista_valori_max_min)

@login_required
@blueprint.route('/tsi-sx', methods=['GET'])
def tsi_sx():
    segment='Calibrazione TSI SX'
    return render_template('calibration/tsi-sx.html', segment = segment)

@login_required
@blueprint.route('/tsi-dx', methods=['GET'])
def tsi_dx():
    segment='Calibrazione TSI DX'
    return render_template('calibration/tsi-dx.html', segment = segment)
