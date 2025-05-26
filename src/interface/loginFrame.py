
import tkinter as tk


class LongInFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=500, height=400)

        title = tk.Label(self, text="Login : ", font=("times new roman", 16))
        title.place(x=20, y=20)

        self.username_label = tk.Label(self, text="Write your username please : ", font=("times new roman", 12))
        self.username_label.place(x=40, y=60)

        self.entry = tk.Entry(self, width=150, borderwidth=0)
        self.entry.bind("<Return>", lambda event: self.login())
        self.entry.focus_set()
        self.entry.place(x=60, y=90)

        signup_label = tk.Label(self, text="If you don't have an account, you can ", font=("times new roman", 9))
        signup_label.place(x=150, y=120)

        signup_button = tk.Button(self, text="sign up", borderwidth=0, font=("times new roman", 9), fg="blue",
                                  activeforeground="black", command=lambda: controller.show_frame("signup"))
        signup_button.place(x=335, y=120)

        login_button = tk.Button(self, text="Login", width=10, borderwidth=1, fg="blue", activeforeground="black",
                                 font=("times new roman", 14), relief="solid", command=lambda: self.login())
        login_button.place(x=392, y=160)

    def config_controller_dimensions(self):
        self.controller.geometry("520x220")

    def login(self):
        username = self.entry.get()
        if username == "":
            return

        data = self.controller.req.sendRequestsToDB(f"""
        SELECT username
        FROM player p
        WHERE p.username = %s
        """, (username,), "check if username exists")

        if len(data) == 0:
            self.username_label.config(text="This username doesn't exists, write your username please : ")
            return

        self.controller.username = username

        self.controller.make_home_frame()
