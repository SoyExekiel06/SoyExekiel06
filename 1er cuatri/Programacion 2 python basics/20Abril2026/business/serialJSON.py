import json
from .pais import pais

def serialize(data, file):
    with open(file, "w") as f:
        text = json.dumps(data, indent = 4)
        f.write(text)

def deserialitation(file):
    with open(file) as f:
        text = f.read()
        return json.loads(text)
  
 
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
    file = "data/pais.json"
    myPais = pais()
    serialize(myPais.toDict(),file)
    input("Presione una tecla para copntinuar")
    myPais.fromDict(deserialitation(file))
    print(myPais.name)