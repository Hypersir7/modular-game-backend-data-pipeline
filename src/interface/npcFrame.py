from tkinter import ttk
import tkinter as tk

class NpcFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=600)

        self.title_label = tk.Label(self, font=("times new roman", 16), text="NPCs : ")
        self.title_label.place(x=20, y=10)

        self.go_home_button = tk.Button(self, text="Home", borderwidth=0, fg="blue", activeforeground="black",
                                        command=lambda: self.controller.show_frame("home"))
        self.go_home_button.place(x=650, y=10)

        # NPC
        tk.Label(self, text="Choose NPC: ", font=("times new roman", 14)).place(x=20, y=60)
        self.npc_combobox = ttk.Combobox(self, width=50)
        self.npc_combobox.place(x=150, y=60)
        self.npc_combobox.bind("<<ComboboxSelected>>", self.load_npc_info)
        self.load_npcs()

        # Dialogue
        self.dialogue_label = tk.Label(self, font=("times new roman", 12))
        self.dialogue_label.place(x=20, y=150)

        # Quests
        tk.Label(self, text="Quests: ", font=("times new roman", 14)).place(x=20, y=180)
        self.quest_combobox = ttk.Combobox(self, width=50)
        self.quest_combobox.place(x=150, y=180)
        self.accept_quest_button = tk.Button(self, text="Accept", command=self.accept_selected_quest)
        self.accept_quest_button.place(x=500, y=178)

        # Buy Objects
        tk.Label(self, text="Objects: ", font=("times new roman", 14)).place(x=20, y=210)
        self.object_combobox = ttk.Combobox(self, width=50)
        self.object_combobox.place(x=150, y=210)
        self.buy_button = tk.Button(self, text="Buy", command=self.buy_item)
        self.buy_button.place(x=500, y=208)

        # Sell Objects
        tk.Label(self, text="Inventory: ", font=("times new roman", 14)).place(x=20, y=240)
        self.sell_combobox = ttk.Combobox(self, width=50)
        self.sell_combobox.place(x=150, y=240)
        self.sell_button = tk.Button(self, text="Sell", command=self.sell_item)
        self.sell_button.place(x=500, y=238)

        # Results
        self.result_label = tk.Label(self, text="", font=("times new roman", 12), fg="green")
        self.result_label.place(x=200, y=280)

    def config_controller_dimensions(self):
        self.controller.geometry("700x600")

    def load_npcs(self):
        # Clear previous NPCs
        self.npc_combobox.config(values=[])
        self.npc_combobox.set('')

        # Load NPCs from the database
        data = self.controller.req.sendRequestsToDB("""
        SELECT name
        FROM pnjs
        """, None, "get all npcs")

        values = []
        for ele in data:
            values.append(ele["name"])

        self.npc_combobox.config(values=values)
        self.npc_combobox.set("Select npc")

        if len(values) == 0:
            return False
        else:
            return True

    def load_npc_info(self, event):
        name = self.npc_combobox.get()

        # Dialogue
        data = self.controller.req.sendRequestsToDB("""
        SELECT dialogue
        FROM pnjs c
        WHERE c.name = %s
        """, (name,), "get npc's dialogue")

        if not data:
            self.dialogue_label.config(text="Dialogue : Not found")
        else:
            dialogue = data[0]["dialogue"]
            self.dialogue_label.config(text=f"Dialogue : {dialogue}")

        # Quests
        quest_data = self.controller.req.sendRequestsToDB("""
        SELECT quest_name
        FROM pnjs_quest
        WHERE pnj_name = %s
        """, (name,), "get npc's quests")

        quests = []
        if not quest_data:
            self.quest_combobox.config(values=[])
            self.quest_combobox.set("No quests available")
        else:
            quests = [quest["quest_name"] for quest in quest_data]
            self.quest_combobox.config(values=quests)
            self.quest_combobox.set("Select quest to accept")
    
        # Objects
        object_data = self.controller.req.sendRequestsToDB("""
        SELECT o.name AS object_name, o.price
        FROM pnjs_object po
        JOIN object o ON po.object_name = o.name
        WHERE po.pnj_name = %s
        """, (name,), "get npc's objects")

        objects = []
        if not object_data:
            self.object_combobox.config(values=[])
            self.object_combobox.set("No objects available")
        else:
            objects = [f"{obj['object_name']} - {obj['price']}g" for obj in object_data]
            self.object_combobox.config(values=objects)
            self.object_combobox.set("Select object to buy")

        # Inventory
        self.load_player_inventory()

        
    def load_player_inventory(self):
        username = self.controller.username

        data = self.controller.req.sendRequestsToDB("""
        SELECT o.name AS object_name, o.price
        FROM player_object po
        JOIN object o ON po.object_name = o.name
        WHERE po.player_id = (SELECT id FROM player WHERE username = %s)
        """, (username,), "get player's inventory")

        if not data:
            self.sell_combobox.config(values=[])
            self.sell_combobox.set("No items in inventory")
            return
        
        items = [f"{item['object_name']} - {item['price']}g" for item in data]
        self.sell_combobox.config(values=items)
        self.sell_combobox.set("Select object to sell")

    def accept_selected_quest(self):
        quest_name = self.quest_combobox.get()
        if quest_name == "No quests available" or not quest_name:
            self.result_label.config(text="No quests available to accept.")
            return
        
        username = self.controller.username

        self.controller.req.sendRequestsToDB("""
            INSERT INTO player_quest (player_id, quest_name, status)
            VALUES ((SELECT id FROM player WHERE username = %s), %s, 'in_progress')
            ON CONFLICT (player_id, quest_name) DO NOTHING
        """, (username, quest_name), "accept npc quest")
        
        self.controller.req.commit_transactions()
        self.result_label.config(text=f"Quest '{quest_name}' accepted!")

        # Update the quest frame
        self.controller.frames["quests"].load_available_quests()

    def buy_item(self):
        item = self.object_combobox.get()
        item_name = item.split(" - ")[0] if item else None
        if not item_name:
            self.result_label.config(text="Select an item to buy.")
            return
        
        username = self.controller.username

        # Get the player's money
        data = self.controller.req.sendRequestsToDB("""
            SELECT money FROM player WHERE username = %s
        """, (username,), "get player's money")
        
        if not data:
            self.result_label.config(text="Player not found.")
            return
        
        player_money = data[0]["money"]

        # Get the price of the item
        item_data = self.controller.req.sendRequestsToDB("""
            SELECT price FROM object WHERE name = %s
        """, (item_name,), "get item's price")
        
        if not item_data:
            self.result_label.config(text="Item not found.")
            return
        
        item_price = item_data[0]["price"]

        # Check if the player has enough money
        if player_money < item_price:
            self.result_label.config(text="Not enough money to buy this item.")
            return

        # Buy the item
        self.controller.req.sendRequestsToDB("""
            INSERT INTO player_object (player_id, object_name)
            VALUES ((SELECT id FROM player WHERE username = %s), %s)
            ON CONFLICT DO NOTHING
        """, (username, item_name), "buy item")

        # Deduct the money
        self.controller.req.sendRequestsToDB("""
            UPDATE player SET money = money - %s WHERE username = %s
        """, (item_price, username), "deduct money")

        self.controller.req.commit_transactions()
        
        self.result_label.config(text=f"Bought {item_name} for {item_price} gold!")
        
        # Update the inventory combobox
        self.load_player_inventory()
        # Update the home and inventory frame
        self.controller.frames["home"].load_username_info()
        self.controller.frames["inventory"].loadInventory()

    
    def sell_item(self):
        item = self.sell_combobox.get()
        item_name = item.split(" - ")[0] if item else None
        if not item_name:
            self.result_label.config(text="Select an item to sell.")
            return
        
        username = self.controller.username

        # Get the price of the item
        item_data = self.controller.req.sendRequestsToDB("""
            SELECT price FROM object WHERE name = %s
        """, (item_name,), "get item's price")
        
        if not item_data:
            self.result_label.config(text="Item not found.")
            return
        
        item_price = item_data[0]["price"]

        # Sell the item
        self.controller.req.sendRequestsToDB("""
            DELETE FROM player_object WHERE player_id = (SELECT id FROM player WHERE username = %s) AND object_name = %s
        """, (username, item_name), "sell item")

        # Add the money back to the player
        self.controller.req.sendRequestsToDB("""
            UPDATE player SET money = money + %s WHERE username = %s
        """, (item_price, username), "add money from selling")

        self.controller.req.commit_transactions()
        
        self.result_label.config(text=f"Sold {item_name} for {item_price} gold!")

        # Update the inventory combobox
        self.load_player_inventory()
        # Update the home and inventory frame
        self.controller.frames["home"].load_username_info()
        self.controller.frames["inventory"].loadInventory()
        
