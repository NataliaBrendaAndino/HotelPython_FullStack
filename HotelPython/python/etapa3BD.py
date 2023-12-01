#agregar un conector a la base de datos:
import mysql.connector

#Cursor: 

#creamos un objeto de reservas

class Reserva:
    #atributo de clase
    reservas = [ ]
    #constructor
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservas(
            codigo INT,
            apellido VARCHAR (60),
            nombre VARCHAR (60),
            dni INT,
            correo VARCHAR(30),
            cantidad INT,
            habitacion VARCHAR(10),
            ingreso DATETIME,
            egreso DATETIME,
            pago VARCHAR (15))''')
        self.conn.commit()


    #------------------------------------------
    #Metodo para dar de alta las reservas
    #-----------------------------------------

    def agregar_reserva(self, cod, ape, nom, dni, mail, cant, hab, ingr, egr, pago):
        self.cursor.execute(f"SELECT * FROM reservas WHERE codigo = {cod}")
        respuesta = self.cursor.fetchone()
        if respuesta: 
            return False
        else:
            sql = f"INSERT INTO reservas \
                (codigo, apellido, nombre, dni, correo, cantidad, habitacion, ingreso, egreso, pago) VALUES \
                ({cod}, '{ape}', '{nom}', {dni}, '{mail}', {cant}, '{hab}', {ingr}, {egr}, '{pago}')"
            #print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
            return True

#los valores que son cadenas llevan '', los que son numericos no llevan


    #------------------------------------------
    #Metodo para consultar las reservas
    #-----------------------------------------

    def ver_reservas(self, cod):
        self.cursor.execute(f"SELECT * FROM reservas WHERE codigo = {cod}")
        respuesta = self.cursor.fetchone()
        return respuesta 


    #------------------------------------------
    #Metodo para mostrar las reservas
    #-----------------------------------------

    def mostrar_reservas(self, reserva):
        print("-"*15)
        print(f"    Codigo: {reserva['codigo']}")
        print(f"  Apellido: {reserva['apellido']}")
        print(f"    Nombre: {reserva['nombre']}")
        print(f"       DNI: {reserva['dni']}")
        print(f"    Correo: {reserva['correo']}")
        print(f"  Cantidad: {reserva['cantidad']}")
        print(f"Habitacion: {reserva['habitacion']}")
        print(f"   Ingreso: {reserva['ingreso']}")
        print(f"    Egreso: {reserva['egreso']}")
        print(f"      Pago: {reserva['pago']}")
        print("-"*15)



    #------------------------------------------
    #Metodo para eliminar las reservas
    #-----------------------------------------

    def eliminar_reservas(self, cod):
        self.cursor.execute(f"DELETE FROM reservas WHERE codigo = {cod}")
        self.conn.commit()
        return self.cursor.rowcount > 0


    #------------------------------------------
    #Metodo para modificar las reservas
    #-----------------------------------------

    def modificar_reserva(self, cod, ape, nom, dni, mail, cant, hab, ingr, egr, pago):
        sql = f"UPDATE reservas SET \
                    apellido = '{ape}', \
                    nombre = '{nom}', \
                    dni = {dni}, \
                    correo = '{mail}', \
                    cantidad = {cant}, \
                    habitacion = '{hab}', \
                    ingreso = {ingr}, \
                    egreso = {egr}, \
                    pago = '{pago}' \
                WHERE codigo = {cod}"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0 


#-------------------------------------------------------------------------------

print("\033[H\033[J")

reserva = Reserva(host="localhost", user="root", password="", database="miapp")

print(reserva.modificar_reserva(10, "Miranda", "Ana", 12344858, "amiranda@gmail.com", 2, "JAVASCRIPT", '20231223', '202312026', "efectivo"))
#reserva.agregar_reserva(11, "Juantorena", "Ana Maria", 17392749, "juan_torena@gmail.com", 2, "JAVASCRIPT", '20240206', '20240209', "efectivo")

#print(reserva.eliminar_reservas(9))

#z = reserva.ver_reservas(7)
#reserva.mostrar_reservas(z)
