import requests

import tkinter as tk
from tkinter import ttk


def combo_box_select_item(event):
    selected_item = comboBox.get()
    res_list.delete(0, tk.END)
    req = requests.Requests()

    match selected_item:
        case "Gold":
            data = req.getTop10Gold()
            for row in data:
                row_dict = dict(row)
                res_list.insert(tk.END, f"{row_dict["username"]} : {row_dict["money"]}")
            return
        case "Characters from the same class":
            data = req.getPlayerMostCharClass()
            for row in data:
                row_dict = dict(row)
                res_list.insert(tk.END, f"{row_dict["username"]} : {row_dict["class"]},"
                                        f" {row_dict["nb_characters"]}")

            return
        case "Gold per Quest":
            data = req.getBestRewardPerLvl()
            for row in data:
                row_dict = dict(row)
                res_list.insert(tk.END, f"{row_dict["name"]}, level {row_dict["difficulty"]} : "
                                        f"{row_dict["money"]}")
            return
        case "Richest NPC":
            data = req.getNpcMostGold()
            for row in data:
                row_dict = dict(row)
                res_list.insert(tk.END, f"{row_dict["pnj_name"]} : {row_dict["total_value"]}")
            return
        case "Most common object for level five quests":
            data = req.getMostCommonItemTypeLvl5()
            for row in data:
                row_dict = dict(row)
                print(row_dict)
                # res_list.insert(tk.END, f"{row_dict["pnj_name"]} : {row_dict["total_value"]}")
            return
        case "Monsters with the best rewards in cumulative gold value based on their health points":
            data = req.getMonsterHighestReward()
            for row in data:
                row_dict = dict(row)
                res_list.insert(tk.END, f"{row_dict["name"]} : (Health){row_dict["health"]} "
                                        f"(money){row_dict["money"]}")
            return

    return


app = tk.Tk()
app.title("DataBase Project")
app.config(width=400, height=700)

headline = tk.Label(app, text="LeaderBord", font=("times new roman", 16))
headline.place(x=20, y=20)

label = tk.Label(app, text="Choose criteria : ", font=("times new roman", 14))
label.place(x=40, y=60)

comboBox = ttk.Combobox(app, values=["Gold", "Characters from the same class", "Gold per Quest", "Richest NPC",
                                     "Most common object for level five quests",
                                     "Monsters with the best rewards in cumulative "
                                     "gold value based on their health points"])

comboBox.place(x=60, y=100)
comboBox.bind("<<ComboboxSelected>>", combo_box_select_item)

frame = tk.Frame(app, height=530, width=320, bg="SystemButtonFace", bd=0)
frame.place(x=60, y=140)
frame.propagate(False)

scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

res_list = tk.Listbox(frame, yscrollcommand=scrollbar.set, border=False, bg="SystemButtonFace", font=("times new roman",
                                                                                                      12), bd=0)

res_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=res_list.yview)

app.mainloop()
