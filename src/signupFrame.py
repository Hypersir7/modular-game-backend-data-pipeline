
import tkinter as tk


class SignUpFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=500, height=400)

        title = tk.Label(self, text="Sign up : ", font=("times new roman", 16))
        title.place(x=20, y=20)

        username_label = tk.Label(self, text="Choose an username please (comma is not allowed) : ",
                                  font=("times new roman", 12))
        username_label.place(x=40, y=60)

        entry = tk.Entry(self, width=150, borderwidth=0)
        entry.place(x=60, y=90)

        login_label = tk.Label(self, text="If you already have an account, you can ", font=("times new roman", 9))
        login_label.place(x=150, y=120)

        login_button = tk.Button(self, text="login", borderwidth=0, font=("times new roman", 9), fg="blue",
                                 activeforeground="black", command=lambda: controller.show_frame("login"))
        login_button.place(x=345, y=120)

        signup_button = tk.Button(self, text="Sign up", width=10, borderwidth=1, fg="blue", activeforeground="black",
                                  font=("times new roman", 14), relief="solid")
        signup_button.place(x=392, y=160)

    def config_controller_dimensions(self):
        self.controller.geometry("520x220")
