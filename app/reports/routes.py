from flask_login import login_required
from app.reports import blueprint
from flask import render_template, request


@login_required
@blueprint.route('/lista_report', methods=['GET'])
def lista_report():
    return render_template('reports/listaReport.html', segment = 'Lista Report')

@login_required
@blueprint.route('/report_analisi', methods=['GET'])
def report_analisi():
    return render_template('reports/report_analisi.html',segment = "Report Analisi")

@login_required
@blueprint.route('/report_oxysx', methods=['GET'])
def report_oxysx():
    selector = request.args.get('selector')
    segment='Report Oxymat '+ selector
    return render_template('reports/report_oxysx.html', selector=selector, segment = segment)

@login_required
@blueprint.route('/report_oxydx', methods=['GET'])
def report_oxydx():
    selector = request.args.get('selector')
    segment='Report Oxymat '+ selector
    return render_template('reports/report_oxydx.html', selector=selector, segment = segment)

@login_required
@blueprint.route('/report_tsisx', methods=['GET'])
def report_tsisx():
    selector = request.args.get('selector')
    segment='Report TSI '+ selector
    return render_template('reports/report_tsisx.html', selector=selector, segment = segment)

@login_required
@blueprint.route('/report_tsidx', methods=['GET'])
def report_tsidx():
    selector = request.args.get('selector')
    segment='Report TSI '+ selector
    return render_template('reports/report_tsidx.html', selector=selector, segment = segment)

