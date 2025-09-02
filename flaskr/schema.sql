DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identificador_autor INTEGER NOT NULL, 
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de creacion del post si no se especifica fecha y hora, se pone la hora actual
    titulo TEXT NOT NULL,
    cuerpo TEXT NOT NULL,
    FOREIGN KEY (identificador_autor) REFERENCES user (id) -- Crear relacion entre post y user un post debe tener un usuario que lo creo
);