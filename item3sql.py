# app.py

# ------------------------------
# 1. Importar librerías necesarias
# ------------------------------
from flask import Flask, request, render_template_string
import sqlite3
import hashlib

# ------------------------------
# 2. Crear la app Flask (sitio web)
# ------------------------------
app = Flask(__name__)

# Puerto 5800
PORT = 5800

# ------------------------------
# 3. Crear la base de datos y tabla si no existe
# ------------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ------------------------------
# 4. Insertar usuario con contraseña hasheada
# ------------------------------
def insert_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Si el usuario ya existe, ignorar
    conn.close()

# ------------------------------
# 5. Validar usuario
# ------------------------------
def validate_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user

# ------------------------------
# 6. Página principal para registrar y validar
# ------------------------------
html = """
<h2>Registro de Usuario</h2>
<form method="POST" action="/register">
  Nombre: <input name="username"><br>
  Contraseña: <input name="password" type="password"><br>
  <input type="submit" value="Registrar">
</form>

<h2>Login</h2>
<form method="POST" action="/login">
  Nombre: <input name="username"><br>
  Contraseña: <input name="password" type="password"><br>
  <input type="submit" value="Ingresar">
</form>
"""

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    insert_user(username, password)
    return f"Usuario {username} registrado."

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        return f"¡Bienvenido, {username}!"
    else:
        return "Usuario o contraseña incorrecta."

# ------------------------------
# 7. Inicializar DB y correr la app
# ------------------------------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=PORT)
