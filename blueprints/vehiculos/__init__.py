from flask import Blueprint, render_template, request, redirect, url_for,session
import sqlite3
from functools import wraps
vehiculos_bp = Blueprint('vehiculos', __name__, template_folder='templates')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_user' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def verifica():
    if 'cargo' not in session or session['cargo'] != "Administrador":
        return False
    return True

@vehiculos_bp.route("/vehiculos")
@login_required
def index():
    conn = sqlite3.connect("urban_maps.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo")
    vehiculos = cursor.fetchall()
    conn.close()
    return render_template('index_vehiculo.html',vehiculos=vehiculos)

@vehiculos_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear():
    if not verifica():
        return redirect(url_for('vehiculos.index'))
    if request.method == "POST":
        # Recupera los datos del formulario
        ci_afiliado = request.form["ci_afiliado"]
        marca = request.form['marca']
        modelo = request.form['modelo']
        color = request.form['color']
        numero_chasis = request.form['numero_chasis']
        placa = request.form['placa']
        observaciones = request.form['observaciones']
        
        # Inserta los datos en la base de datos
        conn = sqlite3.connect("urban_maps.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO vehiculo (ci_afiliado, marca, modelo, color, numero_chasis, placa, observaciones) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ci_afiliado, marca, modelo, color, numero_chasis, placa, observaciones))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return f"Error al insertar el vehículo: {e}"
        finally:
            conn.close()
        
        return redirect(url_for('vehiculos.index'))
    
    # Obtener afiliados para el formulario
    conn = sqlite3.connect("urban_maps.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT ci, nombres FROM guia")
    afiliados = cursor.fetchall()
    conn.close()
    
    return render_template("crear.html", afiliados=afiliados)


@vehiculos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    if not verifica():
        return redirect(url_for('vehiculos.index'))
    conn = sqlite3.connect("urban_maps.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Obtener datos del vehículo a editar
    cursor.execute("SELECT * FROM vehiculo WHERE id = ?", (id,))
    vehiculo = cursor.fetchone()

    # Si es POST, actualizar los datos
    if request.method == "POST":
        ci_afiliado = request.form["ci_afiliado"]
        marca = request.form['marca']
        modelo = request.form['modelo']
        color = request.form['color']
        numero_chasis = request.form['numero_chasis']
        placa = request.form['placa']
        observaciones = request.form['observaciones']
        
        try:
            cursor.execute("""
                UPDATE vehiculo 
                SET ci_afiliado = ?, marca = ?, modelo = ?, color = ?, numero_chasis = ?, placa = ?, observaciones = ?
                WHERE id = ?
            """, (ci_afiliado, marca, modelo, color, numero_chasis, placa, observaciones, id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return f"Error al actualizar el vehículo: {e}"
        finally:
            conn.close()

        return redirect(url_for('vehiculos.index'))

    # Obtener la lista de afiliados para el formulario
    cursor.execute("SELECT ci, nombres FROM guia")
    afiliados = cursor.fetchall()
    conn.close()

    return render_template("editar.html", vehiculo=vehiculo, afiliados=afiliados)


@vehiculos_bp.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    if not verifica():
        return redirect(url_for('vehiculos.index'))
    conn = sqlite3.connect("urban_maps.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehiculo WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('vehiculos.index'))

