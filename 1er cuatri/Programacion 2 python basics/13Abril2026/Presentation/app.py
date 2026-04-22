from Business.logic import Logic

class App:
    def prompt(self):
        print("",40*"*", "\n Bienvenidos al himalaya ¿helado? \n", 40*"*")
        
        dni = input("Ingrese DNI (Solo numeros, sin puntos):")
        user = input("Ingrese el nombre: ")
        myLogic = Logic(user, dni)
        if myLogic.validate() == False:
            print("Datos Ingresados erroneos...")
            return
        print(myLogic.check())