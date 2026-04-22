import xmlrpc.client as xml
from .pais import pais

def serialize(data, file):
    with open(file, "w") as f:
        text = xml.dumps((data,))
        f.write(text)

def deserialize(file):
    with open(file) as f:
        text = f.read()
        return xml.loads(text)[0][0]
  
 
# data = {
#     "name" : "Argentina",
#     "population" : 50000000,
#     "Sup" : 2780000,
#     "Capital" : "CABA",
#     "footballTeams" : [
#         {
#             "name" : "River PLate"
#         }, 
#         {
#              "name" : "Boca Juniors"
#         },
#         {
#             "name" : "San Lorenzo"
#         }
#     ]
# }
def inicio():
    file = "data/pais.xml"
    myPais = pais()
    serialize(myPais.toDict(),file)
    input("Presione una tecla para copntinuar")
    myPais.fromDict(deserialize(file))
    print(myPais.name)