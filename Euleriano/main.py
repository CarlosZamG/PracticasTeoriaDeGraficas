import sys

def simplificar_grafo(M: list):
    '''
    Esta función simplica la gráfica con matriz de adyacencia M.

    :param M: Matriz de adyacencia de la gráfica
    '''
    n: int = len(M)
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                M[i][j] = 0
            elif M[i][j] != 0:
                M[i][j] = 1
                M[j][i] = 1

def eliminar_loops(M: list):
    '''
    Esta función elimina los loops de la gráfica con matriz de adyacencia M.

    :param M: Matriz de adyacencia de la gráfica.
    '''
    n: int = len(M)
    for i in range(n):
        M[i][i] = 0

def dijkstra(MA: list, origen: int, destino: int):
    '''
    Esta función determina el camino más corto en la gráfica con matriz de adyacencia MA entre el
    origen y el destino.

    :param MA: Matriz de adyacencia de la gráfica.
    :param origen: Vértice de origen.
    :param destino: Vértice de destino.
    :return: Lista con los vértices del camino.
    '''
    vertices: list = list(range(len(MA)))
    marcados: list = []
    no_marcados: list = vertices.copy()
    info_vertices: list = [{"v": v, "camino": [vertices[origen]], "tiempo": sys.maxsize} for v in vertices]
    info_vertices[origen]["tiempo"] = 0
    marcados.append(vertices[origen])
    del no_marcados[vertices.index(marcados[-1])]
    while vertices[destino] not in marcados:
        act = marcados[-1]
        for pos, j in enumerate(MA[act]):
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

def c_euleriano_sin_loops(MA: list) -> list:
    '''
    Esta función determina el circuito euleriano de la gráfica con matriz de adyacencia MA eliminando loops.

    :param MA: Matriz de adyacencia de la gráfica.
    :return: Lista con los vértices del circuito euleriano.
    '''

    # Revisamos que la gráfica tenga aristas, en caso de que no haya aristas devuelve una lista vacía. Es nuestra base de la recursividad
    sum_aristas: int = sum([sum(v) for v in MA])
    if sum_aristas == 0:
        return []

    # Elegimos dos vértices adyacentes sobre los cuales vamos a construir el ciclo
    for i, v in enumerate(MA):
        grad = sum(v)
        if grad > 0:
            origen = i
            for j, valor in enumerate(MA[i]):
                if valor > 0:
                    destino = j
                    break
            break

    # Creamos una matriz provisional quitando una arista que une a nuestros vértices de origen y destino
    MatProv: list = [f.copy() for f in MA]
    MatProv[origen][destino] -= 1
    MatProv[destino][origen] -= 1
    simplificar_grafo(MatProv)
    C: list = dijkstra(MatProv, origen, destino)
    # Hacemos nuestro ciclo usando dijkstra y la matriz provisional

    # Creamos otra matriz provisional(MP2) a la que le quitamos las aristas del ciclo
    MP2: list = [f.copy() for f in MA]
    for i, v1 in enumerate(C):
        j = (i + 1) % len(C)
        v2 = C[j]
        MP2[v1][v2] -= 1
        MP2[v2][v1] -= 1

    # Creamos el circuito Euleriano de  MP2
    C_euler: list = c_euleriano_sin_loops(MP2)
    if len(C_euler) == 0:
        return C

    # Vemos el vértice en común de nuestros dos circuitos para poder unirlos
    posC: int = 0
    posCE: int = 0
    for i, v in enumerate(C):
        for j, v_e in enumerate(C_euler):
            if v == v_e:
                posC = i
                posCE = j
                break
    C = C[posC:] + C[:posC]
    C_euler = C_euler[posCE:] + C_euler[:posCE]

    return C + C_euler

def imprimir_trayectoria(T: list) -> None:
    '''
    Esta función imprime los vértices que hay que seguir para trazar la trayectoria T descrita sobre la gráfica.

    :param T: Lista de vértices de la trayectoria.
    :return: None
    '''
    n: int = len(T)
    for i in range(n):
        print(f"v{T[i] + 1} ->", end=" ") if i < n - 1 else print(f"v{T[i] + 1}")

def circuito_euleriano(MA: list) -> list:
    '''
    Esta función determina el circuito euleriano de la gráfica con matriz de adyacencia MA.

    :param MA: Matriz de adyacencia de la gráfica.
    :return: Lista con los vértices del circuito euleriano.
    '''
    n: int = len(MA)
    MatProv: list = [f.copy() for f in MA]
    eliminar_loops(MatProv)
    c_euler: list = c_euleriano_sin_loops(MatProv)
    for i in range(n):
        v: int = MA[i][i] // 2
        agregado: list = [i] * v
        j: int = c_euler.index(i)
        c_euler = c_euler[:j] + agregado + c_euler[j:]
    return c_euler

def camino_euleriano(MA: list, i: int, j: int) -> list:
    '''
    Esta función determina el camino euleriano de la gráfica con matriz de adyacencia MA con inicio i y fin j.

    :param MA: Matriz de adyacencia de la gráfica.
    :param i: Índice de inicio.
    :param j: Índice de fin.
    :return: Lista con vértices del camino euleriano.
    '''
    MA[i][j] += 1
    MA[j][i] += 1
    T: list = []
    C: list = circuito_euleriano(MA)
    for n in range(1, len(C)):
        if (C[n - 1] == j and C[n] == i) or (C[n - 1] == i and C[n] == j):
            T = C[n:] + C[:n]
    return T

def grado(vertice: list) -> int:
    '''
    Esta función determina el grado de un vértice de la gráfica.

    :param vertice: Lista de adyacencia del vértice.
    :return: Grado del vértice.
    '''
    return sum(vertice)

def lista_grados(MA: list) -> list:
    '''
    Esta función devuelve la lista de grados de una gráfica con matriz de adyacencia MA.

    :param MA: Matriz de adyacencia de la gráfica.
    :return: Lista de grados de la gráfica.
    '''
    return list(map(sum, MA))

def filtrar_impares(tupla: tuple) -> int:
    '''
    Esta función determina los elementos impares de una lista.

    :param tupla: tupla de la forma (v,g) donde v es el índice del vértice y g es el grado 
    :return: el  vértice impar.
    '''
    if tupla[1] % 2 != 0:
        return tupla[0]

def verificadora(MA: list) -> list:
    '''
    Esta función determina los vértices de grado impar de la gráfica con matriz de adyacencia MA.

    :param MA: Matriz de adyacencia de la gráfica.
    :return: Lista de vértices de grado impar de la gráfica.
    '''
    impares: list = list(map(filtrar_impares, list(enumerate(lista_grados(MA)))))
    impares = list(filter(lambda x: x != None, impares))
    return impares

def lee_matriz():
    """
    Esta función crea una matriz de adyacencia de un grafo.
    Solicita el triángulo inferior de la matriz unión la diagonal
    y luego copia los valores para hacerla simétrica.
    :return: Matriz leída
    """
    n = int(input("Ingrese el número de vértices del grafo: "))
    M = [[-1] * n for i in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                M[i][j] = valida_entradas(i, j, 1)
            else:
                M[i][j] = valida_entradas(i, j, 0)
            if i > j:
                M[j][i] = M[i][j]
    return M

def valida_entradas(i:int, j:int, flag: int) -> int:
    resul: int = 1
    if flag == 1:
        while resul % 2 != 0:
            while True:
                try:
                    resul = int(input(
                        "Ingrese la entrada M[{0}][{1}] (Esta debe ser par): ".format(str(i + 1), str(j + 1))))
                    break
                except:
                    print("¡No es un valor valido!")
        return resul
    elif flag == 0:
        while True:
            try:
                resul = int(input("Ingrese la entrada M[{0}][{1}]: ".format(str(i + 1), str(j + 1))))
                return resul
            except:
                print("¡No es un valor valido!")
    elif flag == 2:
        while True:
            try:
                resul = int(input("Ingrese un número 1 si desea aplicar busqueda en anchura y un 2 si desea aplicar busqueda en profundidad: "))
                if 0<resul and resul<3:
                    return resul
                else:
                    raise Exception("¡No es un valor valido!")
            except:
                print("¡No es un valor valido!")
    elif flag == 3:
        while True:
            try:
                resul = int(input("Ingrese un número 1 si desea buscar otro árbol y un 2 si desea salir: "))
                if resul == 1:
                    return True
                if resul == 2:
                    return False
                else:
                    raise Exception("¡No es un valor valido!")
            except:
                print("¡No es un valor valido!")


def mainflow(MA: list) -> None:
    '''
    Esta función determina si la gráfica con matriz de adyacencia MA es euleriana, débilmente euleriana o ninguna.

    :param MA: Matriz de adyacencia de la gráfica.
    :return: None
    '''
    impares: list = verificadora(MA)
    eu: int = len(impares)
    if eu == 0:
        print("La matriz es Euleriana")
        C = circuito_euleriano(MA)
        C = C + [C[0]]
        imprimir_trayectoria(C)
    elif eu == 2:
        print("La matriz es débilmente Euleriana")
        imprimir_trayectoria(camino_euleriano(MA, impares[0], impares[1]))
    else:
        print("La matriz no es Euleriana, ni débilmente Euleriana")


def test() -> None:
    '''
    Función para probar mainflow()
    :return: None
    '''
    print("\nPrimera prueba:")
    ME = [
        [0, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 1, 0],
    ]

    mainflow(ME)

    print("\nSegunda prueba:")
    n = 5
    Kn = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        Kn[i][i] = 0

    mainflow(Kn)

    print("\nTercera prueba:")
    Tn = [[0 for i in range(n)] for j in range(n)]
    for i in range(n - 1):
        Tn[i][i + 1] = 1
        Tn[i + 1][i] = 1

    mainflow(Tn)

    print("\nCuarta prueba:")
    n = 4
    Kn = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        Kn[i][i] = 0

    mainflow(Kn)

    print("\nQuinta prueba:")
    ME = [
        [0, 1, 0, 0, 3],
        [1, 0, 2, 0, 1],
        [0, 2, 0, 1, 1],
        [0, 0, 1, 0, 1],
        [3, 1, 1, 1, 0],
    ]
    mainflow(ME)

    print("\nSexta prueba")
    ME = [
        [0, 2, 0, 0, 0, 2],
        [2, 0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0, 0],
        [0, 0, 2, 0, 2, 0],
        [0, 0, 0, 2, 0, 2],
        [2, 0, 0, 0, 2, 0],
    ]

    mainflow(ME)

    print("\n7ma prueba")
    ME = [
        [2, 2],
        [2, 0]
    ]

    mainflow(ME)

    print("\n8va prueba")
    MD = [[0, 1, 0, 1, 1],
          [1, 0, 1, 0, 2],
          [0, 1, 0, 1, 1],
          [1, 0, 1, 0, 2],
          [1, 2, 1, 2, 0], ]

    mainflow(MD)

if __name__ == "__main__":
    M = lee_matriz()
    mainflow(M)