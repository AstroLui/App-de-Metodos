from pulp import *

def Enter_MatrizCosto(n, m):
    matriz = []
    for i in range(n):
        array = []
        for j in range(m):
            array.append(int(input(f"Ingrese un valor para {i} {j}: ")))
        matriz.append(array)
    return matriz

def Enter_Demanda_Oferta(n, m):
    oferta = []
    demanda = []
    for i in range(n):
        oferta.append(int(input(f"{i} Oferta: ")))
    for j in range(m):
        demanda.append(int(input(f"{j} Demanda: ")))
    return oferta, demanda
        
def Start(matriz, oferta, demanda, n, m, modo):

    totalOferta = sum(oferta)
    totalDemanda = sum(demanda)
    if totalOferta != totalDemanda:
        if totalOferta>totalDemanda:
            for fila in matriz:
                fila.append(0)
            m += 1
            valorFaltante = totalOferta-totalDemanda
            demanda.append(valorFaltante)
        else:
            matriz.append([0 for _ in range(m + 1)])
            n += 1
            valorFaltante = totalDemanda-totalOferta
            oferta.append(valorFaltante)
    mode = pulp.const.LpMinimize if(modo == "min") else pulp.const.LpMaximize
    prob = pulp.LpProblem("Problema de Trasnporte", mode)
    variables = pulp.LpVariable.dicts("Rutas",[(i,j) for i in range(n) for j in range(m)], lowBound=0)
    prob += pulp.lpSum(variables[(i, j)] * matriz[i][j] for i in range(n) for j in range(m))

    for i in range(n):
        prob += pulp.lpSum(variables[(i, j)] for j in range(m)) == oferta[i]

    for j in range(m):
        prob += pulp.lpSum(variables[(i, j)] for i in range(n)) == demanda[j]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    return prob.status, prob.variables(), prob.objective