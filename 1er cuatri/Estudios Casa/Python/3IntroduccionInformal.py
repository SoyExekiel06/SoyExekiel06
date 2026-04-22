url = 'https://docs.python.org/es/3.14/tutorial/introduction.html'


'''#Python como calculadora
        tax = 12.5 / 100
        price = 100.50
        price * tax
        12.5625
        price + _
        113.0625
        round(_, 2)
        113.06'''

#para hacer “\” “Alt Gr” + “?”
#ejemplos: 
#    O\ 'Higgins

#    Me dijo  \ "Vas a poder hacerlo\ "

#    Primera Linea '\ n'Segunda Linea

#    (r'C:\NombreDeCarpeta')

    
#    '''\
#    Usage: thingy [OPTIONS]
#         -h                        Display this usage message
#        -H hostname               Hostname to connect to
#    '''


'''Concatenacion y repeticion
    2* + 'un' + 'hexio'

    pre = 'Py'

    pal = pre + 'thon'

    'Pon muchos str sin parentesis ' 
    'para tenerlos unidos'
     Esto solo funciona con dos str literales, no con variables ni expresiones
    
    pal[0] #Primer caracter
    
    pal[5] #Quinta posicion
    
    pal[-1] #Ultima posicion
      
    pal[-2] #Antepenultima posicion
     
    pal[:2] #Caracteres desde el principio a la posicion 2 (Excluida)
    
    pal[4:] #Caracteres de la posicion 4 (Incluida) hasta el final
    
    pal[-2:] #Caracteres desde el anteultimo (Incluido) hasta el final
    
    pal[:x] + pal[x:] == pal #True
    
    pal[50] #Error, pal solo tiene 6 letras
    
    pal[4:50] #Ultimas 2 letras (en este str de 6 caracteres) 
    
    pal[:50] #str vacio (si esta fuera de indice)
    
    pal[:2] = 'py' #Error, las cadenas no se pueden modificar
    #pero, si puedes crear una nueva...
      
    pal[:2] + 'py' #pypy
    '''

'''Listas
    cuad = [1, 4, 9, 16, 25]

    cuad[0] #indexar devuelve el item

    cuad[-3:]

    cuad + [36, 49, 64, 81, 100]

    cubos = [1, 8, 27, 65, 125]

    cubos[3] = 64 #[1, 8, 27, 64, 125]

    cubos.append(216) #[1, 8, 27, 64, 125, 216]

    cubos.append(7**3) #[1, 8, 27, 64, 125, 216, 343]

    rgb = ['Red', 'Green', 'Blue']

    rgba = rgb

    id(rgb) == id(rgba) #True

    rgba.append('Alpha')

    print(rgb) #['Red', 'Green', 'Blue', 'Alph']

    correctRgba = rgba[:]

    correctRgba[-1] = 'Alpha'

    print(correctRgba) #['Red', 'Green', 'Blue', 'Alpha']
    print(rgba) #['Red', 'Green', 'Blue', 'Alph']

    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    print(letras[2:5]) #['C', 'D', 'E']

    letras[:] = []
    print(letras) #[]

    print(len(letras)) #0

    a = ['a', 'b', 'c'] #Primera lista
    n = [1, 2, 3] #Segunda lista
    x = [a, n] #Lista de 2 listas
    print(x) #Imprime lista de listas
    print(x[0]) #imprime lista de indice 0
    print(x[0][1]) #Imprime el segundo indice de la segunda lista'''

'''Primeros pasos programando (con fibonacci)
a, b = 0, 1

while a < 10:
    print(a, end = ', ') #0, 1, 1, 2, 3, 5, 8
    a, b = b, a + b

i = 256 * 256

print("El valor de i es: ", i) #65536'''