
# print("\033[H\033[J") #para limpiar la consola


#lista de reservas
reservas = []
#esta lista va a ser una lista de diccionarios 
# {'cod':1, 'apellido': , 'nombre: ', , , , , }


#----------------------------------------------
#Funcion para consultar las reservas
#----------------------------------------------

def ver_reservas(cod):
    for reserva in reservas:
        if reserva['codigo'] == cod:
            return reserva
    return False


#----------------------------------------------
#Funcion para dar de alta a los huespedes
#----------------------------------------------

def agregar_reserva(cod, ape, nom, dni, mail, cant, hab, ingr, egr, pago):
    if ver_reservas(cod):
        return False
    else:
        huesped = {
            "codigo": cod,
            "apellido": ape,
            "nombre": nom,
            "dni": dni,
            "mail": mail,
            "cantidad": cant,
            "habitacion": hab,
            "ingreso": ingr,
            "egreso": egr,
            "pago": pago 
        }
        reservas.append(huesped)
        return True


#----------------------------------------------
#Funcion para listar a las reservas
#----------------------------------------------

def listar_reservas():
    print("-"*15)
    for reserva in reservas:
        print(f"    Codigo: {reserva['codigo']}")
        print(f"  Apellido: {reserva['apellido']}")
        print(f"    Nombre: {reserva['nombre']}")
        print(f"       DNI: {reserva['dni']}")
        print(f"      Mail: {reserva['mail']}")
        print(f"  Cantidad: {reserva['cantidad']}")
        print(f"Habitacion: {reserva['habitacion']}")
        print(f"   Ingreso: {reserva['ingreso']}")
        print(f"    Egreso: {reserva['egreso']}")
        print(f"      Pago: {reserva['pago']}")
        print("-"*15)



#----------------------------------------------
#Funcion para mostrar las reservas
#----------------------------------------------

def mostrar_reservas(reserva):
    print("-"*15)
    print(f"    Codigo: {aux['codigo']}")
    print(f"  Apellido: {aux['apellido']}")
    print(f"    Nombre: {aux['nombre']}")
    print(f"       DNI: {aux['dni']}")
    print(f"      Mail: {aux['mail']}")
    print(f"  Cantidad: {aux['cantidad']}")
    print(f"Habitacion: {aux['habitacion']}")
    print(f"   Ingreso: {aux['ingreso']}")
    print(f"    Egreso: {aux['egreso']}")
    print(f"      Pago: {aux['pago']}")
    print("-"*15)



#----------------------------------------------
#Funcion para eliminar una reserva
#----------------------------------------------

def eliminar_reservas(cod):
    for reserva in reservas:
        if reserva['codigo'] == cod:
            reservas.remove(reserva)
            return True
    return False




#----------------------------------------------
#Funcion para modificar las reservas
#----------------------------------------------

def modificar_reserva(cod, ape, nom, dni, mail, cant, hab, ingr, egr, pago):
    reserva = ver_reservas(cod)
    if reserva:
        reserva["codigo"] = cod
        reserva["apellido"] = ape
        reserva["nombre"] = nom
        reserva["dni"] = dni
        reserva["mail"] = mail
        reserva["cantidad"] = cant
        reserva["habitacion"] = hab
        reserva["ingreso"] = ingr
        reserva["egreso"] = egr
        reserva["pago"] = pago 

        eliminar_reservas(cod)
        reservas.append(reserva)
        return True
    else:
        return False
    




#----------------------------------------------------------------------------------------------

print("\033[H\033[J")
print(agregar_reserva(1, "Perez", "Alejando", 24595284, "alejandroperez@gmail.com", 2, "HTML" , 12122023, 20122023, "tarjeta"))
print(agregar_reserva(2, "Rico", "Maria", 35167585, "rico_maria@gmail.com", 4, "PYTHON" , 12122023, 20122023, "tarjeta"))
print(agregar_reserva(3, "Rodriguez", "Liliana", 15635744, "llrodriguez@gmail.com", 2, "JAVASCRIPT" , 22122023, 27122023, "efectivo"))

#print(reservas)

listar_reservas()

#aux = ver_reservas(1)
#if aux:
#    mostrar_reservas(aux)
#else:
#    print("Reserva no encontrada.")

print(modificar_reserva(1, "Paez", "Alejando", 15494294, "alejandro_paez@gmail.com", 2, "HTML" , 12122023, 20122023, "tarjeta"))
listar_reservas()



