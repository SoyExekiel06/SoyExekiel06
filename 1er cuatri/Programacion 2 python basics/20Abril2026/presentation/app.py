import business.serialXML as sXML
import business.serialJSON as sJSON
import business.serialYAML as sYAML

class app:
    def prompt():
        x1 = sXML
        x2 = sJSON
        x3 = sYAML

        num = 0
        while (num<=4):
            def inicio1(x):
                x.inicio()
            def inicio2(x2):
                x2.inicio()
            def inicio3(x3):
                x3.inicio()
        
            print("Ingrese 1 si quiere recibir informacion de pais.xml")
            print("Ingrese 2 si quiere recibrir informacion de pais.JSON")
            print("Ingrese 3 si quiere recibir informacion de  pais.YAML")
            try:
                num = int(input("Ingrese 4 o mas si quiere salir: "))
                match num:
                    case 1: 
                        inicio1(x1)
                    case 2:
                        inicio2(x2)
                    case 3:
                        inicio3(x3)
                    case _:
                        print("saliendo")
                        break
            except Exception as e:
                print("Error real:", e)