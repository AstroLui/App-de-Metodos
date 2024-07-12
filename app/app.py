import customtkinter as ctk

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
global modeForTransporte
def segmented_button_callback(value):
    modeForTransporte = "max" if(value == "Maximizar") else "min"
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

labelEntryMatriz = ctk.CTkLabel(tabTransporte, text="Matriz de Costo", font=("Inter Tight", 16))
labelEntryMatriz.pack( padx=2, pady=2, fill="x")


    #<-- Para el Metodo de Transporte Fin-->
#<-- Correr App -->
app.mainloop()

#<--- Funciones --->
def constMatriz():
    return 