import yaml
from .pais import pais

def serialize(data, file):
    with open(file, "w") as f:
        text = yaml.dump(data, explicit_end=True, explicit_start=True)
        f.write(text)

def deserialize(file):
    with open(file) as f:
        text = f.read()
        return yaml.safe_load(text)
  
 
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
    file = "data/pais.yaml"
    myPais = pais()
    serialize(myPais.toDict(),file)
    input("Presione una tecla para copntinuar")
    myPais.fromDict(deserialize(file))
    print(myPais.name)