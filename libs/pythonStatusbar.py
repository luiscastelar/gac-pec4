import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.var = tk.StringVar(value="Listo.")

        self.label = ttk.Label(
            self,
            textvariable=self.var,
            anchor="w"
        )
        self.label.pack(fill="x", padx=5)

    def info(self, msg):
        self.var.set(msg)

    def error(self, msg):
        self.var.set("ERROR: " + msg)
