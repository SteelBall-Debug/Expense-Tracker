# Personal Finance/Expense Tracker App made using Custom tkinter

import customtkinter as ctk
from tkinter import Label
import webbrowser
from Scripts.Dashboard import Dashboard
from Scripts.Settings import Settings
from Scripts.Tabular_view import Table

onboarding_msg = [
    "We’re excited to have you on board. Here’s how to get started:",
    "⚬  Add Transactions: Open the Transactions tab in the sidebar and click the '+' button to start recording your expenses or income.",
    "⚬  View Your Dashboard: The Dashboard provides a clear, detailed analysis of all your transactions.",
    "⚬  Manage Categories & Users: Go to Settings to add or remove transaction categories or manage users.",
    "⚬  Troubleshooting: If something isn’t working as expected, try the refresh buttons.",
    "⚬  Reporting Issues: Still having trouble? Please submit a detailed bug report with screenshots to our GitHub page."
    , "Happy tracking, and here’s to smarter spending!"
]

link_url = "https://github.com/SteelBall-Debug"


class App(ctk.CTk):

    def __init__(self, title, size):

        # main-setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.iconbitmap(self, "Assets/logo.ico")

        # grid configure
        self.grid()

        # Sidebar
        self.sidebar = Sidebar(self, "#159947")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Dashboard
        self.dashboard = Dashboard(self)
        # DESTROYS graphs on exiting the app
        self.protocol("WM_DELETE_WINDOW", self.dashboard.graphs.on_close)

        # Tabular-View
        self.table_view = Table(self, self.dashboard)

        # Settings
        self.settings = Settings(self)

        self.onboarding_frame = None
        self.onboarding_screen()

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
        self.onboarding_frame.grid_forget()

    def apply_updates(self):
        self.dashboard = Dashboard(self)
        self.protocol("WM_DELETE_WINDOW", self.dashboard.graphs.on_close)
        self.table_view = Table(self, self.dashboard)

    def onboarding_screen(self):
        self.onboarding_frame = ctk.CTkFrame(self, fg_color="#151d28", bg_color="#151d28")

        onboarding_title = ctk.CTkLabel(self.onboarding_frame, text="Welcome to the Koin Expense-Tracker!",
                                             font=("Literata 12pt", 25, "bold"))
        onboarding_title.grid(row=0, column=1, padx=10, pady=7, sticky="nw")

        row = 2
        for sentence in onboarding_msg:
            label = ctk.CTkLabel(self.onboarding_frame, text=sentence, font=("Literata 12pt", 18))
            label.grid(row=row, column=1, padx=10, pady=7, sticky="nw")
            row += 1

        link_label = Label(self.onboarding_frame, text="Github/SteelBall-Debug", fg="#6495ED", bg="#151d28", cursor="hand2"
                           , font=("Literata 12pt", 17))
        link_label.grid(row=9, column=1, padx=10, pady=7, sticky="nw")

        link_label.bind("<Button-1>", lambda e: webbrowser.open(link_url))

        self.onboarding_frame.grid(row=0, column=1, sticky="nsew")


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
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=26)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)

    def create_widgets(self):
        dash_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Dashboard", command=self.parent.grid_dash, text_color="#ffffff", font=("", 16, "bold"))
        dash_button.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        table_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Table-view", command=self.parent.grid_table, text_color="#ffffff", font=("", 16, "bold"))
        table_button.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)

        settings_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Settings", command=self.parent.grid_settings, text_color="#ffffff", font=("", 16, "bold"))
        settings_button.grid(row=3, column=0, sticky="nsew", pady=5, padx=5)

        help_button = ctk.CTkButton(master=self, fg_color="#49b265", hover_color="#1f5f5b", text="Help",
                                    command=self.parent.onboarding_screen, text_color="#ffffff",
                                    font=("", 16, "bold"))
        help_button.grid(row=4, column=0, sticky="nsew", pady=5, padx=5)


if __name__ == "__main__":
    App("Koin", (800, 500))      # App( title, geometry(tuple) )
    # first commit
