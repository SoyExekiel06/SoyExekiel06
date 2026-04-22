import tabulate as tbl

parciales = {"Alquiler" : 200000}

print(parciales["Alquiler"])

gastos = [
    {"Categoria" : "Estudio" , "Monto" : -53000},
    {"Categoria" : "Comida", "Monto" : -2000 * 8},
    {"Categoria" : "Comida", "Monto" : -1350 * 5 * 8},
    {"Categoria" : "OcioDT", "Monto" : -9000 #Netflix
    },
    {"Categoria" : "OcioDMP", "Monto" : -86500 / 2 #Cuarteto de Nos
    },
    {"Categoria" : "ServiciosF", "Monto" : -10500 #Internet
    }, 
    {"Categoria" : "Iglesia", "Monto" :  -parciales["Alquiler"] * (5/100)}]
totales = []
netos = {}
cateDigi = ["OcioDMP", "OcioDT"]
for gasto in gastos:
    try:
        parciales[gasto["Categoria"]] += gasto["Monto"]
    except KeyError:
        parciales[gasto["Categoria"]] = gasto["Monto"]

for Categoria in parciales.keys():
    totales.append([Categoria, parciales[Categoria]])

neto = sum(parciales.values())

digi = sum(v for k, v in parciales.items() if k in cateDigi)

totales.append(["Digital", digi])

totales.append(["Neto", neto])

tabla = tbl.tabulate(totales, headers=["Categoria", "Total"])
print(tabla)