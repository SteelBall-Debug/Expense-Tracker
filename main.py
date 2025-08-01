# Personal Finance/Expense Tracker App made using Custom tkinter

import customtkinter as ctk
from Dashboard import Dashboarder
from Settings import Settings
from Tabular_view import Table
import os
import sys


class App(ctk.CTk):

    def __init__(self, title, size):

        # main-setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        # grid configure
        self.grid()

        # Sidebar
        self.sidebar = Sidebar(self, "#159947")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Dashboard
        self.dashboard = Dashboarder(self)
        # DESTROYS graphs on exiting the app
        self.protocol("WM_DELETE_WINDOW", self.dashboard.graphs.on_close)

        # Tabular-View
        self.table_view = Table(self, self.dashboard)

        # Settings
        self.settings = Settings(self)

        self.grid_dash()

        self.mainloop()

    def grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=75)

    def grid_dash(self):
        self.destroy_grids()
        self.dashboard.grid(row=0, column=1, sticky="nsew")
        self.dashboard.lift()

    def grid_table(self):
        self.destroy_grids()
        self.table_view.grid(row=0, column=1, sticky="nsew")
        self.table_view.lift()

    def grid_settings(self):
        self.destroy_grids()
        self.settings.grid(row=0, column=1, sticky="nsew")
        self.settings.lift()

    def destroy_grids(self):
        self.dashboard.grid_forget()
        self.table_view.grid_forget()
        self.settings.grid_forget()

    def apply_updates(self):
        pass


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, color):         # #478af5 - light blue for buttons, #1054c2 - sidebar

        super().__init__(master, fg_color=color, bg_color=color)
        self.parent = master
        self.sidebar_grid()
        self.create_widgets()

    def sidebar_grid(self):
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=26)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def create_widgets(self):
        dash_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Dashboard", command=self.parent.grid_dash, text_color="#ffffff", font=("", 16, "bold"))
        dash_button.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        table_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Table-view", command=self.parent.grid_table, text_color="#ffffff", font=("", 16, "bold"))
        table_button.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)

        settings_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Settings", command=self.parent.grid_settings, text_color="#ffffff", font=("", 16, "bold"))
        settings_button.grid(row=3, column=0, sticky="nsew", pady=5, padx=5)


if __name__ == "__main__":
    App("eXp", (800, 500))      # App( title, geometry(tuple) )
    # first commit
