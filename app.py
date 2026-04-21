from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect('citas.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY,
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie TEXT,
            fecha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_database()

if __name__ == '__main__':
    app.run(debug=True, port=5001)