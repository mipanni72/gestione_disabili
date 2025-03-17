from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Abilita CORS per tutti

# Configurazione database SQLite (per ora, possiamo cambiarlo in PostgreSQL sul cloud)
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print(f"📌 Database in uso: {app.config['SQLALCHEMY_DATABASE_URI']}")

# 🔍 **DEBUG: Verifica Connessione al Database**
@app.before_request
def test_db_connection():
    try:
        db.session.execute("SELECT 1")  # Query di test
        print("✅ Connessione al database OK!")
    except Exception as e:
        print(f"❌ Errore connessione database: {e}")

# 🔍 **DEBUG: Stampa i dati ricevuti prima di salvarli**
@app.route('/api/persone', methods=['POST'])
def aggiungi_persona():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Richiesta non valida, JSON mancante'}), 400

        print("📥 Dati ricevuti:", data)  # Debug dei dati ricevuti

        nuova_persona = Persona(
            nome=data.get('nome'),
            cognome=data.get('cognome'),
            numero_identificazione=data.get('numero_identificazione'),
            indirizzo=data.get('indirizzo'),
            civico=data.get('civico'),
            citta=data.get('citta'),
            numero_permesso=data.get('numero_permesso')
        )

        print("📝 Query da eseguire:", nuova_persona)  # Debug prima di salvare
       
        db.session.add(nuova_persona)
        db.session.commit()
        print("✅ Persona salvata con successo!")  # Conferma salvataggio

        return jsonify({'message': 'Persona aggiunta con successo'}), 201

    except Exception as e:
        print(f"🔥 ERRORE nel salvataggio: {e}")  # Mostra l'errore nei log
        return jsonify({'error': str(e)}), 500

# Funzione per calcolare il Codice Fiscale
def calcola_codice_fiscale(nome, cognome, data_nascita, sesso, citta_nascita):
    if not nome or not cognome or not data_nascita or not sesso or not citta_nascita:
        return None  

    codice_cognome = "".join([c for c in cognome.upper() if c.isalpha()][:3]).ljust(3, "X")
    codice_nome = "".join([c for c in nome.upper() if c.isalpha()][:3]).ljust(3, "X")
    codice_data = data_nascita.replace("-", "")
    codice_sesso = sesso[0].upper()
    codice_citta = "".join([c for c in citta_nascita.upper() if c.isalpha()][:3]).ljust(3, "X")

    codice_fiscale = f"{codice_cognome}{codice_nome}{codice_data}{codice_sesso}{codice_citta}"
    
    return codice_fiscale[:16]  # Tagliamo il codice a 16 caratteri

# Modello per l'anagrafica con tutti i campi
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, default="")
    cognome = db.Column(db.String(100), nullable=False, default="")
    numero_identificazione = db.Column(db.String(50), unique=True, nullable=False, default="")
    indirizzo = db.Column(db.String(255), nullable=True, default="")
    civico = db.Column(db.String(10), nullable=True, default="")
    citta = db.Column(db.String(100), nullable=True, default="")
    luogo_nascita = db.Column(db.String(100), nullable=True, default="")
    data_nascita = db.Column(db.String(10), nullable=True, default="")
    sesso = db.Column(db.String(1), nullable=True, default="")
    codice_fiscale = db.Column(db.String(16), nullable=True, default="")
    tipo_documento = db.Column(db.String(50), nullable=True, default="")
    numero_documento = db.Column(db.String(50), nullable=True, default="")
    data_rilascio_documento = db.Column(db.String(10), nullable=True, default="")
    citta_rilascio_documento = db.Column(db.String(100), nullable=True, default="")
    email = db.Column(db.String(100), nullable=True, default="")
    cellulare = db.Column(db.String(20), nullable=True, default="")
    cognome_delegato = db.Column(db.String(100), nullable=True, default="")
    nome_delegato = db.Column(db.String(100), nullable=True, default="")
    indirizzo_delegato = db.Column(db.String(255), nullable=True, default="")
    civico_delegato = db.Column(db.String(10), nullable=True, default="")
    citta_delegato = db.Column(db.String(100), nullable=True, default="")
    luogo_nascita_delegato = db.Column(db.String(100), nullable=True, default="")
    data_nascita_delegato = db.Column(db.String(10), nullable=True, default="")
    codice_fiscale_delegato = db.Column(db.String(16), nullable=True, default="")
    tipo_documento_delegato = db.Column(db.String(50), nullable=True, default="")
    numero_documento_delegato = db.Column(db.String(50), nullable=True, default="")
    data_rilascio_documento_delegato = db.Column(db.String(10), nullable=True, default="")
    citta_rilascio_documento_delegato = db.Column(db.String(100), nullable=True, default="")
    email_delegato = db.Column(db.String(100), nullable=True, default="")
    cellulare_delegato = db.Column(db.String(20), nullable=True, default="")
    numero_permesso = db.Column(db.String(50), nullable=True, default="")
    data_rilascio_permesso = db.Column(db.String(10), nullable=True, default="")
    data_scadenza_permesso = db.Column(db.String(10), nullable=True, default="")
    targa_1_permesso = db.Column(db.String(20), nullable=True, default="")
    targa_2_permesso = db.Column(db.String(20), nullable=True, default="")

# Inizializza il database SOLO se non esiste
with app.app_context():
    # Controlliamo se la tabella esiste prima di crearla
    from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    
    if not inspector.has_table("persona"):  # ✅ Questo è il metodo corretto!
        print("⚠️ Creazione nuovo database in corso...")
        db.create_all()
        print("✅ Database creato con successo!")
    else:
        print("✅ Database già esistente. Nessuna azione necessaria.")

@app.route('/api/persone', methods=['POST'])
def aggiungi_persona():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Richiesta non valida, JSON mancante'}), 400

        print("📥 Dati ricevuti:", data)  # 🔍 Debug dei dati ricevuti

        # Calcoliamo il codice fiscale solo se tutti i dati richiesti sono presenti
        codice_fiscale = calcola_codice_fiscale(
            data.get('nome'),
            data.get('cognome'),
            data.get('data_nascita'),
            data.get('sesso'),
            data.get('luogo_nascita')
        )

        nuova_persona = Persona(
            nome=data.get('nome'),
            cognome=data.get('cognome'),
            numero_identificazione=data.get('numero_identificazione'),
            indirizzo=data.get('indirizzo'),
            civico=data.get('civico'),
            citta=data.get('citta'),
            luogo_nascita=data.get('luogo_nascita'),
            data_nascita=data.get('data_nascita'),
            sesso=data.get('sesso'),
            email=data.get('email'),
            cellulare=data.get('cellulare'),
            codice_fiscale=codice_fiscale,  # Qui inseriamo il codice fiscale calcolato
            tipo_documento=data.get('tipo_documento'),
            numero_documento=data.get('numero_documento'),
            data_rilascio_documento=data.get('data_rilascio_documento'),
            citta_rilascio_documento=data.get('citta_rilascio_documento'),
            cognome_delegato=data.get('cognome_delegato'),
            nome_delegato=data.get('nome_delegato'),
            indirizzo_delegato=data.get('indirizzo_delegato'),
            civico_delegato=data.get('civico_delegato'),
            citta_delegato=data.get('citta_delegato'),
            luogo_nascita_delegato=data.get('luogo_nascita_delegato'),
            data_nascita_delegato=data.get('data_nascita_delegato'),
            codice_fiscale_delegato=data.get('codice_fiscale_delegato'),
            tipo_documento_delegato=data.get('tipo_documento_delegato'),
            numero_documento_delegato=data.get('numero_documento_delegato'),
            data_rilascio_documento_delegato=data.get('data_rilascio_documento_delegato'),
            citta_rilascio_documento_delegato=data.get('citta_rilascio_documento_delegato'),
            email_delegato=data.get('email_delegato'),
            cellulare_delegato=data.get('cellulare_delegato'),
            numero_permesso=data.get('numero_permesso'),
            data_rilascio_permesso=data.get('data_rilascio_permesso'),
            data_scadenza_permesso=data.get('data_scadenza_permesso'),
            targa_1_permesso=data.get('targa_1_permesso'),
            targa_2_permesso=data.get('targa_2_permesso')
        )

        db.session.add(nuova_persona)
        db.session.commit()
        print("✅ Persona salvata con successo!")  # 🔍 Debug conferma salvataggio

        return jsonify({'message': 'Persona aggiunta con successo'}), 201

    except Exception as e:
        print(f"🔥 ERRORE nel salvataggio: {e}")  # 👀 Mostra l'errore nel log
        return jsonify({'error': str(e)}), 500

# API per ottenere tutte le persone
@app.route('/api/persone', methods=['GET'])
def get_persone():
    persone = Persona.query.all()
    persone_lista = [{column.name: getattr(p, column.name) for column in Persona.__table__.columns} for p in persone]
    return jsonify(persone_lista)

# API per cercare una persona per nome o cognome
@app.route('/api/persone/ricerca', methods=['GET'])
def cerca_persone():
    query = request.args.get('q', '')
    persone = Persona.query.filter((Persona.nome.ilike(f'%{query}%')) | (Persona.cognome.ilike(f'%{query}%'))).all()
    persone_lista = [{'id': p.id, 'nome': p.nome, 'cognome': p.cognome, 'numero_identificazione': p.numero_identificazione} for p in persone]
    return jsonify(persone_lista)

# API per eliminare una persona
@app.route('/api/persone/<int:id>', methods=['DELETE'])
def elimina_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return jsonify({'error': 'Persona non trovata'}), 404
    db.session.delete(persona)
    db.session.commit()
    return jsonify({'message': 'Persona eliminata con successo'})

import os

if __name__ == "__main__":
    app.run(debug=True, port=5000)

