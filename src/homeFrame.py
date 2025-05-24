
import tkinter as tk


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=500, height=400)

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")
