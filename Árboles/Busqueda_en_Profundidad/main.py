"""
Teoría de grafos 3AM1
Equipo COP

Escamilla Huerta Porfirio Damián
García Porfirio Omar
Zamora Gutierrez Carlos David
"""


def dibuja_matriz(M):
    """
    Esta función dibuja la matriz M.
    :param M: Matriz a dibujar.
    """
    for i in range(len(M)):
        print('[', end='')
        for j in range(len(M[i])):
            print('{:^3n}'.format(M[i][j]), end='')
        print(']')


def elimina_bucles(M):
    """
    Esta función elimina los bucles de una matriz de adyacencia.
    :params M: Matriz a la que se le eliminan las diagonales.
    """
    n = len(M)
    for i in range(n):
        M[i][i] = 0


def crea_vértices(M):
    """
    Esta función crea los vértices de la matrás de adyacencia.
    :params M: Matriz de la que se extraen los vértices.
    :return: Retorna una lista con los vértices en forma de diccionario.
    """
    n = len(M)
    vértices = []
    vecinos = []
    vecinos_vj = []
    for i in range(n):
        for j in range(n):
            if M[i][j] != 0:
                vecinos_vj.append(j + 1)
        vecinos.append(vecinos_vj.copy())
        vecinos_vj.clear()
    for i in range(n):
        vértices.append(dict([("vértice", i + 1), ("vecinos", vecinos[i]), ("conectado", False)]))
    return vértices


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
                M[i][j] = valida_entradas(i, j, True)
            else:
                M[i][j] = valida_entradas(i, j, False)
            if i > j:
                M[j][i] = M[i][j]
    return M


def valida_entradas(i: int, j: int, flag: bool) -> int:
    """
    Esta función valida las entradas de la matriz
    :return: La entrada de la matriz_{i,j}
    """
    resul: int = 1
    if flag:
        while resul % 2 != 0:
            while True:
                try:
                    resul = int(input(
                        "Ingrese la entrada M[{0}][{1}] (Esta debe ser par): ".format(str(i + 1), str(j + 1))))
                    break
                except:
                    print("¡No es un valor valido!")
        return resul
    else:
        while True:
            try:
                resul = int(input("Ingrese la entrada M[{0}][{1}]: ".format(str(i + 1), str(j + 1))))
                return resul
            except:
                print("¡No es un valor valido!")

def generar_árbol_profundidad(M):
    V = set()  # Conjunto de vértices ya conectados
    Vaux = set()  # Conjunto de vertices auxiliar
    vecino = 0  # Vecino más pequeño
    Pila = []  # Pila auxiliar
    n = len(M)  # Número de vértices
    MA = [[0 for i in range(n)] for i in range(n)]  # Matriz de adyacencia
    vertices = crea_vértices(M)
    Pila.append(1)
    V.add(1)
    while len(Pila) != 0:  # Acaba cuando la pila está vacía
        u = Pila[-1]  # Tomamos el último elemento de la pila
        Vaux = set(vertices[u - 1].get("vecinos"))  # Obtenemos el conjunto de vertices no conectados a u
        if len(Vaux - V) > 0:  # Si hay al menos un vecino no conectado a u
            vecino = min(Vaux - V)  # Tomamos el vertice no conectado más pequeño
            MA[u - 1][vecino - 1] = 1  # Los conectamos
            MA[vecino - 1][u - 1] = 1
            if vecino not in Pila:  # Si el vecino no estaba en la pila, lo agregamos
                Pila.append(vecino)
            V.add(vecino)  # Agregamos al vecino al conjunto de vertices ya conectados
        else:
            Pila.remove(u)  # Si u no tiene vecinos sin conectar, lo quitamos de la pila
    Pila.clear()
    V.clear()
    Vaux.clear()
    return MA


M = lee_matriz()
print("Matriz ingresada")
dibuja_matriz(M)
elimina_bucles(M)
print("Matriz sin loops")
dibuja_matriz(M)
AM = generar_árbol_profundidad(M)
print("Matriz de adyacencia del árbol generado por profundidad")
dibuja_matriz(AM)
