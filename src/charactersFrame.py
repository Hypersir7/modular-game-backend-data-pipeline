from tkinter import ttk
import tkinter as tk


class CharactersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=600)

        self.title_label = tk.Label(self, font=("times new roman", 16), text="Characters : ")
        self.title_label.place(x=20, y=10)

        self.go_home_button = tk.Button(self, text="Home", borderwidth=0, fg="blue", activeforeground="black",
                                        command=lambda: self.controller.show_frame("home"))
        self.go_home_button.place(x=650, y=10)

        self.characters_combobox = ttk.Combobox(self)
        self.characters_combobox.place(x=20, y=40)
        self.characters_combobox.bind("<<ComboboxSelected>>", self.load_character_info)
        characters_loaded = self.load_characters()
        if characters_loaded:
            self.characters_combobox.current(0)

        self.class_label = tk.Label(self, font=("times new roman", 12))
        self.class_label.place(x=20, y=70)

        self.health_label = tk.Label(self, font=("times new roman", 12))
        self.health_label.place(x=20, y=100)

        self.mana_label = tk.Label(self, font=("times new roman", 12))
        self.mana_label.place(x=20, y=130)

        self.power_label = tk.Label(self, font=("times new roman", 12))
        self.power_label.place(x=20, y=160)

        self.intelligence_label = tk.Label(self, font=("times new roman", 12))
        self.intelligence_label.place(x=20, y=190)

        self.agility_label = tk.Label(self, font=("times new roman", 12))
        self.agility_label.place(x=20, y=220)

        if characters_loaded:
            self.characters_combobox.event_generate("<<ComboboxSelected>>")  # charger le premier char

        self.create_new_character_label = tk.Label(self, text="Create a new character : ", font=("times new roman", 16))
        self.create_new_character_label.place(x=20, y=250)

        self.name_label = tk.Label(self, font=("times new roman", 12), text="Name : ")
        self.name_label.place(x=20, y=290)

        vcmd = (self.register(self.check_entry_input_no_comma), '%P')
        self.name_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.name_entry.place(x=80, y=290)

        self.class_label_1 = tk.Label(self, text="Class : ", font=("times new roman", 12))
        self.class_label_1.place(x=20, y=320)

        self.classes_combobox = ttk.Combobox(self, state="readonly")
        self.classes_combobox.place(x=80, y=320)
        self.load_classes()
        self.classes_combobox.current(0)

        vcmd_1 = (self.register(self.check_entry_input_only_numbers), '%P')

        self.health_label_1 = tk.Label(self, text="Health : ", font=("times new roman", 12))
        self.health_label_1.place(x=20, y=350)

        self.health_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_1)
        self.health_entry.place(x=95, y=350)

        self.mana_label_1 = tk.Label(self, text="Mana : ", font=("times new roman", 12))
        self.mana_label_1.place(x=20, y=380)

        self.mana_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_1)
        self.mana_entry.place(x=95, y=380)

        self.power_label_1 = tk.Label(self, text="Strength : ", font=("times new roman", 12))
        self.power_label_1.place(x=20, y=410)

        self.power_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_1)
        self.power_entry.place(x=95, y=410)

        self.intelligence_label_1 = tk.Label(self, text="Intelligence : ", font=("times new roman", 12))
        self.intelligence_label_1.place(x=20, y=440)

        self.intelligence_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_1)
        self.intelligence_entry.place(x=95, y=440)

        self.agility_label_1 = tk.Label(self, text="Agility : ", font=("times new roman", 12))
        self.agility_label_1.place(x=20, y=470)

        self.agility_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_1)
        self.agility_entry.place(x=95, y=470)

        self.create_character_button = tk.Button(self, text="Create", font=("times new roman", 16), borderwidth=0,
                                                 fg="blue", activeforeground="black",
                                                 command=lambda: self.create_new_character())
        self.create_character_button.place(x=20, y=505)

        self.res_label = tk.Label(self, text="Result : ", font=("times new roman", 12), fg="red")
        self.res_label.place(x=20, y=550)

    def config_controller_dimensions(self):
        self.controller.geometry("700x600")

    def load_characters(self):
        self.characters_combobox.delete(0, tk.END)

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

        if len(values) == 0:
            return False
        else:
            return True

    def load_character_info(self, event):
        username = self.controller.username
        character_name = self.characters_combobox.get()

        data = self.controller.req.sendRequestsToDB("""
        SELECT class, health, mana, strength, intelligence, agility
        FROM character c
        WHERE c.username = %s AND c.name = %s
        """, (username, character_name), "get character's info")

        ch_class = data[0]["class"]
        health = data[0]["health"]
        mana = data[0]["mana"]
        strength = data[0]["strength"]
        intelligence = data[0]["intelligence"]
        agility = data[0]["agility"]

        self.class_label.config(text=f"Class : {ch_class}")
        self.health_label.config(text=f"Health : {health}")
        self.mana_label.config(text=f"Mana : {mana}")
        self.power_label.config(text=f"Strength : {strength}")
        self.intelligence_label.config(text=f"Intelligence : {intelligence}")
        self.agility_label.config(text=f"Agility : {agility}")

    def load_classes(self):
        data = self.controller.req.sendRequestsToDB("""
        SELECT DISTINCT class
        FROM character c
        """, None, "get all the classes")

        values = []
        for ele in data:
            values.append(ele["class"])
        self.classes_combobox.config(values=values)

    @staticmethod
    def check_entry_input_only_numbers(new_value):
        if (new_value == "" or new_value.isdigit()) and len(new_value) <= 3:
            return True
        return False

    @staticmethod
    def check_entry_input_no_comma(new_value):
        if len(new_value) <= 100 and new_value.find(",") == -1:
            return True

        return False

    def create_new_character(self):
        username = self.controller.username
        name = self.name_entry.get()
        ch_class = self.classes_combobox.get()
        health = self.health_entry.get()
        mana = self.mana_entry.get()
        strength = self.power_entry.get()
        intelligence = self.intelligence_entry.get()
        agility = self.agility_entry.get()

        if (name == "" or ch_class == "" or health == "" or mana == "" or strength == "" or intelligence == ""
                or agility == ""):
            return

        data = self.controller.req.sendRequestsToDB("""
                SELECT name
                FROM character c
                WHERE c.name = %s
                """, (name,), "verify if the name exists")

        if len(data) != 0:  # le nom exist deja
            self.res_label.config(text="Result : The name already exists")
            return

        self.controller.req.sendRequestsToDB("""
        INSERT INTO character (username, name, class, health, mana, strength, intelligence, agility)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, name, ch_class, int(health), int(mana), int(strength), int(intelligence), int(agility)),
                                             "insert a new character")

        self.controller.req.commit_transactions()

        self.res_label.config(text="Result : Character was created successfully")

        self.load_characters()
        self.characters_combobox.current(0)
        self.characters_combobox.event_generate("<<ComboboxSelected>>")
