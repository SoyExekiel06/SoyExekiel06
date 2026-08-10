def business(a, b):
    if not (int(a) > 0 or int(b) > 0):
        raise ValueError
    return int(a) + int(b)

def presentation():
    a = input("Ingrese su primer numero natural a sumar: ")
    b = input("Ingrese su segundo numero natural a sumar: ")
    print(business(a, b))

presentation()