import sqlite3
import click
from flask import current_app, g


def traer_database(): #Trae una conexion a la base de datos, creando una nueva si es necesario
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def cerrar_database(e=None): #Cierra la conexion a la base de datos si existe
    db = g.pop("db", None)
    if db is not None:
        db.close()


def iniciar_database(app): #Inicializa la base de datos con la aplicacion Flask
    # Registrar que siempre se cierre la DB al final de cada request
    app.teardown_appcontext(cerrar_database)
    # Registrar el comando de inicialización en la CLI
    app.cli.add_command(iniciar_database_command)


@click.command("iniciar-base-datos") # Define un comando de linea de comandos llamado "iniciar-base-datos"
def iniciar_database_command():
    """Borra los datos existentes y crea nuevas tablas."""
    db = traer_database()
    with current_app.open_resource("schema.sql") as f: # Abre el archivo schema.sql
        db.executescript(f.read().decode("utf8")) # Ejecuta el script SQL para crear las tablas
    click.echo("Base de datos inicializada.") 
