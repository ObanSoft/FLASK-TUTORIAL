import functools # Importamos el módulo functools para usar decoradores.

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
) # Importamos las funciones necesarias de Flask.

from werkzeug.security import check_password_hash, generate_password_hash # Importamos funciones para manejar el hash de contraseñas.

from flaskr.db import traer_database # Importamos la función para obtener la conexión a la base de datos.

bp = Blueprint('autenticacion', __name__, url_prefix='/autenticacion') # Creamos un Blueprint para la autenticación.

@bp.route('/registrarse', methods=('GET', 'POST')) # Definimos la ruta para el registro de usuarios.

def registrarse(): # Vista para registrar un nuevo usuario.
    if request.method == 'POST': # Si el método de la solicitud es POST, procesamos el formulario.
        usuario = request.form['usuario'] # Obtenemos el nombre de usuario del formulario.
        contrasena = request.form['contrasena'] # Obtenemos la contraseña del formulario.
        db = traer_database()
        error = None

        if not usuario:
            error = 'Usuario requerido.' # Validamos que el nombre de usuario no esté vacío.
        
        elif not contrasena:
            error = 'Contraseña requerida.' # Validamos que la contraseña no esté vacía.
        
        if error is None:
            try:
                db.execute( # Insertamos el nuevo usuario en la base de datos.
                    "INSERT INTO usuario (usuario, contrasena) VALUES (?, ?)",
                    (usuario, generate_password_hash(contrasena)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"El usuario {usuario} ya se encuentra registrado." # Si el usuario ya existe, capturamos la excepción.
            else:
                return redirect(url_for("autenticacion.iniciar_sesion")) # Redirigimos al usuario a la página de inicio de sesión tras un registro exitoso.
        
        flash(error)

    return render_template('autenticacion/registrarse.html') # Renderizamos la plantilla de registro.