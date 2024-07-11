from pulp import *
import numpy as np

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
        
n = int (input("Ingresar un numero para n: "))
m = int (input("Ingresar un numero para m: "))
matriz = Enter_MatrizCosto(n, m)
oferta, demanda = Enter_Demanda_Oferta(n, m)

prob = pulp.LpProblem("Problema de Trasnporte", pulp.const.LpMinimize)
variables = pulp.LpVariable.dicts("Variables",[(i,j) for i in range(n) for j in range(m)], lowBound=0)
prob += pulp.lpSum(variables[(i, j)] * matriz[i][j] for i in range(n) for j in range(m))

for i in range(n):
    prob += pulp.lpSum(variables[(i, j)] for j in range(m)) == oferta[i]

for j in range(m):
    prob += pulp.lpSum(variables[(i, j)] for i in range(n)) == demanda[j]

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print("Status:", LpStatus[prob.status])

### Imprimimos la solución
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print('El costo mínimo es:', value(prob.objective))