import json
import os

class dataHelper:

    def __init__(self):
        self.usersFile= 'users.json'


    def addUser(self, username, hashedPassword):
        #TODO validaciones si el usuario se encuentra o no en el archivo
        
        users = self.deserialize(self.usersFile) #entro al file

        users[username] = hashedPassword #en la key username va a poner el hashed password

        self.serialize(users, self.usersFile) #lo vuelvo a serializar en json :)

    def getUser(self, username):
        users = self.deserialize(self.usersFile)
        try:
            return users[username] # tira key error si el usuario no existe
        except KeyError:
            return None

    def serialize(self, data, file): #abre el archivo para insertar el usuario
        with open(file, "w") as f:
            f.write(json.dumps(data, indent=4))


    def deserialize(self,file):
        with open(file, "r") as f:
            return json.loads(f.read())