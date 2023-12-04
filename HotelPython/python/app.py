#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------

class Reserva:
    #atributo de clase
    reservas = [ ]
    #--------------------------------------------------------------------
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexion sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host = host,
            user = user, 
            password = password
        )
        self.cursor = self.conn.cursor()

# Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

# Una vez que la base de datos esta establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservas(
            apellido VARCHAR (60),
            nombre VARCHAR (60),
            dni INT PRIMARY KEY,
            correo VARCHAR(30),
            cantidad INT,
            habitacion VARCHAR(10),
            ingreso DATE,
            egreso DATE)''')
        self.conn.commit()



# Cerrar el cursor inicial y abrir uno nuevo con el parametro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


#--------------------------------------------------------------------

    def agregar_reserva(self, ape, nom, dni, mail, cant, hab, ingr, egr):
        # Verificamos si ya existe el huesped con el mismo codigo de reserva
        self.cursor.execute(f"SELECT * FROM reservas WHERE dni = {dni}")
        respuesta = self.cursor.fetchone()
        if respuesta:
            return False
        else:                
            sql = f"INSERT INTO reservas (apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso) VALUES ('{ape}', '{nom}', {dni}, '{mail}', {cant}, '{hab}', {ingr}, {egr})"

        self.cursor.execute(sql)
        self.conn.commit()
        return True


#--------------------------------------------------------------------

    def ver_reservas(self, dni):
        self.cursor.execute(f"SELECT * FROM reservas WHERE dni = {dni}")
        respuesta = self.cursor.fetchone()
        return respuesta 


#--------------------------------------------------------------------

    def modificar_reserva(self, ape, nom, dni, mail, cant, hab, ingr, egr):
        sql = f"UPDATE reservas SET \
                    apellido = '{ape}', \
                    nombre = '{nom}', \
                    correo = '{mail}', \
                    cantidad = {cant}, \
                    habitacion = '{hab}', \
                    ingreso = {ingr}, \
                    egreso = {egr}, \
                WHERE dni = {dni}"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0


#--------------------------------------------------------------------

    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        reservas = self.cursor.fetchall()
        return reservas

#--------------------------------------------------------------------

    def eliminar_reservas(self, dni):
        self.cursor.execute(f"DELETE FROM reservas WHERE dni = {dni}")
        self.conn.commit()
        return self.cursor.rowcount > 0


#--------------------------------------------------------------------

    def mostrar_reservas(self, reserva):
        if reserva:
            print("-"*15)
            print(f"  Apellido: {reserva['apellido']}")
            print(f"    Nombre: {reserva['nombre']}")
            print(f"       DNI: {reserva['dni']}")
            print(f"    Correo: {reserva['correo']}")
            print(f"  Cantidad: {reserva['cantidad']}")
            print(f"Habitacion: {reserva['habitacion']}")
            print(f"   Ingreso: {reserva['ingreso']}")
            print(f"    Egreso: {reserva['egreso']}")
            print("-"*15)
        else: 
            print("Huesped no registrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Huesped

reserva = Reserva(host='localhost', user='root', password='', database= 'miapp')

reserva.agregar_reserva("Paez", "Florencia", 36257437, "paez.florencia@gmail.com", 2, "CSS", '20231215', '20231220')


#--------------------------------------------------------------------

#fetch("https://jovial-klepon-1e2878.netlify.app/reservar")
@app.route("/reservas", methods=["GET"])
def listar():
    reservas = reserva.listar_reservas()
    return jsonify(reservas)

#--------------------------------------------------------------------

@app.route("/reservas/<int:dni>", methods=["GET"])
def mostrar_reserva_reservas(dni):
    reservas = reserva.ver_reservas(dni)
    if reservas:
        return jsonify(reservas), 201
    else:
        return "Reserva no registrada", 403

#--------------------------------------------------------------------

@app.route("/reservas", methods=["POST"])
def agregar_reserva():
    apellido = request.form['lastname']
    nombre = request.form['firstname']
    dni = request.form['dni']
    correo = request.form['mail']
    cantidad = request.form['number']
    habitacion = request.form['habitacion']
    ingreso = request.form['fecha_de_ingreso']
    egreso = request.form['fecha_de_egreso']

    if reserva.agregar_reserva(apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso):
        return jsonify({"mensaje": "Reserva registrada"}), 201


#--------------------------------------------------------------------


@app.route("/reservas/<int:dni>", methods=["PUT"])
def modificar_reserva(dni):
    #revisar como hacer para poder modificar a traves de un boton
    #datos de la reserva
    data = request.form
    nuevo_apellido = data.get("apellido")
    nuevo_nombre = data.get("nombre")
    nuevo_dni = data.get("dni")
    nuevo_mail = data.get("mail")
    nueva_cantidad = data.get("cantidad")
    nueva_habitacion = data.get("habitacion")
    nuevo_ingreso = data.get("ingreso")
    nuevo_egreso = data.get("egreso")

#actualizacion de la reserva
    if reserva.modificar_reserva(nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso):
        return jsonify({"mensaje": "Reserva modificada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404


#--------------------------------------------------------------------

@app.route("/reservas/<int:dni>", methods=["DELETE"])
def eliminar_reservas(dni):
    if reserva.eliminar_reservas(dni):
        return jsonify({"mensaje": "Reserva eliminada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

#--------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)