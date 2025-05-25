
import tkinter as tk
from tkinter import ttk


class LeaderBoardFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(width=400, height=700)

        headline = tk.Label(self, text="Leaderboard", font=("times new roman", 16))
        headline.place(x=20, y=20)

        label = tk.Label(self, text="Choose criteria : ", font=("times new roman", 14))
        label.place(x=40, y=60)

        self.comboBox = ttk.Combobox(self, values=["Gold", "Characters from the same class", "Gold per Quest",
                                                   "Richest NPC",
                                                   "Most common object for level five quests",
                                                   "Monsters with the best rewards in cumulative gold value based on "
                                                   "their health points"])

        self.comboBox.place(x=60, y=100)
        self.comboBox.bind("<<ComboboxSelected>>", self.combo_box_select_item)

        frame = tk.Frame(self, height=530, width=320, bd=0)
        frame.place(x=60, y=140)
        frame.propagate(False)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.res_list = tk.Listbox(frame, yscrollcommand=scrollbar.set, border=False,
                                   font=("times new roman", 12), bd=0)

        self.res_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.res_list.yview)

    def combo_box_select_item(self, event):
        selected_item = self.comboBox.get()
        self.res_list.delete(0, tk.END)

        match selected_item:
            case "Gold":
                data = self.controller.req.getTop10Gold()
                for row in data:
                    row_dict = dict(row)
                    self.res_list.insert(tk.END, f"{row_dict["username"]} : {row_dict["money"]}")
                return
            case "Characters from the same class":
                data = self.controller.req.getPlayerMostCharClass()
                for row in data:
                    row_dict = dict(row)
                    self.res_list.insert(tk.END, f"{row_dict["username"]} : {row_dict["class"]}, "
                                                 f"{row_dict["nb_characters"]}")

                return
            case "Gold per Quest":
                data = self.controller.req.getBestRewardPerLvl()
                for row in data:
                    row_dict = dict(row)
                    self.res_list.insert(tk.END, f"{row_dict["name"]}, level {row_dict["difficulty"]} : "
                                                 f"{row_dict["money"]}")
                return
            case "Richest NPC":
                data = self.controller.req.getNpcMostGold()
                for row in data:
                    row_dict = dict(row)
                    self.res_list.insert(tk.END, f"{row_dict["pnj_name"]} : {row_dict["total_value"]}")
                return
            case "Most common object for level five quests":
                data = self.controller.req.getMostCommonItemTypeLvl5()
                for row in data:
                    row_dict = dict(row)
                    print(row_dict)
                    # res_list.insert(tk.END, f"{row_dict["pnj_name"]} : {row_dict["total_value"]}")
                return
            case "Monsters with the best rewards in cumulative gold value based on their health points":
                data = self.controller.req.getMonsterHighestReward()
                for row in data:
                    row_dict = dict(row)
                    self.res_list.insert(tk.END, f"{row_dict["name"]} : (Health){row_dict["health"]} "
                                                 f"(money){row_dict["money"]}")
                return

        return

    def config_controller_dimensions(self):
        self.controller.geometry("400x700")
