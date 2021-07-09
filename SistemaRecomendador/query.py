import csv
import sqlite3

def insertarDatos():
    #Conexion con el archivo de base de datos
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()

    cont = 0 #evitar linea 1 del csv
    #comprobamos si la tabla ya tiene datos insertados
    conteo = cur.execute('SELECT * FROM movie')
    # print(len(conteo.fetchall()))
    if len(conteo.fetchall())<=0:
        #se procede a la insercion de los datos tras leer el csv
        with open('ml-latest-small\movies.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                print(', '.join(row)) #devolvemos la linea leida
                if cont == 0: #para evitar la primera línea del csv
                    cont += 1
                else: #parseamos la columna e insertamos
                    movieId = int(row[0])
                    title = row[1]
                    genres = row[2]

                    cur.execute("INSERT INTO movie VALUES(?,?,?)", (movieId,title,genres))
                
        con.commit() #reflejamos los datos en el archivo .db
        print("\nLa información de las peliculas ya ha sido cargada\n")
    else:
        print("La información de las películas ya habia sido cargada\n")

    #  Para añadir id del tmdb
    cont = 0
    error = 0
    with open('ml-latest-small\links.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            # print(', '.join(row)) #devolvemos la linea leida
            if cont == 0: #para evitar la primera línea del csv
                cont += 1
            else: #parseamos la columna e insertamos
                try:
                    movieId = int(row[0])
                    # title = row[1]
                    tmdb = int(row[2])
                    
                except:
                    error +=1
                    tmdb=0
                cur.execute("UPDATE movie SET tmdbId = ? WHERE movieId = ?", (tmdb,movieId))
                
    # print(error)        
    con.commit() #reflejamos los datos en el archivo .db
    
    # comprobamos si la tabla ya tiene datos insertados
    conteo = cur.execute('SELECT * FROM rating')
    # print(len(conteo.fetchall()))
    if len(conteo.fetchall())<=0:
        cont = 0 #evitar linea 1 del csv
        #se procede a la insercion de los datos tras leer el csv
        with open('ml-latest-small\/ratings.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                print(', '.join(row)) #devolvemos la linea leida
                if cont == 0: #para evitar la primera línea del csv
                    cont += 1
                else: #parseamos la columna e insertamos
                    userId = int(row[0])
                    movieId = int(row[1])
                    rating = float(row[2])
                    timestamp = int(row[3])

                    cur.execute("INSERT INTO rating(userId,movieId,rating,timestamp) VALUES(?,?,?,?)", (userId,movieId,rating,timestamp))
        con.commit() #reflejamos los datos en el archivo .db
        print("La información de las valoraciones ya ha sido cargada\n")
    else:
        print("La información de las valoraciones ya habia sido cargada\n")

    con.close() #cerramos la conexion con la bbdd

#-------------------------------------------------------------------------------------------
def votadas(uid):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    conteo = cur.execute('SELECT movieId, rating FROM rating WHERE rating.userId = ?',(uid,))
    lista = []
    for (item) in cur:
        lista.append((item[0],item[1]))
        # print(movieId)
    con.close()
    return lista

def noVotadas(uid):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute('select movieId from rating WHERE rating.userId <> ? EXCEPT SELECT movieId FROM rating WHERE rating.userId = ?', (uid,uid))
    lista = []
    for (movieId) in cur:
        lista.append(movieId[0])
        # print(movieId)
    con.close()
    return lista

def noVotadasCombo(uid):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute('select movieId from rating WHERE rating.userId <> ? EXCEPT SELECT movieId FROM rating WHERE rating.userId = ?', (uid,uid))
    lista = []
    for (movieId) in cur:
        lista.append(str(movieId[0]))
        # print(movieId)
    con.close()
    return lista

def sameEnergy(mid1, mid2):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute('SELECT rating, userId FROM rating WHERE movieId=? AND userId IN (SELECT userId FROM rating WHERE movieId=?)', (mid1,mid2))
    lista = []
    for (item) in cur:
        lista.append((item[0],item[1]))
    con.close()
    return lista

def commonFilms(sentencia):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute(sentencia)
    lista = []
    for (item) in cur:
        lista.append(item[0])
        # print(lista)
    con.close()
    return lista

def media(sentencia):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute(sentencia)
    result=0
    for (item) in cur:
        result = item[0]
    # print(result)
    con.close()
    return result

def getUsers():
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute("SELECT userId FROM rating GROUP BY userId;")
    lista = []
    for (item) in cur:
        lista.append(str(item[0]))
    con.close()
    return lista

# def getMovies():
#     try:
#         con = sqlite3.connect('bbdd/movielens.db')
#     except:
#         print("No conectado")
#     cur = con.cursor()
#     cur.execute("SELECT movieId, title FROM movie;")
#     lista = []
#     for (item) in cur:
#         lista.append((item[0],item[1]))
#     con.close()
#     return lista

def getMovies():
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute("SELECT movieId FROM movie;")
    lista = []
    for (item) in cur:
        lista.append(str(item[0]))
    con.close()
    return lista

def insertSim(sim,p1,p2):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    cur.execute("INSERT INTO similitudes(p1,p2,similitud) VALUES (?,?,?)",(p1,p2,sim))
    con.commit()
    con.close()

def selectSim(p1,p2):
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    value = 10
    cur.execute("select similitud from similitudes where p1=? and p2=?",(p1,p2))
    for (item) in cur:
        value = item[0]
    print(value)
    con.close()
    return value
    
def moviesNoOpinion():
    try:
        con = sqlite3.connect('bbdd/movielens.db')
    except:
        print("No conectado")
    cur = con.cursor()
    value = 10
    cur.execute("select movie.movieId from movie EXCEPT select rating.movieId from rating GROUP  by movieId")
    lista = []
    for (item) in cur:
        lista.append(str(item[0]))
    con.close()
    return lista

# similitudBBDD(2,3)
