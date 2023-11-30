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
        self.cursor.execute('''CREATE TABLE IF NOT EXIST reservas(
            codigo INT (3) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            apellido VARCHAR (60) NOT NULL,
            nombre VARCHAR (60) NOT NULL,
            dni INT (8), NOT NULL,
            mail VARCHAR
            cantidad INT(1),
            habitacion VARCHAR (10),
            ingreso INT(8),
            egreso INT(8),
            pago INT(2))
                            ''')
        self.conn.commit()


#REVISAR
# codigo seria como un codigo de reserva (un id)
# fijarse como poner el mail y las fechas


# Cerrar el cursor inicial y abrir uno nuevo con el parametro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


#--------------------------------------------------------------------

    def agregar_reserva(self, codigo, apellido, nombre, dni, mail, cantidad, habitacion, ingreso, egreso, pago):
        # Verificamos si ya existe el huesped con el mismo codigo de reserva
        self.cursor.execute(f"SELECT * FROM reservas WHERE codigo = {codigo}")
        reserva_existe = self.cursor.fetchone()
        if reserva_existe:
            return False

        sql = "INSERT INTO reservas (codigo, apellido, nombre, dni, mail, cantidad, habitacion, ingreso, egreso, pago) VALUES (%s %s %s %s %s %s %s)"
        valores = (codigo, apellido, nombre, dni, ingreso, egreso, pago)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True


#--------------------------------------------------------------------

    def consultar_reserva(self, codigo):
# Consultamos el huesped a partir del codigo de reserva
        self.cursor.execute(f"SELECT * FROM reservas WHERE codigo = {codigo}")
        return self.cursor.fetchone()


#--------------------------------------------------------------------

    def modificar_reserva(self, codigo, nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso, nuevo_pago):
        sql = "UPDATE reservas SET apellido = %s, nombre = %s, dni = %s, mail = %s, cantidad = %s, habitacion = %s, ingreso = %s, egreso = %s, pago = %s WHERE codigo = %s"
        valores = (nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso, nuevo_pago, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


#--------------------------------------------------------------------


    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        reservas = self.cursor.fetchall()
        return reservas


#--------------------------------------------------------------------

    def eliminar_reservas(self, codigo):
    # Eliminamos una reserva de la tabla a partir de su codigo (o apretando el boton en la tabla???)
        self.cursor.execute(f"DELETE FROM reservas WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0 


#--------------------------------------------------------------------

    def mostrar_reservas(self, codigo):
    # Mostramos los datos de un huesped a partir de su codigo de reserva
        reserva = self.consultar_reserva(codigo)
    if reserva: 
        print ("-" * 40)
        print (f"Código........: {reserva['codigo']}")
        print (f"Apellido......: {reserva['apellido']}")
        print (f"Nombre........: {reserva['nombre']}")
        print (f"DNI...........: {reserva['dni']}")
        print (f"Mail..........: {reserva['mail']}")
        print (f"Cantidad......: {reserva['cantidad']}")
        print (f"Habitacion....: {reserva['habitacion']}")
        print (f"Fe. de Ingreso: {reserva['ingreso']}")
        print (f"Fe. de Egreso.: {reserva['egreso']}")
        print (f"Me. de Pago...: {reserva['pago']}")
        print ("-" * 40)
    else: 
        print("Huesped no registrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Huesped

reserva = Reserva(host='localhost', user='root', password='', database= 'miapp')

reserva.agregar_reserva(1, "Paez", "Florencia", 36170641, fajglgl@hotmail.com, 2, CSS, 28112023, 30112023, 2)
reserva.agregar_reserva(2, "Dominguez", "Pedro", 23575685, fajglgl@hotmail.com, 1, HTML, 30112023, 15122023, 2)
reserva.agregar_reserva(3, "Stover", "Juan Martin", 28194042, fajglgl@hotmail.com, 2, PYTHON , 29112023, 12122023, 2)


#--------------------------------------------------------------------

#fetch("https://jovial-klepon-1e2878.netlify.app/reservar")
@app.route("/reservas", methods=["GET"])
def listar_reservas():
    reserva = Reserva.listar_reservas()
    return jsonify(reserva)

#--------------------------------------------------------------------

@app.route("/reservas/<int:codigo>", methods=["GET"])
def mostrar_reservas(codigo):
    reserva = Reserva.consultar_reserva(codigo)
    if reserva:
        return jsonify(reserva), 201
    else:
        return "Reserva no registrada", 403

#--------------------------------------------------------------------

@app.route("/reservas", methods=["POST"])
def agregar_reserva():
    codigo = request.form['codigo']
    apellido = request.form['apellido']
    nombre = request.form['nombre']
    dni = request.form['dni']
    mail = request.form['mail']
    cantidad = request.form['cantidad']
    habitacion = request.form['habitacion']
    ingreso = request.form['ingreso']
    egreso = request.form['egreso']
    pago = request.form['pago']

    if Reserva.agregar_reserva(codigo, apellido, nombre, dni, mail, cantidad, habitacion, ingreso, egreso, pago):
        return jsonify({"mensaje": "Reserva registrada"}), 201
    else: 
        return jsonify({"mensaje": "Ya existe este codigo"}), 400


#--------------------------------------------------------------------


@app.route("/reservas/<int:codigo>", methods=["PUT"])
def modificar_reserva(codigo):
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
    nuevo_pago = data.get("pago")

#actualizacion de la reserva
    if reserva.modificar_reserva(codigo, nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso, nuevo_pago):
        return jsonify({"mensaje": "Reserva modificada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404


#--------------------------------------------------------------------

@app.route("/reservas/<int:codigo>", methods=["DELETE"])
def eliminar_reservas(codigo):
    if reser.eliminar_reservas(codigo):
        return jsonify({"mensaje": "Reserva eliminada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

#--------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)