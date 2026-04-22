import tabulate as tbl

gastos = [{
    "Categoria" : "Comida", "Monto" : -150000 #COTO
},
{
    "Categoria" : "Comida", "Monto" : -25000 * 3 #Salidas y cafes
},
{
    "Categoria" : "Servicios", "Monto" : -47000 #internet
},
{
    "Categoria" : "Servicios", "Monto" : -25000 #Luz
},
{
    "Categoria" : "Servicios", "Monto" : -40000 #Gas
},
{
    "Categoria" : "Servicios", "Monto" : -2000 #Agua
},
{
    "Categoria" : "Ocio", "Monto" : -14000 / 2 #Netlix
},
{
    "Categoria" : "ElectroD", "Monto" : -65000 #Lavarropa
},
{
    "Categoria" : "Ejercicio", "Monto" : -25000 #Natacion (1vezXSemanaAlMes)
}
]

totales = []
parciales = {"Ingresos" : 450000}
netos = {}
for gasto in gastos:
    try:
        parciales[gasto["Categoria"]] += gasto["Monto"]
    except KeyError:
        parciales[gasto["Categoria"]] = gasto["Monto"]

for Categoria in parciales.keys():
    totales.append([Categoria, parciales[Categoria]])

neto = sum(parciales.values())

totales.append(["Neto", neto])

tabla = tbl.tabulate(totales, headers=["Categoria", "Total"])
print(tabla)