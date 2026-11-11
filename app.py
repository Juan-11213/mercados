import os

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


def get_db():
    """Conexión a MySQL usando variables de entorno (nada de claves en el código)."""
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "bolsa_mercados"),
        connection_timeout=5,
    )


def consultar(sql, params=None):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        conn.close()


@app.errorhandler(mysql.connector.Error)
def error_db(err):
    return render_template("error.html", detalle=str(err)), 500


@app.route("/")
def index():
    totales = {}
    for tabla in ("usuarios", "empresas", "activos", "mercados", "noticias", "alertas"):
        totales[tabla] = consultar(f"SELECT COUNT(*) AS n FROM {tabla}")[0]["n"]
    return render_template("index.html", totales=totales)


@app.route("/activos")
def activos():
    filas = consultar(
        """
        SELECT a.nombre AS activo, a.simbolo, a.tipo,
               e.nombre AS empresa, e.sector,
               m.nombre AS mercado, m.pais,
               (SELECT p.precio FROM precios_historicos p
                 WHERE p.id_activo = a.id_activo
                 ORDER BY p.fecha DESC LIMIT 1) AS ultimo_precio
        FROM activos a
        LEFT JOIN empresas e ON a.id_empresa = e.id_empresa
        LEFT JOIN mercados m ON a.id_mercado = m.id_mercado
        ORDER BY a.nombre
        """
    )
    return render_template("activos.html", filas=filas)


@app.route("/precios")
def precios():
    filas = consultar(
        """
        SELECT a.nombre AS activo, p.precio, p.fecha
        FROM precios_historicos p
        INNER JOIN activos a ON p.id_activo = a.id_activo
        ORDER BY p.fecha DESC, a.nombre
        """
    )
    return render_template("precios.html", filas=filas)


@app.route("/noticias")
def noticias():
    filas = consultar(
        """
        SELECT n.titulo, n.descripcion, n.fuente, n.fecha_publicacion,
               e.nombre AS empresa
        FROM noticias n
        LEFT JOIN empresas e ON n.id_empresa = e.id_empresa
        ORDER BY n.fecha_publicacion DESC
        """
    )
    return render_template("noticias.html", filas=filas)


@app.route("/carteras")
def carteras():
    filas = consultar(
        """
        SELECT u.nombre AS usuario, c.nombre AS cartera, c.saldo_virtual,
               a.nombre AS activo, d.cantidad, d.precio_compra
        FROM carteras_virtuales c
        INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
        LEFT JOIN detalle_cartera d ON d.id_cartera = c.id_cartera
        LEFT JOIN activos a ON d.id_activo = a.id_activo
        ORDER BY u.nombre, c.nombre
        """
    )
    return render_template("carteras.html", filas=filas)


@app.route("/alertas")
def alertas():
    filas = consultar(
        """
        SELECT u.nombre AS usuario, a.nombre AS activo,
               al.precio_objetivo, al.tipo_alerta, al.estado
        FROM alertas al
        INNER JOIN usuarios u ON al.id_usuario = u.id_usuario
        INNER JOIN activos a ON al.id_activo = a.id_activo
        ORDER BY al.estado, u.nombre
        """
    )
    return render_template("alertas.html", filas=filas)


@app.route("/salud")
def salud():
    """Endpoint simple para comprobar que la app y la BD responden."""
    consultar("SELECT 1")
    return {"estado": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
