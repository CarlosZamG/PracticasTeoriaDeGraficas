"""
Teoría de grafos 3AM1
Equipo COP 

Escamilla Huerta Porfirio Damián
García Porfirio Omar
Zamora Gutierrez Carlos David
"""


class Vértice:
    """
    Este objeto, representa a los vértices del grafo,
    tiene un arreglo de vértices vecinos y un booleano
    que indica si está conectado o no.
    """
    conteo = 0

    def __init__(self, vecinos, conectado=False):
        self.vecinos = vecinos
        self.conectado = conectado
        self.conteo += 1


def lee_matriz():
    """
    Esta función crea una matriz de adyacencia de un grafo solicitando las entradas a_{i,j} con i >= j.
    :return: Matriz leída
    """
    n = int(input("Ingrese el número de vértices del grafo: "))
    M = [[-1] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i >= j:
                if i == j:
                    while M[i][j]%2 != 0:
                        M[i][j] = int(input("Ingrese la entrada M[{0}][{1}] (Esta debe ser par): ".format(str(i + 1), str(j + 1))))
                else:
                    M[i][j] = int(input("Ingrese la entrada M[{0}][{1}]: ".format(str(i + 1), str(j + 1))))
                if i > j:
                    M[j][i] = M[i][j]
    return M


def dibuja_matriz(M):
    """
    Esta función dibuja la matriz M
    :param M: Matriz a dibujar
    :return: Output
    """
    for i in range(len(M)):
        print('[', end='')
        for j in range(len(M[i])):
            print('{:^3n}'.format(M[i][j]), end='')
        print(']')


def elimina_bucles(M):
    n=len(M)
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i][j] = 0


M = lee_matriz()
print("Matriz leida")
dibuja_matriz(M)
elimina_bucles(M)
print("Matriz sin loops")
dibuja_matriz(M)
