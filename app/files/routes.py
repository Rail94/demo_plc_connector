import json
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required
from sqlalchemy import inspect
from app.files import blueprint
from app.models import Users
from app.forms import UploadFileForm
import os
from werkzeug.utils import secure_filename


# --- IMPORTANTE --- #
# --- Cambiare i campi del dictionary con rispettivamente 'nome_tabella_sul_db': nome_modello_corrispondente --- #

# Create a dictionary to map table names to model classes
table_model_mapping = {
    'user': Users,
    # Add more table names and corresponding model classes as needed
}

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/files')
@login_required
def files():
    file_path = os.path.join('dati/archivio')
    files = os.listdir(file_path)
    return render_template('files/files.html', files=files, segment="files")

@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('dati/archivio', filename)
            file.save(file_path)
            flash('File uploaded successfully', 'success')
            return redirect(url_for('files_blueprint.files'))
        else:
            flash('File type not allowed', 'error')
    
    return render_template('files/upload_file.html', form=form, segment="files")

@blueprint.route('/download/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join('dati/archivio', filename)
    return send_from_directory(filename=file_path, as_attachment=True)

@blueprint.route('/generate_json', methods=['GET', 'POST'])
@login_required
def generate_json():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        row_id = request.form.get('row_id')

        # Retrieve the selected model class based on the table name
        model = table_model_mapping.get(table_name)

        if model is not None:
            # Retrieve the selected row from the database
            row = model.query.filter_by(id=row_id).first()
            if row is not None:
                # Get the column names of the table
                inspector = inspect(model)
                column_names = [column.key for column in inspector.columns]

                # Create a dictionary of columns and values
                row_data = {}
                for column_name in column_names:
                    row_data[column_name] = getattr(row, column_name)

                # Generate the JSON file with indentation
                json_data = json.dumps(row_data, indent=4)

                # Save the JSON file in the specified folder
                file_path = os.path.join('file_json', f'{table_name}_row_{row_id}.json')
                with open(file_path, 'w') as file:
                    file.write(json_data)

                flash('JSON file generated successfully!', 'success')
                return redirect(url_for('files_blueprint.generate_json'))
            else:
                flash('Invalid Row!', 'error')
                return redirect(url_for('files_blueprint.generate_json'))
        else:
            flash('Invalid Table!', 'error')
            return redirect(url_for('files_blueprint.generate_json'))

    # Retrieve the available table names dynamically
    table_names = table_model_mapping.keys()

    return render_template('files/generate_json.html', table_names=table_names, segment="json")