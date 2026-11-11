# Bolsa de Mercados

Aplicación web en Flask que consulta una base de datos MySQL (`bolsa_mercados`) y muestra activos, precios históricos, noticias, carteras virtuales y alertas. Desplegada en Red Hat Developer Sandbox (OpenShift).

## Estructura

```
app.py                 Aplicación Flask (rutas y conexión a MySQL)
requirements.txt       Dependencias de Python
Dockerfile             Imagen opcional (gunicorn en el puerto 8080)
schema.sql             Tablas y datos de ejemplo
consultas_practica.sql Consultas SQL de práctica
templates/             Plantillas HTML (herencia desde base.html)
static/css/style.css   Estilos
```

## Variables de entorno

| Variable      | Descripción                          | Valor por defecto |
|---------------|--------------------------------------|-------------------|
| `DB_HOST`     | Servicio de MySQL                    | `mysql`           |
| `DB_PORT`     | Puerto de MySQL                      | `3306`            |
| `DB_USER`     | Usuario de MySQL                     | `root`            |
| `DB_PASSWORD` | Contraseña                           | (vacía)           |
| `DB_NAME`     | Nombre de la base de datos           | `bolsa_mercados`  |

## Ejecutar en local

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
mysql -u root -p < schema.sql   # crea la BD y los datos
export DB_HOST=localhost DB_USER=root DB_PASSWORD=tu_clave
python app.py                   # http://localhost:8080
```

## Rutas

`/` resumen · `/activos` · `/precios` · `/noticias` · `/carteras` · `/alertas` · `/salud`

## Despliegue en OpenShift

1. Subir el repositorio a GitHub.
2. En la consola: **+Add → Import from Git** y pegar la URL del repo (builder Python).
3. Elegir el mismo grupo de aplicación donde está MySQL y marcar **Create a route**.
4. En el Deployment, pestaña **Environment**, definir `DB_HOST`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`.
5. Cargar `schema.sql` en MySQL (con `oc rsh` al pod de MySQL o desde un cliente).
