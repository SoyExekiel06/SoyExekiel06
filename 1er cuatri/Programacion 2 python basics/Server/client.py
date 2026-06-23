import requests


def menu():
    print("1- Monedas")
    print("2- Cotizaciones")
    print("3- Leer cotizacion con post")
    return int(input().strip())

if __name__ == "__main__":
    opcion = menu()
    match opcion:
        case 1:
            response = requests.get("http://127.0.0.1:20220/monedas")
            print(response.status_code)
            print(response.json())
        case 2:
            codigo = input("Ingrese el codigo de moneda: \n").strip()
            url = "http://127.0.0.1:20220/cotizacion?codigo={}".format(codigo)
            response = requests.get(url)
            print(response.status_code)
            print(response.json())
        case 3:
            code = input("Ingrese el Codigo de la moneda \n").strip()
            url = "http://127.0.0.1:20220/cotizacion?codigo={}".format(code)
            body = "{" + '"codigo"' + ": " + '"' + code + '"' + "}"
            response = requests.post(url, json=body)
            print(response.status_code)
            print(response.json())
