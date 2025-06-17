import json
import customtkinter as ctk


class Dashboard(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master)
        self.main_label()
        self.create_grid()

        self.total = 0
        self.balance_value = 0

        self.balance = None
        self.expenses = None
        self.budget = None

        self.create_cards()
        self.render_cards()

        # Refresh Button
        self.refresh_butt = ctk.CTkButton(self, text="↻", font=("", 24, "bold"), command=self.refresh)
        self.refresh_butt.grid(row=1, column=0, pady=10, padx=20, sticky="nsw")

    def main_label(self):
        label = ctk.CTkLabel(master=self, text="Dashboard", font=("", 30, "bold"))
        label.grid(row=0, column=0, sticky="nsw", pady=10, padx=20)

    def create_grid(self):
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=30)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def create_cards(self):
        self.balance = Flashcard(self, "Balance", self.get_balance(), "#478af5")
        self.expenses = Flashcard(self, "Expenses", self.get_expenses(), "#478af5")
        self.budget = Flashcard(self, "Budget", "0.0", "#478af5")

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
            return self.balance_value

    def refresh(self):
        self.create_cards()
        self.render_cards()


class Flashcard(ctk.CTkFrame):

    def __init__(self, master, title, text, color):
        super().__init__(master=master, fg_color=color)
        self.title = ctk.CTkLabel(self, text=title, font=("", 16, "bold"), text_color="black")
        self.text = ctk.CTkLabel(self, text=text, font=("", 14, "bold"), text_color="black")
        self.display_text()

    def display_text(self):
        self.title.pack(padx=10, pady=5)
        self.text.pack(padx=10, pady=5)

    def update_color(self, color):
        self.text.configure(text_color=color)
