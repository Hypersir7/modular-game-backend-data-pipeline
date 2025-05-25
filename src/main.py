import tkinter as tk
import requests

import loginFrame
import signupFrame
import leaderboardFrame
import homeFrame
import charactersFrame


class Application(tk.Tk):
    req = requests.Requests()
    currently_visible_frame_id = "login"
    username = ""

    def __init__(self):
        super().__init__()

        self.geometry("700x700")
        self.title("DataBase Project")
        self.container_frame = tk.Frame(self)
        self.container_frame.config(width=700, height=700)
        self.container_frame.place(x=0, y=0)

        self.frames = {"login": loginFrame.LongInFrame(self.container_frame, self),
                       "signup": signupFrame.SignUpFrame(self.container_frame, self),
                       "leaderboard": leaderboardFrame.LeaderBoardFrame(self.container_frame, self)}

        self.frames[self.currently_visible_frame_id].config_controller_dimensions()
        self.frames[self.currently_visible_frame_id].place(x=0, y=0)

        self.mainloop()

    def show_frame(self, frame_id):
        self.frames[self.currently_visible_frame_id].place_forget()
        self.frames[frame_id].config_controller_dimensions()
        self.frames[frame_id].place(x=0, y=0)
        self.currently_visible_frame_id = frame_id

    def make_home_frame(self):
        self.frames["home"] = homeFrame.HomeFrame(self.container_frame, self)
        self.frames["characters"] = charactersFrame.CharactersFrame(self.container_frame, self)
        self.show_frame("home")

    def logout(self):
        self.frames["login"] = loginFrame.LongInFrame(self.container_frame, self)
        self.frames["signup"] = signupFrame.SignUpFrame(self.container_frame, self)
        self.show_frame("login")


my_app = Application()
