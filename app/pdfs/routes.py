import os
from flask_login import login_required
from app.pdfs import blueprint
from flask import render_template, request, send_file
from weasyprint import HTML
import io

PDF_DIR = '/app/dati/archivio/pdf'  # Directory to store PDF files

@blueprint.route('/print_pdf/report_analisi', methods=['POST'])
def print_pdf_report_analisi():
    rendered_html = render_template('reports/report_analisi.html', segment = "Report Analisi")
    pdf_file = HTML(string=rendered_html).write_pdf()
    pdf_path = os.path.join(PDF_DIR, 'report_analisi.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)
    return f"PDF saved at {pdf_path}"

@blueprint.route('/print_pdf/report_oxysx', methods=['POST'])
def print_pdf_report_oxysx():
    selector = request.form.get('selector')
    segment = request.form.get('segment') 
    rendered_html = render_template('reports/report_oxysx.html' , selector=selector, segment = segment)
    pdf_file = HTML(string=rendered_html).write_pdf()
    pdf_path = os.path.join(PDF_DIR, 'report_oxysx.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)
    return f"PDF saved at {pdf_path}"

@blueprint.route('/print_pdf/report_oxydx', methods=['POST'])
def print_pdf_report_oxydx():
    selector = request.form.get('selector')
    segment = request.form.get('segment')
    rendered_html = render_template('reports/report_oxydx.html' , selector=selector, segment = segment)
    pdf_file = HTML(string=rendered_html).write_pdf()
    pdf_path = os.path.join(PDF_DIR, 'report_oxydx.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)
    return f"PDF saved at {pdf_path}"

@blueprint.route('/print_pdf/report_tsisx', methods=['POST'])
def print_pdf_report_tsisx():
    
    selector = request.form.get('selector')
    segment = request.form.get('segment')
    rendered_html = render_template('reports/report_tsisx.html' , selector=selector, segment = segment)
    pdf_file = HTML(string=rendered_html).write_pdf()
    pdf_path = os.path.join(PDF_DIR, 'report_tsisx.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)
    return f"PDF saved at {pdf_path}"

@blueprint.route('/print_pdf/report_tsidx', methods=['POST'])
def print_pdf_report_tsidx():
    selector = request.form.get('selector')
    segment = request.form.get('segment')
    rendered_html = render_template('reports/report_tsidx.html' , selector=selector, segment = segment)
    pdf_file = HTML(string=rendered_html).write_pdf()
    pdf_path = os.path.join(PDF_DIR, 'report_tsidx.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)
    return f"PDF saved at {pdf_path}"