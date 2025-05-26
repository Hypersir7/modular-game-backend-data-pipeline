import tkinter as tk
from tkinter import ttk


class MonstersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=700)

        self.title_label = tk.Label(self, text="Monster Bestiary", font=("times new roman", 16))
        self.title_label.place(x=20, y=10)

        self.back_button = tk.Button(self, text="Home", borderwidth=0, fg="blue",
                                     activeforeground="black",
                                     command=lambda: controller.show_frame("home"))
        self.back_button.place(x=650, y=10)

        self.monster_combobox = ttk.Combobox(self, width=50)
        self.monster_combobox.place(x=20, y=50)
        self.monster_combobox.bind("<<ComboboxSelected>>", self.load_monster_info)


        self.stats_labels = {
            "health": tk.Label(self, font=("times new roman", 12)),
            "attack": tk.Label(self, font=("times new roman", 12)),
            "defense": tk.Label(self, font=("times new roman", 12)),
            "money": tk.Label(self, font=("times new roman", 12)),
            "probability": tk.Label(self, font=("times new roman", 12)),
        }

        y = 90
        for key, label in self.stats_labels.items():
            label.place(x=20, y=y)
            y += 30


        self.loot_title = tk.Label(self, text="Loots:", font=("times new roman", 14))
        self.loot_title.place(x=20, y=250)

        self.loot_listbox = tk.Listbox(self, width=60, font=("times new roman", 11))
        self.loot_listbox.place(x=20, y=280)

        self.load_monster_names()

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")

    def load_monster_names(self):
        data = self.controller.req.sendRequestsToDB("""
            SELECT name FROM monster ORDER BY name
        """, None, "load monster names")
        names = [row["name"] for row in data]
        self.monster_combobox.config(values=names)

    def load_monster_info(self, event):
        monster_name = self.monster_combobox.get()

        data = self.controller.req.sendRequestsToDB("""
            SELECT health, attack, defense, money, probability
            FROM monster
            WHERE name = %s
        """, (monster_name,), "load monster stats")

        if not data:
            return

        stats = data[0]
        self.stats_labels["health"].config(text=f"Health : {stats['health']}")
        self.stats_labels["attack"].config(text=f"Attack : {stats['attack']}")
        self.stats_labels["defense"].config(text=f"Defense : {stats['defense']}")
        self.stats_labels["money"].config(text=f"Gold drop : {stats['money']}")
        self.stats_labels["probability"].config(text=f"Drop chance : {stats['probability']}%")

        # GETTING LOOT
        self.loot_listbox.delete(0, tk.END)
        lootData = self.controller.req.sendRequestsToDB("""
            SELECT o.name, mo.probability
            FROM monster_object mo
            JOIN monster m ON m.id = mo.monster_id
            JOIN object o ON o.name = mo.object_name
            WHERE m.name = %s
        """, (monster_name,), "get monster loots")

        if not lootData:
            self.loot_listbox.insert(tk.END, "No loot defined.")
            return

        for loot in lootData:
            self.loot_listbox.insert(tk.END, f"{loot['name']} - {loot['probability']}% [drop probability]")
