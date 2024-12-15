from flask import Blueprint, render_template, request, redirect, url_for,session
import sqlite3
from functools import wraps
mapas_bp = Blueprint('mapas', __name__, template_folder='templates')
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
@mapas_bp.route("/mapas")
def index_maps():
    return render_template("index_mapas.html")

@mapas_bp.route("/El_Alto")
def ver_alto():
    return render_template("elAlto.html")

@mapas_bp.route("/Telefericos")
def ver_telefericos():
    return render_template("estaciones.html")

@mapas_bp.route("/rutas_centricas")
def ver_rutas_centricas():
    return render_template("rutas_centricas.html")

@mapas_bp.route("/zonas")
def ver_zonas():
    return render_template("zonas.html")


