import customtkinter as ctk

#<--- Creacion de la App --->
app = ctk.CTk()
#<--- Configuracion de la App --->
app.title("App")
app.geometry("400x700")
app._set_appearance_mode("light")
app._font
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
    print(modeForTransporte)

labelChoose = ctk.CTkLabel(tabTransporte, text="Costo a")
labelChoose.grid(row=0, column=0, padx=(75, 0))
chooseOption = ctk.CTkSegmentedButton(tabTransporte,values=["Maximizar", "Minimizar"], command=segmented_button_callback)
chooseOption.grid(row=0, column=1, padx=(5, 10), pady=5)
    #<-- Para el Metodo de Transporte Fin-->
#<-- Correr App -->
app.mainloop()
