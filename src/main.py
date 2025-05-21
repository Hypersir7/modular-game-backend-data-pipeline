
import tkinter as tk
from tkinter import ttk


def combo_box_select_item(event):
    # rien pour le moment
    res_list.insert(tk.END, "Hello world !")
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
