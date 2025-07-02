import json
import customtkinter as ctk
import calendar
import pandas as pd
from datetime import date, datetime, timedelta
from Heatmap import Heatmap


class Dashboard(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master)
        self.main_label()
        self.create_grid()

        # divider frame
        self.description_frame = ctk.CTkFrame(self)
        self.description_frame_grid()
        self.description_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        self.total = 0
        self.balance_value = 0

        self.balance = None
        self.expenses = None
        self.budget = None
        self.color = "black"

        self.create_cards()
        self.render_cards()

        # Refresh Button
        self.refresh_butt = ctk.CTkButton(self.description_frame, text="↻", font=("", 24, "bold"), command=self.refresh)
        self.refresh_butt.grid(row=1, column=0, pady=10, padx=20, sticky="nsw")

        # Heat Map
        current_year = datetime.now().year
        self.start_date = date(current_year, 1, 1)

        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            self.frequency_table = df[["date"]].value_counts()

        self.heatmap = Heatmap(self, self.start_date, self.frequency_table, None)
        self.heatmap.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    def main_label(self):
        label = ctk.CTkLabel(master=self, text="Dashboard", font=("", 30, "bold"))
        label.grid(row=0, column=0, sticky="nsw", pady=10, padx=20)

    def create_grid(self):
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=70)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def description_frame_grid(self):
        self.description_frame.rowconfigure(0, weight=20)
        self.description_frame.rowconfigure(1, weight=1)
        self.description_frame.rowconfigure(2, weight=30)
        self.description_frame.columnconfigure(0, weight=1)
        self.description_frame.columnconfigure(1, weight=1)
        self.description_frame.columnconfigure(2, weight=1)

    def create_cards(self):
        self.balance = Flashcard(self.description_frame, "Balance", self.get_balance(), "#478af5", text_color=self.color)
        self.expenses = Flashcard(self.description_frame, "Expenses", self.get_expenses(), "#478af5")
        self.budget = Flashcard(self.description_frame, "Budget", "0.0", "#478af5")

    def render_cards(self):
        self.balance.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.expenses.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)
        self.budget.grid(row=2, column=2, sticky="nsew", padx=20, pady=10)

    def get_expenses(self):
        total = 0
        with open("Transactions.json", "r") as f:
            file_data = json.load(f)
            transactions = file_data["Transactions"]
            for entry in transactions:
                if entry["type"] == "Expense":
                    total += entry["amount"]
            self.total = total
            return total

    def get_balance(self):
        inc = 0
        with open("Transactions.json", "r") as f:
            file_data = json.load(f)
            transactions = file_data["Transactions"]
            for entry in transactions:
                if entry["type"] == "Income":
                    inc += entry["amount"]
            self.balance_value = inc - self.get_expenses()
            if self.balance_value > 0:
                self.color = "#0cf223"
            elif self.balance_value < 0:
                self.color = "red"
            return self.balance_value

    def refresh(self):
        self.create_cards()
        self.render_cards()


class Flashcard(ctk.CTkFrame):

    def __init__(self, master, title, text, color, text_color="black"):
        super().__init__(master=master, fg_color=color)
        self.title = ctk.CTkLabel(self, text=title, font=("", 16, "bold"), text_color="black")
        self.text = ctk.CTkLabel(self, text=text, font=("", 14, "bold"), text_color=text_color)
        self.display_text()

    def display_text(self):
        self.title.pack(padx=10, pady=5)
        self.text.pack(padx=10, pady=5)

