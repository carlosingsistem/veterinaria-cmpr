from flask import Flask, render_template, request, redirect
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
def agenda():
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    citas = cursor.fetchall()

    return render_template('index.html', citas=citas)

@app.route('/agendar', methods=('GET', 'POST'))
def agendar():
    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        
        conn = sqlite3.connect('citas.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)
        """, (mascota, propietario, especie, fecha))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template('agendar.html')

@app.route('/modificar/<int:id>', methods=('GET', 'POST'))
def modificar(id):
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    cita = cursor.fetchone()

    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        conn.execute("""
            UPDATE pacientes SET mascota= ?, propietario=?, especie=?, fecha = ? WHERE id = ?
        """, (mascota, propietario, especie, fecha, id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template('modificar.html', cita=cita)

@app.route('/cancelar/<int:id>')
def cancelar(id):
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)