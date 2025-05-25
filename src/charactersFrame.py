
import tkinter as tk


class CharactersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=700)

        self.title_label = tk.Label(self, font=("times new roman", 16), text="Characters : ")
        self.title_label.place(x=20, y=10)

        self.go_home_button = tk.Button(self, text="Home", borderwidth=0, fg="blue", activeforeground="black",
                                        command=lambda: self.controller.show_frame("home"))
        self.go_home_button.place(x=650, y=10)

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")


