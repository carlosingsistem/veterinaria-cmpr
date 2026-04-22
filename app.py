from flask import Flask, render_template, request, redirect
import sqlite3

# Configuración de la aplicación Flask
app = Flask(__name__)

# Inicializar la base de datos
def init_database():
    #conexion a la base de datos y creacion de la tabla y base de datos
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

# Para el listado de las citas
# La funcion renderiza la plantilla enviando la lista de citas
@app.route("/")
def agenda():
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    citas = cursor.fetchall()

    return render_template('index.html', citas=citas)

# Para agendar o crear una cita
@app.route('/agendar', methods=('GET', 'POST'))
def agendar():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        
        conn = sqlite3.connect('citas.db')
        cursor = conn.cursor()
        # Insertamos en la base de datos
        cursor.execute("""
            INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)
        """, (mascota, propietario, especie, fecha))
        conn.commit()
        conn.close()
        # redirigimos a la raiz
        return redirect("/")
    return render_template('agendar.html')

# Para la modificacion de una cita
@app.route('/modificar/<int:id>', methods=('GET', 'POST'))
def modificar(id):
    # Obtenmos los datos de la cita
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    cita = cursor.fetchone()

    if request.method == 'POST':
        #obtenemos los datos del formulario
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        # Ejecución de la actualización (UPDATE) con los nuevos valores
        conn.execute("""
            UPDATE pacientes SET mascota= ?, propietario=?, especie=?, fecha = ? WHERE id = ?
        """, (mascota, propietario, especie, fecha, id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    # Renderiza el formulario de edición con la información de la cita seleccionada
    return render_template('modificar.html', cita=cita)

# Para la cancelacion de una cita
@app.route('/cancelar/<int:id>')
def cancelar(id):
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    # Ejecuatmos la sentencia con cursor para la eliminacin de la cita
    cursor.execute("DELETE FROM pacientes WHERE id=?",(id,))
    conn.commit()
    conn.close()
    # Regresa al listado principal después de la eliminación
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)