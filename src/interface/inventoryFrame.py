import tkinter as tk
from tkinter import ttk


class InventoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=700)

        self.title_label = tk.Label(self, text="Inventory", font=("times new roman", 16))
        self.title_label.place(x=20, y=10)

        self.back_button = tk.Button(self, text="Home", borderwidth=0, fg="blue",
                                     activeforeground="black", command=lambda: controller.show_frame("home"))
        self.back_button.place(x=650, y=10)

        # INVENTORY DISPLAY
        self.inventory_listbox = tk.Listbox(self, width=80, font=("times new roman", 12))
        self.inventory_listbox.place(x=20, y=60)

        # OBJECT LIST
        objet_list = tk.Frame(self)
        objet_list.place(x=20, y=430)

        scrollbar = tk.Scrollbar(objet_list, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.object_listbox = tk.Listbox(objet_list, width=60, height=8,
                                         yscrollcommand=scrollbar.set, font=("times new roman", 10))
        self.object_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.object_listbox.yview)

        self.loadAvailableObjects()

        self.manual_entry = tk.Entry(self, width=45, font=("times new roman", 10))
        self.manual_entry.place(x=20, y=390)

        self.add_button = tk.Button(self, text="Add Object", command=self.addSelectedObject)
        self.add_button.place(x=400, y=390)

        self.equip_button = tk.Button(self, text="Equip Object", command=self.equipObject)
        self.equip_button.place(x=20, y=600)

        self.remove_button = tk.Button(self, text="Remove Object", command=self.removeObject)
        self.remove_button.place(x=140, y=600)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.loadInventory)
        self.refresh_button.place(x=280, y=600)

        self.loadInventory()

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")

    def loadAvailableObjects(self):
        data = self.controller.req.sendRequestsToDB("""
            SELECT name FROM object
        """, None, "get all object names")

        self.object_listbox.delete(0, tk.END)
        for row in data:
            self.object_listbox.insert(tk.END, row["name"])

    def loadInventory(self):
        self.inventory_listbox.delete(0, tk.END)
        username = self.controller.username

        data = self.controller.req.sendRequestsToDB("""
            SELECT o.name, o.type, o.property, o.price, po.equipped
            FROM player_object po
            JOIN player p ON p.id = po.player_id
            JOIN object o ON o.name = po.object_name
            WHERE p.username = %s
        """, (username,), "get player inventory")

        if not data:
            self.inventory_listbox.insert(tk.END, "Inventory is empty.")
            return

        for row in data:
            if row["equipped"] == True: # BY DEFAULT IS SET FALSE IN THE DB
                equipped = "[✅ EQUIPPED]"
            else:
                equipped = ""
            info = f"{equipped} {row['name']} ({row['type']}) -- {row['property']} -- {row['price']} gold coins"
            self.inventory_listbox.insert(tk.END, info)

    def addSelectedObject(self):
        objectName = self.manual_entry.get().strip()

        if not objectName:
            selected = self.object_listbox.curselection()
            if not selected:
                return
            objectName = self.object_listbox.get(selected[0])

        username = self.controller.username

        self.controller.req.sendRequestsToDB("""
            INSERT INTO player_object (player_id, object_name)
            VALUES ((SELECT id FROM player WHERE username = %s), %s)
            ON CONFLICT DO NOTHING
        """, (username, objectName), "add object to player")

        self.controller.req.commit_transactions()
        self.loadInventory()
        self.manual_entry.delete(0, tk.END)

    def removeObject(self):
        selection = self.inventory_listbox.curselection()
        if not selection:
            return

        info = self.inventory_listbox.get(selection[0])
        objectName = info.replace("[✅ EQUIPPED]", "").strip().split(" (")[0]

        username = self.controller.username
        self.controller.req.sendRequestsToDB("""
            DELETE FROM player_object
            WHERE player_id = (SELECT id FROM player WHERE username = %s)
            AND object_name = %s
        """, (username, objectName), "remove object from inventory")

        self.controller.req.commit_transactions()
        self.loadInventory()

    def equipObject(self):
        selection = self.inventory_listbox.curselection()
        if not selection:
            return

        info = self.inventory_listbox.get(selection[0])
        objectName = info.replace("[✅ EQUIPPED]", "").strip().split(" (")[0]

        username = self.controller.username

        self.controller.req.sendRequestsToDB("""
            UPDATE player_object
            SET equipped = FALSE
            WHERE player_id = (SELECT id FROM player WHERE username = %s)
        """, (username,), "unequip all")

        self.controller.req.sendRequestsToDB("""
            UPDATE player_object
            SET equipped = TRUE
            WHERE player_id = (SELECT id FROM player WHERE username = %s)
            AND object_name = %s
        """, (username, objectName), "equip object")

        self.controller.req.commit_transactions()
        self.loadInventory()
