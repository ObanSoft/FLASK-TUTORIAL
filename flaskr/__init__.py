import os  # Libreria par intracutar con el sistema operativo

from flask import Flask # Importa la clase Flask del framework Flask
from . import db # Importa el modulo db del paquete actual
from . import autenticacion # Importa el modulo auth del paquete actual


def create_app(prueba_configuracion=None): # Funcion que crea y configura la aplicacion Flask
    app =Flask(__name__, instance_relative_config=True) # Crea una instancia de la aplicacion Flask
    app.config.from_mapping(
        SECRET_KEY='dev', # Clave secreta para la aplicacion
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'), # Ruta de la base de datos SQLite
    )

    if prueba_configuracion is None: # Si no se proporciona una configuracion de prueba
        app.config.from_pyfile('config.py', silent=True)
    
    else: # Si se proporciona una configuracion de prueba
        app.config.from_mapping(prueba_configuracion)
         
    try: # Crea el directorio de instancia si no existe
        os.makedirs(app.instance_path)
    except OSError:
        pass # Si el directorio ya existe, no hace nada

    db.iniciar_database(app) # Inicializa la base de datos con la aplicacion Flask
    app.register_blueprint(autenticacion.bp) # Registra el blueprint de autenticacion


    @app.route('/9000') # Define una ruta para la aplicacion
    def hola():
        return 'HACKEADOS'

    return app # Devuelve la instancia de la aplicacion Flask