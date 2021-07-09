from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem
import algoritmo
import query
import notas

def insertarComboBox(combobox, usuarios):
    combobox.addItems(usuarios)

def insertarComboBoxDupla(combobox, user):
    peliculas = query.noVotadasCombo(user)
    peliculasNoOpi = query.moviesNoOpinion()
    for i in peliculasNoOpi:
        peliculas.append(i)
    # peliculas.sort()
    combobox.addItems(peliculas)

# def insertarTabla(tabla, datos, filas):
#     tabla.setRowCount(filas)
#     for fila in range(0, len(datos)):
#         for columna in range(0, len(datos[0])):
#             tabla.setItem(fila, columna, QTableWidgetItem(datos[fila][columna]))

def insertarRecomendaciones(tabla, usuario, umbral, vecinos):
    noValoradas = query.noVotadas(usuario)
    if vecinos != '': #si la casilla de vecinos tiene releno se ejecuta el ranking de forma predeterminada
        recomendaciones = algoritmo.recomendacionesVecinos(usuario, int(vecinos))
        for fila in range(0, len(noValoradas)):
            for columna in range(0, 1):
                tabla.setItem(fila, columna, QTableWidgetItem(recomendaciones[fila][columna]))
    else: 
        if umbral =='': # de forma predeterminada al dar el boton se hace el umbral para para todos
            umbral = -1
        # si se ha introducido un umbral (y no un vecindario), se calcula con el valor introducido
        recomendaciones = algoritmo.recomendacionesUmbral(usuario, float(umbral))
        for fila in range(0, len(noValoradas)):
            for columna in range(0, 1):
                tabla.setItem(fila, columna, QTableWidgetItem(recomendaciones[fila][columna]))

def mostrarPrediccion(prediccion, usuario, pelicula):
    prediccion.setText("")
    # peliculasNoOpi = query.moviesNoOpinion()
    prediccion.setText(str(algoritmo.prediccion(usuario, pelicula, )))
    # prediccion.setText(str(notas.recomendacionExt(pelicula) + " TMDB"))
    
    
