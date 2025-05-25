from PIL import Image, ImageTk
import tkinter as tk

import tooltip


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=700, height=700)

        self.username_label = tk.Label(self, font=("times new roman", 16))
        self.username_label.place(x=20, y=10)
        # level
        self.shield_img = ImageTk.PhotoImage(Image.open("imgs/sword_shield.png").resize((26, 26)))
        self.level_img = tk.Label(self, image=self.shield_img)
        self.level_img.place(x=20, y=40)
        self.level_label = tk.Label(self, font=("times new roman", 16))
        self.level_label.place(x=70, y=40)

        tooltip.ToolTip(self.level_img, "Level")

        # xp
        self.fire_img = ImageTk.PhotoImage(Image.open("imgs/blue fire.png").resize((28, 28)))
        self.xp_img = tk.Label(self, image=self.fire_img)
        self.xp_img.place(x=20, y=70)
        self.xp_label = tk.Label(self, font=("times new roman", 16))
        self.xp_label.place(x=70, y=70)

        tooltip.ToolTip(self.xp_img, "Xp")

        # gold
        self.gold_img = ImageTk.PhotoImage(Image.open("imgs/gold.png").resize((38, 38)))
        self.money_img = tk.Label(self, image=self.gold_img)
        self.money_img.place(x=20, y=100)
        self.money_label = tk.Label(self, font=("times new roman", 16))
        self.money_label.place(x=70, y=110)

        tooltip.ToolTip(self.money_img, "Gold")
        # ==========================================================================================

        self.load_username_info()

        self.logout_button = tk.Button(self, text="Logout", borderwidth=0, fg="blue", activeforeground="black",
                                       command=lambda: self.controller.logout())
        self.logout_button.place(x=645, y=10)

        self.characters_button = tk.Button(self, text=" > Characters", font=("times new roman", 12), fg="blue",
                                           activeforeground="black", borderwidth=0,
                                           command=lambda: self.controller.show_frame("characters"))
        self.characters_button.place(x=20, y=150)

        self.leaderboard_button = tk.Button(self, text=" > LeaderBoard", font=("times new roman", 12), fg="blue",
                                            activeforeground="black", borderwidth=0,
                                            command=lambda: self.controller.show_frame("leaderboard"))
        self.leaderboard_button.place(x=20, y=180)

    def config_controller_dimensions(self):
        self.controller.geometry("700x700")

    def load_username_info(self):
        username = self.controller.username
        self.username_label.config(text=f"{username}")
        data = self.controller.req.sendRequestsToDB("""
        SELECT level, xp, money
        FROM player p
        WHERE p.username = %s
        """, (username,), "getting the user's info")

        level = data[0]["level"]
        xp = data[0]["xp"]
        money = data[0]["money"]

        self.level_label.config(text=f"{level}")
        self.xp_label.config(text=f"{xp}")
        self.money_label.config(text=f"{money}")
