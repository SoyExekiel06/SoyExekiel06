try:
    raise StopIteration("Para de buscar el siguiente")
except ZeroDivisionError:
    print("Infinito")
except TypeError:
    print("Fijate que puedas hacer eso con esos tipos de datos")
except Exception as e:
    print("ocurio el error: {}" .format(e.args[0]))