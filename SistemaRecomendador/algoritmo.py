#Conexión con BBDD
import query
#Operaciones matemáticas (raiz)
import math
import notas

# PRE { Parametros de entrada: userId y un listado de peliculas}
# POST { Devuelve una sentencia que calcula la media de las valoraciones realizadas por userId para el listado de peliculas pasadas por parametro}
def mediaSentencia(user, pelis):
    sentencia='SELECT avg(rating) from rating WHERE userId ='+str(user)+' and ('
    limit = 990 # para evitar el error de límite de líneas en una query
    index = 0
    for i in pelis:
        sentencia+='movieId = '+str(i)+' or '
        index += 1
        if limit == index:
            break
    sentencia=sentencia[:-3] # Se borra el ultimo ' or ' para obtrener una sentencia correcta y ejecutable
    sentencia+=')' # Se finaliza la sentencia para ser ejetuada
    print(sentencia)
    return sentencia
# PRE { Parametros de entrada: userId, movieId, UMBRAL DE SIMILITUD(recogido de la interfaz, por defecto -1)}
# POST { Devuelve la PREDICCION sobre la pelicula yu el usuario pasados por parametros}
def prediccion(u,p,umbral=-1):
    try:
        numerador = 0
        denominador = 0
        votadas = query.votadas(u)   # Consulta que devuelve las peliculas votadas por un usuario
        for i in range(len(votadas)):  # Calculamos la similitud entre las peliculas votadas por el usuario y la pelicula pasados por parametros
            print('iterador: ',i,' logitud: ',len(votadas))
            print("Pelis: ",votadas[i][0],", ",p )
            similitud = sim(votadas[i][0],p)
            if similitud >= umbral:  # Se comprueba que la similitud calculada cumpla la condición
                # Si TRUE realiza la prediccion, si FLASE pasa a la siguiente iteracion (Siguiente pelicula votada)
                # print(similitud,'>=',umbral)
                numerador += (similitud * votadas[i][1])
                print(numerador)
                print('nota de peli votada: ', votadas[i][1])
                denominador += similitud
                print(denominador)
        return round(numerador/denominador,2)
    except:
        return str(notas.recomendacionExt(p)) + " TMDB"
def prediccion_vecindario(u,p,vecindario=5):
    numerador = 0
    denominador = 0
    votadas = query.votadas(u)
    lista = []
    for i in range(len(votadas)):
        similitud = sim(votadas[i][0],p)
        lista.append((similitud, votadas[i][1]))
    lista.sort(key=lambda tup: tup[0], reverse=True) #una vez calculada la prediccion ordenamos la lista
    for i in range(0,vecindario):
        numerador += lista[i][0] * lista[i][1] 
        denominador += lista[i][0]
    return round(numerador/denominador,2)

# PRE { Parametros de entrada: movieId (pelicula votada), movieId (pelicula a predecir)}
# POST { Devuelve un valor [-1 , 1] -> similitud entre ambas peliculas}
def sim(movie1,movie2):
    # comprobamos si el par de peliculas están en la BBDD y si no calculamos la similitud
    if (movie1>movie2):
        aux=movie2
        movie2=movie1
        movie1=aux
    value = query.selectSim(movie1,movie2)
    if 10 != value:
        return value
    # Ambas listas tienen mismo tamaño y mismo orden
    # Obtenemos una lista de tuplas (rating, userId) de aquellos usuarios que han votado ambas peliculas, siendo el rating sobre la pelicula ("mid1")
    ratings1 = query.sameEnergy(movie1,movie2)  
    # Obtenemos una lista de tuplas (rating, userId) de aquellos usuarios que han votado ambas peliculas, siendo el rating sobre la pelicula ("mid2")
    ratings2 = query.sameEnergy(movie2,movie1)
    numerador=0
    denominadorIzq=0 
    denominadorDer=0
    denominador=0
    longitud = len(ratings1)
    print("Longitud= " ,len(ratings1))
    if(longitud < 2):
        query.insertSim(0, movie1,movie2)
        return 0
    #  consulta para obtener la lista de peliculas en comun de aquellos usuarios que han votado las peliculas "movie1" y "movie2" (pasadas por parametro)
    sentencia='SELECT movieId FROM rating WHERE userId = '+str(ratings1[0][1])+' and userId IN (SELECT userId FROM rating WHERE movieId='+str(movie1)+' AND userId IN (SELECT userId FROM rating WHERE movieId='+str(movie2)+'))'
    for j in ratings1:
        #  Construimos la sentencia mediante INTERSECT para ir eliminando de la lista aquellas peliculas que no hayan visto todos los usuarios válidos
        sentencia+='INTERSECT SELECT movieId FROM rating WHERE userId = '+str(j[1])+' and userId IN (SELECT userId FROM rating WHERE movieId='+str(movie1)+' AND userId IN (SELECT userId FROM rating WHERE movieId='+str(movie2)+'))'
    pelisComunes = query.commonFilms(sentencia)
    notaPonderada1 = []
    notaPonderada2 = []

    for i in range(len(ratings1)):
        print(i,'.')
        # Calculamos las valoraciones ponderadas de cada pelicula, para todos los usuarios válidos
        # Siguiendo la formula: vp = valoracion - media de valoraciones (del usuario que ha hecho esa valoración)
        notaPonderada1.append(ratings1[i][0] - query.media(mediaSentencia(ratings1[i][1],pelisComunes)))
        notaPonderada2.append(ratings2[i][0] - query.media(mediaSentencia(ratings2[i][1],pelisComunes)))
        # Se construye el numerador y el denominador de la formula SIMILITUD DEL COSENO
        numerador+=notaPonderada1[i]*notaPonderada2[i]
        denominadorIzq+=notaPonderada1[i]**2
        denominadorDer+=notaPonderada2[i]**2
    denominador=math.sqrt(denominadorIzq)*math.sqrt(denominadorDer)
    if (denominador == 0):
        query.insertSim(0, movie1,movie2)
        return 0
    else:
    # Se devuelve la similitud
        resultado = round(numerador/denominador,2)
        query.insertSim(resultado, movie1,movie2)
        return resultado

def recomendacionesUmbral(usuario, umbral):
    noVotadas = query.noVotadas(usuario)
    lista = []
    for i in noVotadas:
        lista.append((noVotadas[i], prediccion(usuario, noVotadas[i], umbral)))
    lista.sort(key=lambda tup: tup[1], reverse=True)
    return lista

def recomendacionesVecinos(usuario, numVecinos):
    noVotadas = query.noVotadas(usuario)
    lista = []
    for i in noVotadas:
        lista.append((noVotadas[i], prediccion_vecindario(usuario, noVotadas[i], numVecinos)))
    lista.sort(key=lambda tup: tup[1], reverse=True)
    return lista

def insertarSimilitudes(): #funcion que calcula las 47 millones de similitudes y las guarda en BBDD
    for i in range(1,9743):
        for j in range(i+1,9743):
            print(i," ", j)
            # if (i==1 and j==1000): #control de loop en pruebas BORRAR
            #     exit(0)
            # calculo la similitud para el par de pelis selecionadas
            query.insertSim(sim(i,j),i,j)

# insertarSimilitudes()

# print(prueba: ',prediccion(1,5))

# iid=5
# uid = 2
# votadas = bbdd.votadas(uid)
# noVotadas =bbdd.noVotadas(uid) 

# for i in bbdd.noVotadas(uid):
#     print(prediccion(uid,i))

# sim(1,3)
# print(round(sim(1,3),2))
# la 1 y la 14
# la 1 y la 3
# la 1 y la 456
# la 1 y la 6547 pensarla

# print(round(prediccion(147,1,),2))
# usuario 53
