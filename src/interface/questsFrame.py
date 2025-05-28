import tkinter as tk
from tkinter import ttk

class QuestsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=600)

        self.title_label = tk.Label(self, text="Available Quests", font=("times new roman", 16))
        self.title_label.place(x=20, y=10)

        self.quest_listbox = tk.Listbox(self, height=10, width=70)
        self.quest_listbox.place(x=20, y=50)

        self.back_button = tk.Button(self, text="Home", borderwidth=0, fg="blue",
                                     activeforeground="black", command=lambda: controller.show_frame("home"))
        self.back_button.place(x=650, y=10)

        self.validate_button = tk.Button(self, text="Validate Quest", command=self.validate_selected_quest)
        self.validate_button.place(x=20, y=250)

        self.result_label = tk.Label(self, text="", font=("times new roman", 12), fg="green")
        self.result_label.place(x=20, y=300)

        self.quest_detail_label = tk.Label(self, text="", font=("times new roman", 10))
        self.quest_detail_label.place(x=20, y=360)

        self.quest_listbox.bind("<<ListboxSelect>>", self.display_quest_details)

        self.load_available_quests()

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")

    def load_available_quests(self):
        self.quest_listbox.delete(0, tk.END)
        username = self.controller.username

        data = self.controller.req.sendRequestsToDB("""
            SELECT q.name, q.description
            FROM quest q
            WHERE q.name NOT IN (
                SELECT pq.quest_name
                FROM player_quest pq
                JOIN player p ON p.id = pq.player_id
                WHERE p.username = %s AND pq.status = 'completed'
            )
        """, (username,), "load available quests")

        for row in data:
            self.quest_listbox.insert(tk.END, row["name"])

    def validate_selected_quest(self):
        selection = self.quest_listbox.curselection()
        if not selection:
            self.result_label.config(text="Please select a quest.")
            return

        quest_name = self.quest_listbox.get(selection[0])
        username = self.controller.username

        # Get rewards
        rewards = self.controller.req.sendRequestsToDB("""
            SELECT xp, money FROM quest WHERE name = %s
        """, (quest_name,), "get quest rewards")[0]

        xp_reward = rewards["xp"]
        money_reward = rewards["money"]

        # Update player XP and money
        self.controller.req.sendRequestsToDB("""
            UPDATE player
            SET xp = xp + %s, money = money + %s
            WHERE username = %s
        """, (xp_reward, money_reward, username), "reward player")

        # Mark quest as completed
        self.controller.req.sendRequestsToDB("""
            INSERT INTO player_quest (player_id, quest_name, status)
            VALUES (
                (SELECT id FROM player WHERE username = %s),
                %s,
                'completed'
            )
            ON CONFLICT (player_id, quest_name) DO UPDATE SET status = 'completed'
        """, (username, quest_name), "mark quest as completed")

        # Give object rewards (if any)
        object_rewards = self.controller.req.sendRequestsToDB("""
            SELECT object_name FROM quest_object WHERE quest_name = %s
        """, (quest_name,), "get quest object rewards")

        for obj in object_rewards:
            self.controller.req.sendRequestsToDB("""
                INSERT INTO player_object (player_id, object_name)
                SELECT id, %s FROM player WHERE username = %s
                ON CONFLICT DO NOTHING
            """, (obj["object_name"], username), "give player object reward")

        self.controller.req.commit_transactions()

        self.result_label.config(text="Quest completed! Rewards received.")
        self.load_available_quests()

        # to visually update the rewards (exp, gold) and items after each completed quest on the homeframe & inventory:
        self.controller.frames["home"].load_username_info()
        self.controller.frames["inventory"].loadInventory()

    
    def display_quest_details(self, event):
        selection = self.quest_listbox.curselection()
        if not selection:
            self.quest_detail_label.config(text="")
            return
        
        quest_name = self.quest_listbox.get(selection[0])


        # To display EXP and GOLD rewards & Description
        data = self.controller.req.sendRequestsToDB("""
            SELECT xp, money, description
            FROM quest
            WHERE name = %s
        """, (quest_name,), "get quest details")


        # to display the objects rewards
        object_data = self.controller.req.sendRequestsToDB("""
        SELECT object_name
        FROM quest_object
        WHERE quest_name = %s
        """, (quest_name,), "get quest object rewards")

        if data:
            quest = data[0]
            objects = ", ".join([obj['object_name'] for obj in object_data]) or "None"

            detail_text =(
                f"XP Reward: {quest['xp']} XP\n"
                f"Money Reward: {quest['money']} gold coins\n\n"
                f"Object Rewards: {objects}\n\n"
                f"Description:\n{quest['description']}"
            )
            self.quest_detail_label.config(text=detail_text)
        else:
            self.quest_detail_label.config(text="No details available.")
