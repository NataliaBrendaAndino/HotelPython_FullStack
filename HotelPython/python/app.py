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
            dni INT,
            correo VARCHAR(30) UNIQUE,
            cantidad INT,
            habitacion VARCHAR(10),
            ingreso DATE,
            egreso DATE)''')
        self.conn.commit()



# Cerrar el cursor inicial y abrir uno nuevo con el parametro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


#--------------------------------------------------------------------

    def agregar_reserva(self, apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso):
        try:
            sql = f"INSERT INTO reservas (apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso) VALUES ('{apellido}', '{nombre}', {dni}, '{correo}', {cantidad}, '{habitacion}', '{ingreso}', '{egreso}')"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
        # Maneja la excepción específica para el código duplicado
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                return False
        else:
            raise err

#--------------------------------------------------------------------

    def ver_reservas(self, dni):
        self.cursor.execute(f"SELECT * FROM reservas WHERE dni = {dni}")
        respuesta = self.cursor.fetchone()
        return respuesta 


#--------------------------------------------------------------------

    def modificar_reserva(self, antiguo_dni, nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso):
        sql = "UPDATE reservas SET apellido= %s, nombre = %s, dni = %s, correo = %s, cantidad = %s, habitacion = %s, ingreso = %s, egreso = %s  WHERE dni = %s"
        valores = (nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_mail, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso, antiguo_dni)
        self.cursor.execute(sql, valores)
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

reserva = Reserva(host='localhost', user='root', password='root', database= 'miapp')

reserva.agregar_reserva("Paez", "Florencia", 36174865, "paezflorencia@gmail.com", 2, "PYTHON", '20231223', '20231202')
reserva.agregar_reserva("Rodriguez", "Damian", 23567246, "damian_rod@gmail.com", 2, "HTML", '20231210', '20231201')
reserva.agregar_reserva("Castro", "Daniel", 13567284, "castrodan@gmail.com", 4, "JAVASCRIPT", '20231210', '20231201')
reserva.agregar_reserva("Juarez", "Unai", 33466224, "unaijuarez_17@gmail.com", 2, "CSS", '20240110', '20240115')



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
    apellido = request.form.get('firstname')
    nombre = request.form.get('lastname')
    dni = request.form.get('dni')
    correo = request.form.get('mail')
    cantidad = request.form.get('number')
    habitacion = request.form.get('habitacion')
    ingreso = request.form.get('fecha_de_ingreso')
    egreso = request.form.get('fecha_de_salida')

    if reserva.agregar_reserva(apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso):
        return jsonify({"mensaje": "Reserva registrada"}), 201


#--------------------------------------------------------------------


@app.route("/reservas/<int:antiguo_dni>", methods=["PUT"])
def modificar_reserva(antiguo_dni):
    # revisar como hacer para poder modificar a través de un botón
    # datos de la reserva
    nuevo_apellido = request.form.get('apellido')
    nuevo_nombre = request.form.get('nombre')
    nuevo_dni = request.form.get('nuevo_dni')
    nuevo_correo = request.form.get('correo')
    nueva_cantidad = request.form.get('cantidad')
    nueva_habitacion = request.form.get('habitacion')
    nuevo_ingreso = request.form.get('ingreso')
    nuevo_egreso = request.form.get('egreso')

    # actualización de la reserva
    try:
        if reserva.modificar_reserva(antiguo_dni, nuevo_apellido, nuevo_nombre, nuevo_dni, nuevo_correo, nueva_cantidad, nueva_habitacion, nuevo_ingreso, nuevo_egreso):
            return jsonify({"mensaje": "Reserva modificada"}), 200
        else:
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
    except Exception as e:
        print("Error al modificar reserva:", e)
        return jsonify({"mensaje": "Error al modificar reserva"}), 500



#--------------------------------------------------------------------

@app.route("/reservas/<int:codigo>", methods=["DELETE"])
def eliminar_reservas(codigo):
    if reserva.eliminar_reservas(codigo):
        return jsonify({"mensaje": "Reserva eliminada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

#--------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)