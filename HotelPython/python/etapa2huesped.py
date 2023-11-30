# definimos la clase Huesped:
class Huesped:
    #atributo de clase
    #constructor
    def __init__(self, ape, nom, dni, mail):
        self.apellido = ape
        self.nombre = nom
        self.dni = dni
        self.mail = mail

    def __str__(self):
        datos = f"Nombre: {self.apellido}, {self.nombre} \nDNI   : {self.dni} \nMail  : {self.mail}"
        print("-"*10)
        return datos
        

    
    def __del__(self):
        print(f"Objeto {self.nombre} borrado.")



    #---------------------------------------------------
print("\033[H\033[J") #limpiar la consola

huesped1 = Huesped("Perez", "Mario", 23447294, "marioperez@gmail.com")
huesped2 = Huesped("Gomez", "Lili", 12495194, "gomez_l@gmail.com")

print(huesped1)
print(huesped2)