import eventlet

from app import socketio, db
from app.models import Variabili
from app.socket import blueprint
from threading import Thread
from sqlalchemy import and_

stop_event = eventlet.event.Event()

def fetch_ev():
    session = db.session()
    position_names = session.query(Variabili).filter(Variabili.nome.op('regexp')('^Posizioni_Nomi-(DX|SX)_[0-9]+$')).all()
    positions = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_Pos_[0-9]+(_DX|_SX)$'))).all()
    genPos = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_GenPos+(_DX|_SX)$'))).all()
    vent = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_Vent+(_DX|_SX)$'))).all()
    prop = session.query(Variabili).filter(Variabili.nome.op('regexp')('^Percentuale-Prop+(-DX|-SX)$')).all()
    genAn = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_GenAnaliz+(_DX|_SX)$'))).all()
    
    pos_names_bit_values = [var.valore_appoggio for var in position_names]
    pos_bit_values = [True if var.valore_appoggio == "True" else False for var in positions]
    genPos_bit_values = [True if var.valore_appoggio == "True" else False for var in genPos]
    vent_bit_values = [True if var.valore_appoggio == "True" else False for var in vent]
    prop_bit_values = [str(var.valore_appoggio) + "%" for var in prop]
    genAn_bit_values = [True if var.valore_appoggio == "True" else False for var in genAn]
    
    session.close()
    return {
        "pos_names_bit_values" : pos_names_bit_values,
        "pos_bit_values" : pos_bit_values,
        "prop_bit_values" : prop_bit_values,
        "genPos_bit_values" : genPos_bit_values,
        "vent_bit_values" : vent_bit_values,
        "genAn_bit_values" : genAn_bit_values
    }

def fetch_oxy_ev():
    session = db.session()
    
    oxy = session.query(Variabili).filter(and_(Variabili.tipo.like('REAL'),Variabili.nome.op('regexp')('^OXYMAT+(-DX|-SX)$'))).all()
    tsi = session.query(Variabili).filter(and_(Variabili.tipo.like('REAL'),Variabili.nome.op('regexp')('^OXYMAT+(-DX|-SX)$'))).all()
    evGa = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_GA+(_DX|_SX)$'))).all()
    tankGa = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_Tank_GA+(_DX|_SX)$'))).all()
    ventGenCamp = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_GenCampioni_3Vie+(_DX|_SX)$')) ).all()
    zeroNames = session.query(Variabili).filter(Variabili.nome.op('regexp')('^Nome_Simbolico_ZERO(_DX|_SX)_R$')).all()
    spanNames = session.query(Variabili).filter(Variabili.nome.op('regexp')('^Nome_Simbolico_SPAN_OXYMAT(_DX|_SX)_R$')).all()
    zero = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_ZERO+(_DX|_SX)$'))).all()
    span = session.query(Variabili).filter(and_(Variabili.nome.like('EV%'),Variabili.nome.op('regexp')('^EV_[^_]+_SPAN+(_DX|_SX)$'))).all()
    
    oxy_bit_values = [var.valore_appoggio for var in oxy]
    tsi_bit_values = [var.valore_appoggio for var in tsi]
    evGa_bit_values = [True if var.valore_appoggio == "True" else False for var in evGa]
    tankGa_bit_values = [True if var.valore_appoggio == "True" else False for var in tankGa]
    ventGenCamp_bit_values = [True if var.valore_appoggio == "True" else False for var in ventGenCamp]
    zero_names_bit_values = [var.valore_appoggio for var in zeroNames]
    span_names_bit_values = [var.valore_appoggio for var in spanNames]
    zero_bit_values = [True if var.valore_appoggio == "True" else False for var in zero]
    span_bit_values = [True if var.valore_appoggio == "True" else False for var in span]
    
    session.close()
    return {
        
        "oxy_bit_values" : oxy_bit_values,
        "tsi_bit_values" : tsi_bit_values,
        "evGa_bit_values" : evGa_bit_values,
        "tankGa_bit_values" : tankGa_bit_values,
        "ventGenCamp_bit_values" : ventGenCamp_bit_values,
        "zero_names_bit_values" : zero_names_bit_values,
        "span_names_bit_values" : span_names_bit_values,
        "zero_bit_values" : zero_bit_values,
        "span_bit_values" : span_bit_values
    }

def background_thread(app):
    with app.app_context():
        while True:
            eventlet.sleep(5)
            bit_values = fetch_ev()
            bit_values_oxy = fetch_oxy_ev()
            socketio.emit('update_bits', bit_values)
            socketio.emit('update_bits_oxy', bit_values_oxy)

@socketio.on('connect')
def handle_connect():
    bit_values = fetch_ev()
    bit_values_oxy = fetch_oxy_ev()
    socketio.emit('update_bits', bit_values)
    socketio.emit('update_bits_oxy', bit_values_oxy)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def start_background_thread(app):
    thread = Thread(target=background_thread, args=(app,))
    thread.start()
    return thread