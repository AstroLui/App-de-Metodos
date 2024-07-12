import customtkinter as ctk
from solTrasporte import Start
from pulp import LpStatus, value, LpVariable
#<-- Variables Globales -->
global modeForTransporte
#<--- Funciones --->
def buttonMatriz_comand():
    for widget in frameEntryMatriz.winfo_children():
        widget.destroy()    
    n = int(entryRow.get())
    m = int(entryCol.get())
    for i in range(n):
        for j in range(m):
            entry=ctk.CTkEntry(frameEntryMatriz, width=30, placeholder_text=f"{i}{j}")
            entry.grid(row=i, column=j, padx=5, pady=5)
    for i in range(n):
        entry=ctk.CTkEntry(frameEntryMatriz, width=30, placeholder_text=f"O{i}")
        entry.grid(row=i, column=m+1, padx=5, pady=5)
    for j in range(m):
        entry=ctk.CTkEntry(frameEntryMatriz, width=30, placeholder_text=f"D{j}")
        entry.grid(row=n+1, column=j, padx=5, pady=5)

def segmented_button_callback(value):
    modeForTransporte = "max" if(value == "Maximizar") else "min"

def buttonSolver_comand():
    matriz=[]
    n = int(entryRow.get())
    m = int(entryCol.get())
    i = 0
    j = 0
    k = 0
    array=[]
    ofertas = []
    demandas = []
    for widget in frameEntryMatriz.winfo_children():
        if(i < n):
            if(j < m):
                array.append(int(widget.get()))
                j+=1
            else:
                matriz.append(array)
                array=[]
                i+=1
                array.append(int(widget.get()))
                j=1
                if(i == n):
                    ofertas.append(int(widget.get()))
                    k+=1
        else:
            if(k < n):
                ofertas.append(int(widget.get()))
                k +=1
            else:
                demandas.append(int(widget.get()))
    print(matriz)
    print(ofertas)
    print(demandas)
    status, variables, objetivo = Start(matriz, ofertas, demandas, n, m)
    textstatus = LpStatus[status]
    costoTotal = value(objetivo)
    for v in variables:
        textBoxSolver.insert("0.0", str(v.name) + " : " + str(v.varValue) + "\n")
    textBoxSolver.insert("0.0", "Costo Total: " + " " + str(costoTotal) + "\n")
    textBoxSolver.insert("0.0", "Status: " + " " + str(textstatus) + "\n")

#<--- Creacion de la App --->
app = ctk.CTk()
#<--- Configuracion de la App --->
app.title("App")
app.geometry("400x700")
app._set_appearance_mode("light")
#<--- Adicion de Widgets --->
    #<-- TabView Main -->
tabView = ctk.CTkTabview(master=app)
tabView.pack(padx=(20, 20), pady=(5, 20), fill="both", expand=True, side="top")

tabView.add("Metodo de Transporte")
tabView.add("Metodo de Hungaro")
tabTransporte = tabView.tab("Metodo de Transporte")
tabView.set("Metodo de Transporte")
    #<-- TabView Main Fin -->
    #<-- Para el Metodo de Transporte -->
frameChoose = ctk.CTkFrame(tabTransporte)
frameChoose.pack(padx=2, pady=2, fill="x")
labelChoose = ctk.CTkLabel(frameChoose, text="Costo a", font=("Inter Tight", 15))
labelChoose.grid(row=0, column=0, padx=(75, 0))
chooseOption = ctk.CTkSegmentedButton(frameChoose,values=["Maximizar", "Minimizar"], command=segmented_button_callback)
chooseOption.grid(row=0, column=1, padx=(5, 10), pady=5)

frameEntry = ctk.CTkFrame(tabTransporte)
frameEntry.pack(padx=2, pady=2, fill="x")
labelEntryRow = ctk.CTkLabel(frameEntry, text="Ingrese el numero de Filas", font=("Inter Tight", 14))
labelEntryRow.grid(row=0, column=0, padx=(15, 3), pady=3)
entryRow = ctk.CTkEntry(frameEntry, width=50, border_width=0)
entryRow.grid(row=0, column=1, padx=10, pady=2)
labelEntryCol = ctk.CTkLabel(frameEntry, text="Ingrese el numero de Columna", font=("Inter Tight", 13))
labelEntryCol.grid(row=1, column=0, padx=(15, 3), pady=3)
entryCol = ctk.CTkEntry(frameEntry, width=50, border_width=0)
entryCol.grid(row=1, column=1, padx=10, pady=2)

buttonMatriz = ctk.CTkButton(tabTransporte, text="Formar Matriz",border_width=0, command=buttonMatriz_comand)
buttonMatriz.pack(padx=10, pady=10, fill="x")

labelEntryMatriz = ctk.CTkLabel(tabTransporte, text="Matriz de Costo", font=("Inter Tight", 16))
labelEntryMatriz.pack( padx=2, pady=2, fill="x")
frameEntryMatriz = ctk.CTkFrame(tabTransporte, )
frameEntryMatriz.pack(padx=2, pady=2, fill="x")

buttonSolver = ctk.CTkButton(tabTransporte, text="Resolver",border_width=0, command=buttonSolver_comand)
buttonSolver.pack(padx=10, pady=10, fill="x")

textBoxSolver = ctk.CTkTextbox(tabTransporte)
textBoxSolver.pack(padx=20, pady=10, fill="both")
    #<-- Para el Metodo de Transporte Fin-->
#<-- Correr App -->
app.mainloop()

