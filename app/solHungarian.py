from munkres import *

def Enter_MatrizCosto(n):
    matriz = []
    for i in range(n):
        array = []
        for j in range(n):
            array.append(int(input(f"Ingrese un valor para {i} {j}: ")))
        matriz.append(array)
    return matriz

def Aplicar_Metodo(matriz):

    m = Munkres()

    asignaciones = m.compute(matriz)

    asignacionOptima = []
    cost_total = 0

    for row, col in asignaciones:
        costo = matriz[row][col]
        asignacionOptima.append((row, col))
        cost_total += costo
    
    return asignacionOptima, cost_total

