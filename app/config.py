import os

SECRET_KEY = 'your_secret_key'

# --- IMPORTANTE --- #
# --- Cambiare la stringa di connessione con le seguenti impostazioni: --- #
# --- mysql+pymysql://"nome_utente_db":"passsword_utente_db"@"host_di_connessione":3306/"nome_db"  --- #
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://MSE:MSengineering0.@db/plc_connector_test'

SQLALCHEMY_TRACK_MODIFICATIONS = False