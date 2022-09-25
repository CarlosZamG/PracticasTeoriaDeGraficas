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
        vecinos.append(dict([("vecinos", vecinos_vj.copy())]))
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


def valida_entradas(i:int, j:int, flag: bool) -> int:
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


def generar_árbol_anchura(M):
    conectados = [0]
    n = len(M)
    MA = [[0 for i in range(n)] for i in range(n)]
    #dibuja_matriz(MA)
    while len(conectados) != n:
      
      for c in conectados:
        idx=0
        for i in M[c]:
          if i != 0 and idx not in conectados:
            conectados.append(idx)
            #print(f"c:{c} index:{idx} ")
            MA[c][idx] = 1
            MA[idx][c] = 1
            
            #print(MA)
          idx += 1 
    #print(conectados) 
    return MA

M = lee_matriz()
print("Matriz ingresada")
dibuja_matriz(M)
elimina_bucles(M)
print("Matriz sin loops")
dibuja_matriz(M)
AM = generar_árbol_anchura(M)
print("Matriz de adyacencia del árbol generado")
dibuja_matriz(AM)
