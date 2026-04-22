import Persona as per
parms = {"nombre": "Julio", "edad": 78}
myPersona = per.Persona(**parms)
myPersona.presentacion()