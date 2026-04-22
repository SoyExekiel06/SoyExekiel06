url = 'https://docs.python.org/es/3.14/tutorial/controlflow.html'

"""Sentencia if 
    x = int(input('Ingrese un entero: '))
    if x < 0:
        x = 0
        print('Negativo cambiado a cero')
    elif x ==0:
        print('Cero')
    elif x == 1:
        print('Uno')
    else:
        print('Varios')"""

"""Sentencia for
    pals = ['gato', 'ventana', 'defenestrado']
    for i in pals:
        print(i, len(i))
    
    users = {'Hans': 'Activo', 'Eleonora' :'Inactivo', '景太郎' : 'Activo'}
    for user, status in users.copy().items():
        if status == 'Inactivo':
            del users[user]
    activeUsers = {}
    for user, status in users.items():
        if status == 'Activo':
            activeUsers[user] = status"""

""" Funcion Range()
    for i in range(5):
        print(i)
    
    list(range(5, 10)) #Empieza en 5, termina antes del numero 10
    list(range(0, 10, 3)) #Empieza en 0, termina antes del numero 10, va de 3 en 3
    list (range(-10, -100, -30)) #empieza en -10, termina antes del 100, va de -30 en -30

    a = ['Maria', 'tenia', 'un', 'pequeño', 'cordero']
    for i in range(len(a)):
        print(i, a[i])
    
    sum(range(4)) #0 + 1 + 2 + 3
"""

"""Break y continue
for n in range(2, 1000): #(primer numero que se intenta obtener su MCP, numero maximo de intentos - 1)
    for x in range(2, n): #(MCP, n)
        if n % x == 0:
            print(f"{n} es igual {x} * {n//x}")
            break #el break hace que solo este el menor numero por el que se puede multiplicar el primer factor
        #Sin el break estarian todas las multiplicaciones de numeros naturales, desde el primer numero intentado

for num in range(1, 10):
    if num % 2 == 0:
        print(f"Se encontro un numero par {num}")
        continue   
    print(f"Se encontro un numero impar {num}")
"""

"""else en bucles
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n/x)
                break
        else:
            # loop fell through without finding a factor
            print(n, 'is a prime number')
"""

"""Sentencia Pass
    Se usa principalmente para crear clases o metodos vacios
    class MyClaseVacia:
        pass
    
    def initlog(*args):
        pass   # Recuerda implementar esto!
"""

"""Sentencia Match
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "No encontrado"
        case 418:
            return "Soy una tetera"
        case 500 | 503 | 401:
            return "No permitido"
        case 200:
            return "Todo piola"
        case _:
            return "Algo esta mal con el internet""

        
    class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        
    def where_is(point):
        match point:
            case (0, 0):
                print("Origen")
            case (0, y):
                print(f"Y={y}")
            case (x, 0):
                print(f"X={x}")
            case (x, y):
                print(f"X={x}, Y={y}")
            case _:
                raise ValueError("No un punto")

    from enum import Enum
    class Color(Enum):
        RED = 'red'
        GREEN = 'green'
        BLUE = 'blue'

    color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("Grass is green")
        case Color.BLUE:
            print("I'm feeling the blues :(")  
"""

"""Definir funciones
    def fib(n):    # write Fibonacci series less than n
    "Print a Fibonacci series less than n."
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Now call the function we just defined:
fib(2000)


def preg_Ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        reply = input(prompt)
        if reply in {'s', 'si'}:
            return True
        if reply in {'n', 'no', 'nop'}:
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('Respuesta de usuario invalida')
        print(reminder)

empezar = preg_Ok(prompt="")
if empezar:
    print("Bien hecho")
elif empezar != True:
    print("Ingrese una s")
"""

def fib(n):    # write Fibonacci series less than n
    "Print a Fibonacci series less than n."
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Now call the function we just defined:
fib(2000)