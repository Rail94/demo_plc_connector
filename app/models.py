from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin

# Users and Roles association table
user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('Roles.id'), primary_key=True)
)

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Roles(db.Model):
    
    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Marche(db.Model):
    
    __tablename__ = 'Marche_HMI'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    caratteristiche = db.Column(db.String(100), nullable=False)
    
    # (Inversa) Relazione con tabella PLC
    plc = db.relationship('PLC', back_populates='marca')
    
class PLC(db.Model):
    
    __tablename__ = 'PLC_HMI'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    rack = db.Column(db.Integer, nullable=False)
    posizione = db.Column(db.Integer, nullable=False)
    # Relazione con tabella Marche
    marca_id = db.Column(db.Integer, db.ForeignKey('Marche_HMI.id'), nullable=False)
    marca = db.relationship('Marche', back_populates='plc')
    
    # (Inversa) Relazione con tabella Variabili
    variabile = db.relationship('Variabili', back_populates='plc')

class Logiche(db.Model):
    
    __tablename__ = 'Logiche'
    
    id = db.Column(db.Integer, primary_key=True)
    logica = db.Column(db.String(500), nullable=False)
    delay = db.Column(db.Integer, nullable=False)
    elapsed_time = db.Column(db.Integer, nullable=False)
    logica_ok = db.Column(db.Boolean, nullable=False, default=False)
    vars = db.Column(db.String(100), nullable=False)
    vars_values = db.Column(db.String(100), nullable=False)

    # Relazione con  tabella Gruppi
    gruppo_id = db.Column(db.Integer, db.ForeignKey('Gruppi_HMI.id'), nullable=False)
    gruppo = db.relationship('Gruppi', back_populates='logica')
    


class Variabili(db.Model):
    
    __tablename__ = 'Variabili_HMI'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    valore_appoggio = db.Column(db.String(50), nullable=False)
    w_r = db.Column(db.Boolean, nullable=False, default=False)
    tipo = db.Column(db.String(100), nullable=False)
    db_plc = db.Column(db.Integer, nullable=False)
    offset_var = db.Column(db.Integer, nullable=False)
    lunghezza = db.Column(db.String(100), nullable=False)
    bit_index = db.Column(db.Integer, nullable=False)
    eseguito = db.Column(db.Boolean, nullable=False, default=False)
    data_eseguito = db.Column(db.DateTime, nullable=False, default=False)
    sincronizzato = db.Column(db.Boolean, nullable=False, default=False)
    occupato = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relazione con  tabella Gruppi
    gruppo_id = db.Column(db.Integer, db.ForeignKey('Gruppi_HMI.id'), nullable=False)
    gruppo = db.relationship('Gruppi', back_populates='variabile')
    
    # Relazione con tabella PLC
    plc_id = db.Column(db.Integer, db.ForeignKey('PLC_HMI.id'), nullable=False)
    plc = db.relationship('PLC', back_populates='variabile')
    


class Servizi(db.Model):
    
    __tablename__ = 'Servizi'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    parametri = db.Column(db.String(500), nullable=False)
    
    gruppo_id = db.Column(db.Integer, db.ForeignKey('Gruppi_HMI.id'), nullable=False)
    gruppo = db.relationship('Gruppi', back_populates='servizio')
    

class Gruppi(db.Model):
    
    __tablename__ = 'Gruppi_HMI'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    w_r = db.Column(db.Boolean, nullable=False, default=False)

    # Relazione con  tabella Servizi
    servizio = db.relationship('Servizi', back_populates='gruppo')
    
    # (Inversa) Relazione con tabella Logiche
    logica = db.relationship('Logiche', back_populates='gruppo')

    # (Inversa) Relazione con tabella Variabili
    variabile = db.relationship('Variabili', back_populates='gruppo')
    
class Variabili_Sistema_table(db.Model):
    
    __tablename__ = 'Variabili_Sistema_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Calibrazione_Oxymat_1_R_table(db.Model):
    
    __tablename__ = 'Calibrazione_Oxymat_1_R_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Calibrazione_Oxymat_1_W_table(db.Model):
    
    __tablename__ = 'Calibrazione_Oxymat_1_W_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Start_Analisi_W_table(db.Model):
    
    __tablename__ = 'Start_Analisi_W_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Start_Analisi_R_table(db.Model):
    
    __tablename__ = 'Start_Analisi_R_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Sessione_Analisi_W_table(db.Model):
    
    __tablename__ = 'Sessione_Analisi_W_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Sessione_Analisi_R_table(db.Model):
    
    __tablename__ = 'Sessione_Analisi_R_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Gen_Report_W_table(db.Model):
    
    __tablename__ = 'Gen_Report_W_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
class Avvio_Calibrazione_W_table(db.Model):
    
    __tablename__ = 'Avvio_Calibrazione_W_table_HMI'

    id = db.Column(db.Integer, primary_key=True)
    chiavi = db.Column(db.String(100), nullable=False)
    valori = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    