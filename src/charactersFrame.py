from tkinter import ttk
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

        self.characters_combobox = ttk.Combobox(self)
        self.characters_combobox.place(x=20, y=40)
        self.characters_combobox.bind("<<ComboboxSelected>>", self.load_character_info)

        self.load_characters()

        self.class_label = tk.Label(self, font=("times new roman", 12))
        self.class_label.place(x=20, y=70)

        self.health_label = tk.Label(self, font=("times new roman", 12))
        self.health_label.place(x=120, y=70)

        self.mana_label = tk.Label(self, font=("times new roman", 12))
        self.mana_label.place(x=220, y=70)

        self.power_label = tk.Label(self, font=("times new roman", 12))
        self.power_label.place(x=320, y=70)

        self.intelligence_label = tk.Label(self, font=("times new roman", 12))
        self.intelligence_label.place(x=420, y=70)

        self.agility_label = tk.Label(self, font=("times new roman", 12))
        self.agility_label.place(x=520, y=70)

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")

    def load_characters(self):
        username = self.controller.username
        data = self.controller.req.sendRequestsToDB("""
        SELECT name
        FROM character c
        WHERE c.username = %s
        """, (username,), "get characters names")
        values = []
        for ele in data:
            values.append(ele["name"])

        self.characters_combobox.config(values=values)

    def load_character_info(self):
        username = self.controller.username
        character_name = self.characters_combobox.get()

        data = self.controller.req.sendRequestsToDB("""
        SELECT class, health, mana, strength, intelligence, agility
        FROM character c
        WHERE c.username = %s AND c.name = %s
        """, (username, character_name), "get character's info")

        ch_class = data[0]["class"]

