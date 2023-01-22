import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def valida_entradas(i: int = 0, j: int = 0, flag: int = 2) -> int:
    resul: int = 1
    if flag==0:
        while resul % 2 != 0:
            while True:
                try:
                    resul = int(input(
                        "Ingrese la entrada M[{0}][{1}] (Esta debe ser par): ".format(str(i + 1), str(j + 1))))
                    break
                except:
                    print("¡No es un valor valido!")
        return resul
    elif flag == 1:
        while True:
            try:
                resul = int(input("Ingrese la entrada M[{0}][{1}]: ".format(str(i + 1), str(j + 1))))
                return resul
            except:
                print("¡No es un valor valido!")
    elif flag == 2:
        while True:
            try:
                resul = int(input("Ingrese el número de vértices del grafo: "))
                return resul
            except:
                print("¡No es un valor valido! Ingrese un número Natural o 0")

def lee_matriz():
    """
    Esta función crea una matriz de adyacencia de un grafo.
    Solicita el triángulo inferior de la matriz unión la diagonal
    y luego copia los valores para hacerla simétrica.
    :return: Matriz leída
    """
    n = valida_entradas()
    M = np.array([[-1] * n for i in range(n)])
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                M[i][j] = valida_entradas(i, j, 0)
            else:
                M[i][j] = valida_entradas(i, j, 1)
            if i > j:
                M[j][i] = M[i][j]
    return M

def elimina_bucles(M):
    """
    Esta función elimina los bucles de una matriz de adyacencia.
    :params M: Matriz a la que se le eliminan las diagonales.
    """
    for i in range(len(M)):
        M[i][i] = 0

def elimina_multiaristas(M:np.array):
    """
    Esta función elimina las multiaristas de una matriz de adyacencia.
    :params M: Matriz a la que se le eliminan las diagonales.
    """
    M[M>0] = 1
        
def escribe_matriz(M):
    """
    Esta función dibuja la matriz M.
    :param M: Matriz a dibujar.
    """
    print("Matriz de adyacencia")
    for i in range(len(M)):
        print('[', end='')
        for j in range(len(M[i])):
            print('{:^3n}'.format(M[i][j]), end='')
        print(']')

def generador_vertices(MA: np.array):
    return np.array(range(len(MA)))

def generador_aristas(MA: np.array):
    edges = []
    for i in range(len(MA)):
        for j in range(i+1):
             if MA[i][j] != 0:
                 edges.append((i,j))
    return edges

def empareja_colores(grafo_coloreado: dict, lista_colores: list):
    llaves = [k for k in grafo_coloreado.keys()]
    valores = [k for k in grafo_coloreado.values()]
    colores = [[llaves[i],lista_colores[valores[i]]] for i in range(len(llaves))]
    return colores

def dibuja_grafo(edges, vertices, node_color: list):
    G = nx.Graph()
    pos = nx.spring_layout(G, seed=3113794652) 
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    if node_color != None:
        color_map = ['' for i in range(len(vertices))]
        for i in range(len(vertices)):
            for j in range(len(node_color)):
                if i == node_color[j][0]:
                    color_map[i] = node_color[j][1]
                elif color_map[i] == '':
                    color_map[i]='#000000'
        nx.draw(G, node_color = color_map)
    else:
        nx.draw(G, with_labels = True)

def color_aleatorio():
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

def colores_aleatorios(number_of_colors):
    colores = [color_aleatorio() for i in range(number_of_colors)]
    return colores

def colorear(M):
  coloracion = {0:0}
  for i,v in enumerate(M):
    c = 0
    adyacentes = filter(lambda e: (e[1]>0),enumerate(v))
    adyacentes = list(adyacentes)
    adyacentes = [a[0] for a in adyacentes]
    cols = [coloracion[ver] for ver in adyacentes if ver in coloracion.keys()]
    cols.sort()
    for j,a in enumerate(cols): 
      if j != a:
        c = j
        break
      c += 1
    coloracion[i]=c
  return coloracion

if __name__ == "__main__":
    M = [
    [0,1,1,1,1,1,1],
    [1,0,1,1,0,0,1],
    [1,1,0,0,1,1,0],
    [1,1,0,0,1,0,0],
    [1,0,1,1,0,1,1],
    [1,0,1,0,1,0,1],
    [1,1,0,0,1,1,0],
      ]
    M2 = [
    [0,1,1,1],
    [1,0,0,1],
    [1,0,0,0,],
    [1,1,0,0,],
      ]
    dict_col = colorear(M)
    m = len(set(dict_col.values()))
    M = np.array([np.array(v) for v in M])
    lc = colores_aleatorios(len(M))
    print(empareja_colores(dict_col, lc))
    dibuja_grafo(generador_aristas(M),generador_vertices(M),empareja_colores(dict_col, lc))