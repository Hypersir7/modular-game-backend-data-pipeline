import tkinter as tk
import requests

import loginFrame
import signupFrame
import leaderboardFrame
import homeFrame


class Application(tk.Tk):
    req = requests.Requests()
    currently_visible_frame_id = "login"
    username = ""

    def __init__(self):
        super().__init__()

        self.geometry("700x700")
        self.title("DataBase Project")
        container_frame = tk.Frame(self)
        container_frame.config(width=700, height=700)
        container_frame.place(x=0, y=0)

        self.frames = {"login": loginFrame.LongInFrame(container_frame, self),
                       "signup": signupFrame.SignUpFrame(container_frame, self),
                       "leaderboard": leaderboardFrame.LeaderBoardFrame(container_frame, self),
                       "home": homeFrame.HomeFrame(container_frame, self)}

        self.frames[self.currently_visible_frame_id].config_controller_dimensions()
        self.frames[self.currently_visible_frame_id].place(x=0, y=0)

        self.mainloop()

    def show_frame(self, frame_id):
        self.frames[self.currently_visible_frame_id].place_forget()
        self.frames[frame_id].config_controller_dimensions()
        self.frames[frame_id].place(x=0, y=0)
        self.currently_visible_frame_id = frame_id


my_app = Application()
