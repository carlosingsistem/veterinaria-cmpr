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

@app.route("/")
def index():
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    citas = cursor.fetchall()

    return render_template('index.html', citas=citas)

if __name__ == '__main__':
    app.run(debug=True, port=5001)