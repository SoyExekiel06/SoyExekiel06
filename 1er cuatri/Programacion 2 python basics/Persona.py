class Persona:
    edad = 0
    nombre = ""

    def presentacion(self):
        print("Hola soy {} y tengo {} años"
            .format(self.nombre, self.edad))
    
    def __init__(self, nombre, edad = 17):
        self.edad = edad
        self.nombre = nombre

if __name__ == "__main__": 
    params = {"nombre": "Santiago", "edad": 19}
    myPerson0 = Persona(**params)
    myPerson0.presentacion()