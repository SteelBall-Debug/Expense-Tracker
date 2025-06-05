import customtkinter as ctk


class Dashboard(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master)
        self.main_label()

    def main_label(self):
        label = ctk.CTkLabel(master=self, text="Dashboard", font=("", 24, "bold"))
        label.pack(side='top')
