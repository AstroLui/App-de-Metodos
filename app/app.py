import customtkinter as ctk
from solTrasporte import Start
from solHungarian import Aplicar_Metodo, Aplicar_Metodo_Pasos
from pulp import LpStatus, value, LpVariable

# <--- Funciones --->


def buttonMatriz_comand():
    for widget in frameEntryMatriz.winfo_children():
        widget.destroy()
    n = int(entryRow.get())
    m = int(entryCol.get())
    for i in range(n):
        for j in range(m):
            entry = ctk.CTkEntry(frameEntryMatriz, width=60,
                                 placeholder_text=f"{i}{j}", border_width=0)
            entry.grid(row=i, column=j, padx=5, pady=5)
    for i in range(n):
        entry = ctk.CTkEntry(frameEntryMatriz, width=73,
                             placeholder_text=f"O{i}", border_width=0)
        entry.grid(row=i, column=m+1, padx=5, pady=5)
    for j in range(m):
        entry = ctk.CTkEntry(frameEntryMatriz, width=73,
                             placeholder_text=f"D{j}", border_width=0)
        entry.grid(row=n+1, column=j, padx=5, pady=5)


def buttonMatrizH_comand():
    for widget in frameEntryMatrizH.winfo_children():
        widget.destroy()
    n = int(entryRowH.get())
    m = int(entryColH.get())
    for i in range(n):
        for j in range(m):
            entryH = ctk.CTkEntry(frameEntryMatrizH, width=60,
                                  placeholder_text=f"{i}{j}", border_width=0)
            entryH.grid(row=i, column=j, padx=5, pady=5)


def segmented_button_callback(value):
    global modeForTransporte
    modeForTransporte = "max" if (value == "Maximizar") else "min"
    print(modeForTransporte)


def buttonSolver_comand():
    textBoxSolver.insert("0.0", "<------------------------> \n")
    matriz = []
    n = int(entryRow.get())
    m = int(entryCol.get())
    i = 0
    j = 0
    k = 0
    array = []
    ofertas = []
    demandas = []
    for widget in frameEntryMatriz.winfo_children():
        if (i < n):
            if (j < m):
                array.append(int(widget.get()))
                j += 1
            else:
                matriz.append(array)
                array = []
                i += 1
                array.append(int(widget.get()))
                j = 1
                if (i == n):
                    ofertas.append(int(widget.get()))
                    k += 1
        else:
            if (k < n):
                ofertas.append(int(widget.get()))
                k += 1
            else:
                demandas.append(int(widget.get()))
    status, variables, objetivo = Start(
        matriz, ofertas, demandas, n, m, modeForTransporte)
    textstatus = LpStatus[status]
    costoTotal = value(objetivo)
    for v in variables:
        textBoxSolver.insert("0.0", str(v.name) +
                             " : " + str(v.varValue) + "\n")
    textBoxSolver.insert("0.0", "Costo Total: " + " " + str(costoTotal) + "\n")
    textBoxSolver.insert("0.0", "Status: " + " " + str(textstatus) + "\n")


def buttonSolverH_comand():
    textBoxSolverH.delete("0.0", "end")
    textBoxSolverH.insert("0.0", "<------------------------> \n")

    matriz = []
    n = int(entryRowH.get())
    m = int(entryColH.get())
    array = []

    for index, widget in enumerate(frameEntryMatrizH.winfo_children()):
        array.append(int(widget.get()))
        if (index + 1) % m == 0:
            matriz.append(array)
            array = []

    if array:  # To handle any remaining elements
        matriz.append(array)

    # matriz = []
    # n = int(entryN.get())

    # widgets = frameEntryMatrizH.winfo_children()
    # # Fill matrix
    # for i in range(n):
    #     row = []
    #     for j in range(n):
    #         row.append(int(widgets[i * n + j].get()))
    #     matriz.append(row)

    Aplicar_Metodo_Pasos(matriz, textBoxSolverH)
    asignaciones, costoTotal = Aplicar_Metodo(matriz)

    # Show each assignment and its value
    value_list = []
    total_sum = ""
    for idx, (i, j) in enumerate(asignaciones, start=1):
        value = matriz[i][j]
        value_list.append(value)
        textBoxSolverH.insert("end", f"Asignación {
                              idx}: (Columna {i}, Fila {j}) -> Valor: {value}\n")

    textBoxSolverH.insert("end", f"Costo Total: {costoTotal}\n")
    for i in range(len(value_list)-1):
        total_sum += str(value_list[i]) + " + "
    total_sum += str(value_list[-1]) + " = " + str(sum(value_list))
    textBoxSolverH.insert(
        "end", f"Suma de valores de asignaciones: {total_sum}\n")


def segmented_button_callbackH(value):
    global modeForHungaro
    modeForHungaro = "max" if (value == "Maximizar") else "min"
    print(modeForHungaro)


# <--- Funciones Fin --->
# <--- Creacion de la App --->
app = ctk.CTk()
# <--- Configuracion de la App --->
app.title("App")
app.geometry("400x700")
app._set_appearance_mode("light")
# <--- Adicion de Widgets --->
# <-- TabView Main -->
tabView = ctk.CTkTabview(master=app)
tabView.pack(padx=(20, 20), pady=(5, 20), fill="both", expand=True, side="top")

tabView.add("Metodo de Transporte")
tabView.add("Metodo Hungaro")
tabTransporte = tabView.tab("Metodo de Transporte")
tabHungaro = tabView.tab("Metodo Hungaro")
tabView.set("Metodo de Transporte")
# <-- TabView Main Fin -->
# <-- Para el Metodo de Transporte -->
# <- Frame para la eleccion de Costo ->
frameChoose = ctk.CTkFrame(tabTransporte)
frameChoose.pack(padx=2, pady=2, fill="x")
labelChoose = ctk.CTkLabel(
    frameChoose, text="Problema a", font=("Inter Tight", 15))
labelChoose.grid(row=0, column=0, padx=(75, 0))
chooseOption = ctk.CTkSegmentedButton(
    frameChoose, values=["Maximizar", "Minimizar"], command=segmented_button_callback)
chooseOption.grid(row=0, column=1, padx=(5, 10), pady=5)
# <- Frame para la eleccion de Costo Fin ->
# <- Frame para la inputs de los numeros de filas y columnas ->
frameEntry = ctk.CTkFrame(tabTransporte)
frameEntry.pack(padx=2, pady=2, fill="x")
labelEntryRow = ctk.CTkLabel(
    frameEntry, text="Ingrese el numero de Filas", font=("Inter Tight", 14))
labelEntryRow.grid(row=0, column=0, padx=(15, 3), pady=3)
entryRow = ctk.CTkEntry(frameEntry, width=50, border_width=0)
entryRow.grid(row=0, column=1, padx=10, pady=2)
labelEntryCol = ctk.CTkLabel(
    frameEntry, text="Ingrese el numero de Columnas", font=("Inter Tight", 13))
labelEntryCol.grid(row=1, column=0, padx=(15, 3), pady=3)
entryCol = ctk.CTkEntry(frameEntry, width=50, border_width=0)
entryCol.grid(row=1, column=1, padx=10, pady=2)
# <- Frame para la inputs de los numeros de filas y columnas Fin ->
# <- Button para formar la Matriz ->
buttonMatriz = ctk.CTkButton(tabTransporte, text="Formar Matriz", border_width=0, font=(
    "Inter Tight", 14), command=buttonMatriz_comand)
buttonMatriz.pack(padx=10, pady=10, fill="x")
# <- Button para formar la Matriz Fin ->
# <- Espacio donde se formara la Matriz ->
labelEntryMatriz = ctk.CTkLabel(
    tabTransporte, text="Matriz de Costo", font=("Inter Tight", 16))
labelEntryMatriz.pack(padx=2, pady=2, fill="x")
frameEntryMatriz = ctk.CTkFrame(tabTransporte, )
frameEntryMatriz.pack(padx=2, pady=2, fill="x")
# <- Espacio donde se formara la Matriz Fin ->
# <- Button para generar la solucion ->
buttonSolver = ctk.CTkButton(
    tabTransporte, text="Resolver", border_width=0, command=buttonSolver_comand)
buttonSolver.pack(padx=10, pady=10, fill="x")
# <- Button para generar la solucion Fin ->
# <- TextBox donde se mostrar los resultados de la solucion ->
textBoxSolver = ctk.CTkTextbox(tabTransporte)
textBoxSolver.pack(padx=20, pady=10, fill="both")
# <- TextBox donde se mostrar los resultados de la solucion Fin ->
# <-- Para el Metodo de Transporte Fin-->
# <-- Para el Metodo Hungaro  -->
# <- Frame para la eleccion de Costo ->
frameChooseH = ctk.CTkFrame(tabHungaro)
frameChooseH.pack(padx=2, pady=2, fill="x")
labelChooseH = ctk.CTkLabel(
    frameChooseH, text="Problema a", font=("Inter Tight", 15))
labelChooseH.grid(row=0, column=0, padx=(75, 0))
chooseOptionH = ctk.CTkSegmentedButton(
    frameChooseH, values=["Maximizar", "Minimizar"], command=segmented_button_callback)
chooseOptionH.grid(row=0, column=1, padx=(5, 10), pady=5)
# <- Frame para la eleccion de Costo Fin ->
# <- Frame para el input del tamaño de la Matriz ->
# frameEntryH = ctk.CTkFrame(tabHungaro)
# frameEntryH.pack(padx=2, pady=2, fill="x")
# labelEntryN = ctk.CTkLabel(
#     frameEntryH, text="Ingrese el tamaño de la matriz: ", font=("Inter Tight", 13))
# labelEntryN.grid(padx=2, pady=2, row=0, column=0)
# entryN = ctk.CTkEntry(frameEntryH, border_width=0, width=50)
# entryN.grid(padx=2, pady=2, row=0, column=1)
frameEntryH = ctk.CTkFrame(tabHungaro)
frameEntryH.pack(padx=2, pady=2, fill="x")
labelEntryRowH = ctk.CTkLabel(
    frameEntryH, text="Ingrese el numero de Filas", font=("Inter Tight", 14))
labelEntryRowH.grid(row=0, column=0, padx=(15, 3), pady=3)
entryRowH = ctk.CTkEntry(frameEntryH, width=50, border_width=0)
entryRowH.grid(row=0, column=1, padx=10, pady=2)
labelEntryColH = ctk.CTkLabel(
    frameEntryH, text="Ingrese el numero de Columnas", font=("Inter Tight", 13))
labelEntryColH.grid(row=1, column=0, padx=(15, 3), pady=3)
entryColH = ctk.CTkEntry(frameEntryH, width=50, border_width=0)
entryColH.grid(row=1, column=1, padx=10, pady=2)
# <- Frame para el input del tamaño de la Matriz Fin ->
# <- Button que formara la matriz ->
buttonMatrizH = ctk.CTkButton(tabHungaro, text="Forma Matriz", font=(
    "Inter Tight", 14), command=buttonMatrizH_comand)
buttonMatrizH.pack(padx=10, pady=10, fill="x")
# <- Button que formara la matriz Fin ->
# <- Espacio para la formacion de la Matriz ->
labelEntryMatrizH = ctk.CTkLabel(
    tabHungaro, text="Matriz de Costo", font=("Inter Tight", 16))
labelEntryMatrizH.pack(padx=5, pady=5, fill="x")
frameEntryMatrizH = ctk.CTkFrame(tabHungaro)
frameEntryMatrizH.pack(padx=2, pady=2, fill="x")
# <- Espacio para la formacion de la Matriz Fin ->
# <- Button para genera la solucion ->
buttonSolverH = ctk.CTkButton(tabHungaro, text="Resolver", font=(
    "Inter Tight", 14), command=buttonSolverH_comand)
buttonSolverH.pack(padx=10, pady=10, fill="x")
# <- Button para genera la solucion Fin ->
# <- TextBox para mostrar los resultados ->
textBoxSolverH = ctk.CTkTextbox(tabHungaro)
textBoxSolverH.pack(padx=20, pady=20, fill="x")
# <- TextBox para mostrar los resultados Fin ->
# <-- Para el Metodo Hungaro Fin -->
# <-- Correr App -->
app.mainloop()
