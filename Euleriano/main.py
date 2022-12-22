import sys

def simplificar_grafo(M):
  n = len(M)
  for i in range(n):
        for j in range(i + 1):
            if i == j:
                M[i][j] = 0
            elif M[i][j] != 0:
                M[i][j] = 1
                M[j][i] = 1
            


def eliminar_loops(M):
  n = len(M)
  for i in range(n):
    M[i][i] = 0


def dijkstra(MA,origen, destino):
  """
  Función modificada del Algoritmo de Dijkstra

  Recibe como parámetros:
    - MA: La matriz de adyacencia de la gráfica
    - origen: El índice en del vértice de origen en MA
    - destino: El índice en del vértice de destino en MA

  Retorna una lista con los índices de los vértices que forman el camino del vértice de origen al de destino 
  """
  vertices = list(range(len(MA)))
  marcados = []
  no_marcados = vertices.copy()
  info_vertices=[ {"v": v ,"camino":[vertices[origen]], "tiempo":sys.maxsize} for v in vertices]
  
  info_vertices[origen]["tiempo"] = 0
  marcados.append(vertices[origen])
  del no_marcados[vertices.index(marcados[-1])]

  
  while vertices[destino] not in marcados:
    act =  marcados[-1]

    for pos,j in enumerate(MA[act]):
      if j != 0:
        t = info_vertices[act]["tiempo"] + j
        if info_vertices[pos]["tiempo"] > t:
          info_vertices[pos]["tiempo"] = t
          info_vertices[pos]["camino"] = info_vertices[act]["camino"].copy()
          info_vertices[pos]["camino"].append(vertices[pos])

    minimo = sys.maxsize

    for nm in no_marcados:
      idx_nuevo = vertices.index(nm)
      t = info_vertices[idx_nuevo]["tiempo"]
      if t < minimo:
        minimo = t
        act = nm

    marcados.append(act)
    no_marcados.remove(act)   
  
  return info_vertices[destino]["camino"]

def c_euleriano_sin_loops(MA):
  """
  Función que devuelve el circuito Euleriano de una gráfica sin loops
  
  Recibe como parámetros:
    - MA: La matriz de adyacencia de la gráfica

  Devuelve una lista con los vértices que hay que ir uniendo para completar el ciclo
  """

  # Revisamos que la gráfica tenga aristas, en caso de que no haya aristas devuelve una lista vacía. Es nuestra base de la recursividad
  sum_aristas = sum([sum(v) for v in MA]) 
  if sum_aristas == 0:
    return []

  # Elegimos dos vértices adyacentes sobre los cuales vamos a construir el ciclo
  for i,v in enumerate(MA):
    grad = sum(v)
    if grad > 0:
      origen = i
      for j,valor in enumerate(MA[i]):
        if valor > 0:
          destino = j
          break
      break

  # Creamos una matriz provisional quitando una arista que une a nuestros vértices de origen y destino   
  MatProv = [f.copy() for f in MA]
  MatProv[origen][destino] -= 1
  MatProv[destino][origen] -= 1
  simplificar_grafo(MatProv)
  C = dijkstra(MatProv,origen,destino)
  # Hacemos nuestro ciclo usando dijkstra y la matriz provisional 

  # Creamos otra matriz provisional(MP2) a la que le quitamos las aristas del ciclo
  MP2 = [f.copy() for f in MA]
  for i,v1 in enumerate(C):
    j = (i + 1) % len(C)
    v2 = C[j]
    MP2[v1][v2] -= 1
    MP2[v2][v1] -= 1

  # Creamos el circuito Euleriano de  MP2
  C_euler = c_euleriano_sin_loops(MP2)
  if len(C_euler) == 0:
    return C

  # Vemos el vértice en común de nuestros dos circuitos para poder unirlos
  posC = 0
  posCE = 0
  for i,v in enumerate(C):
    for j, v_e in enumerate(C_euler):
      if v == v_e:
        posC = i
        posCE = j
        break 
  C = C[posC:] + C[:posC]
  C_euler = C_euler[posCE:] + C_euler[:posCE]
  
  return C + C_euler

def circuito_euleriano(MA):
  n = len(MA) 
  MatProv = [f.copy() for f in MA]
  eliminar_loops(MatProv)
  c_euler = c_euleriano_sin_loops(MatProv)
  for i in range(n):
    v = MA[i][i] // 2
    agregado =  [i]*v
    j = c_euler.index(i)
    c_euler = c_euler[:j] + agregado + c_euler[j:]

  return c_euler  

def trayectoria_euleriana(MA,i,j):
  MA[i][j] += 1
  MA[j][i] += 1
  C = circuito_euleriano(MA)
  for n in range(1,len(C)):
    if (C[n-1] == j and  C[n] == i) or (C[n-1] == i and  C[n] == j):
      T = C[n:] + C[:n]

  return T

def grado(vertice):
  return sum(vertice)

def lista_grados(MA):
  grados = []
  for vertice in MA:
    grados.append(grado(vertice))
  return grados

def filtrar_impares(tupla):
  if tupla[1] % 2 != 0:
    return tupla[0]

def verificadora(MA):
  
  impares = list(map(filtrar_impares, list(enumerate(lista_grados(MA))))) 
  impares = list(filter(lambda x:x!=None, impares))
  
  return impares

def testflow(MA):
  impares = verificadora(MA)
  eu = len(impares)
  if eu == 0:
    print("La matriz es Euleriana")
    print(circuito_euleriano(MA))
  elif eu == 2:
    print("La matriz es debilmente Euleriana")
    print(trayectoria_euleriana(MA,impares[0],impares[1]))
  else:
    print("La matriz no es euleriana")


def run():

    print("\nPrimera prueba:")
    ME=[
    [0,1,0,1,0,0,0,0,0],
    [1,0,1,1,1,0,0,0,0],
    [0,1,0,0,0,1,0,0,0],
    [1,1,0,0,1,0,1,0,0],
    [0,1,0,1,0,1,0,1,0],
    [0,0,1,0,1,0,0,1,1],
    [0,0,0,1,0,0,0,1,0],
    [0,0,0,0,1,1,1,0,1],
    [0,0,0,0,0,1,0,1,0],
    ]
    
    testflow(ME) 

    print("\nSegunda prueba:")
    n = 5
    Kn = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        Kn[i][i] = 0
    
    testflow(Kn)

    print("\nTercera prueba:")
    Tn = [[0 for i in range(n)] for j in range(n)]
    for i in range(n-1):
      Tn[i][i+1] = 1
      Tn[i+1][i] = 1
    
    testflow(Tn) 

    print("\nCuarta prueba:")
    n = 4
    Kn = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        Kn[i][i] = 0
    
    testflow(Kn)

  
    print("\nQuinta prueba:")
    ME = [
          [0,1,0,0,3],
          [1,0,2,0,1],
          [0,2,0,1,1],
          [0,0,1,0,1],
          [3,1,1,1,0],
          ]
    testflow(ME)

    print("\nSexta prueba")
    ME = [
        [0,2,0,0,0,2],
        [2,0,2,0,0,0],
        [0,2,0,2,0,0],
        [0,0,2,0,2,0],
        [0,0,0,2,0,2],
        [2,0,0,0,2,0],
        ]

    testflow(ME)

    print("\n7ma prueba")
    ME = [
          [2,2],
          [2,0]
          ]
    
    testflow(ME)

    print("\n8va prueba")
    MD = [[0,1,0,1,1],
          [1,0,1,0,2],
          [0,1,0,1,1],
          [1,0,1,0,2],
          [1,2,1,2,0],]

    testflow(MD)


if __name__=="__main__":
    run()