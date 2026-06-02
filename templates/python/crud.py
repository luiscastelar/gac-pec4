import tkinter as tk
from tkinter import ttk

class CRUD:
    def __init__(self):
        # Inicio el panel raíz (root)
        self.root = tk.Tk()
        self.root.title("Ventana Principal")
        self.root.minsize(400, %%ALTURA%%)

        # Marco principal centrado
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Inicio del panel principal
        self.create_index_widget()  

    def create_index_widget(self):
        # Destruimos paneles hijos
        for ventana in self.main_frame.winfo_children():
            ventana.destroy()

        titulo = ttk.Label(
            self.main_frame,
            text="Panel principal (DB: %%TIPO_DB%% ➡️ UI: %%UI_TYPE%%)",
            font=("Segoe UI", 14, "bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 15))

        # Botones en la ventana principal para abrir las ventanas hijas
%%BOTONES%%

        # Acciones de los botones (funciones callback)
%%ACCIONES_DE_BOTONES%%


    def _abrir_ventana_hija(self, titulo, funcion_creacion):

        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("800x500")

        # Truco importante:
        # reutilizamos tu arquitectura esperando self.root
        class Dummy:
            pass

        wrapper = Dummy()
        wrapper.root = ventana

        # Permitimos que tus módulos puedan usar clear_widgets()
        def clear_widgets():
            for w in ventana.winfo_children():
                w.destroy()

        wrapper.clear_widgets = clear_widgets

        funcion_creacion(wrapper)

        ventana.transient(self.root)
        ventana.grab_set()


    def run(self):
        # Comenzamos GUI de la App
        self.root.mainloop()


# Check if the script is run directly (not imported)
if __name__ == "__main__":
    # Instanciamos la aplicación
    app = CRUD()
    # La lanzamos
    app.run()
