import json
import customtkinter as ctk
import pandas as pd
from datetime import date, datetime
from tkinter import ttk
from Heatmap import Heatmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from Settings import CATEGORIES, USERS



class Dashboarder(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master, fg_color="#090a14",  bg_color="#090a14")
        self.main_label()
        self.create_grid()

        # divider frame
        self.description_frame = ctk.CTkFrame(self, fg_color="#090a14")
        self.description_frame_grid()
        self.description_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        self.total = 0
        self.balance_value = 0

        self.balance = None
        self.expenses = None
        self.budget = None
        self.color = "white"

        self.create_cards()
        self.render_cards()

        # Refresh Button
        self.refresh_butt = ctk.CTkButton(self.description_frame, text="↻", font=("", 24, "bold"), command=self.refresh, fg_color="#468232")
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
        self.heatmap.grid(row=2, column=0, sticky="nsw", padx=20, pady=10)

        self.indicator = ctk.CTkFrame(self, width=300, height=40, fg_color="#090a14")
        self.indicator.grid_propagate(False)
        self.indicator.grid(row=3, column=0, sticky="nw", padx=20, pady=1)

        self.indicator_title = ctk.CTkLabel(self.indicator, text="click value returned here", text_color="white",
                                            font=("", 14, "italic"))
        self.indicator_title.grid(row=0, column=1, sticky="ns", padx=10)

        self.indicator_text = ctk.CTkLabel(self.indicator, text="No transactions", text_color="red")

        # mini tree-view
        self.columns = ("Sr.no.", "Date", "User", "Type", "Category", "Amount", "Note")
        self.mini_tree = ttk.Treeview(self, columns=self.columns, show="headings", height=10)

        ctk.CTkLabel(self, text="Data Visualization", font=("", 25, "bold")).grid(row=5, column=0, sticky="sw", pady=60, padx=10)
        self.graphs = Graph(self)
        self.graphs.grid(row=6, column=0, sticky="nsew")

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
        self.balance = Flashcard(self.description_frame, "Balance", round(self.get_balance(), 2), "#151d28", text_color=self.color)
        self.expenses = Flashcard(self.description_frame, "Expenses",  round(self.get_expenses(), 2), "#151d28")
        self.budget = Flashcard(self.description_frame, "Budget", "0.0", "#151d28")

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
        self.update_heatmap()
        self.graphs.destroy()
        self.graphs = Graph(self)
        self.graphs.grid(row=6, column=0, sticky="nsew")

    def show_indicator(self):
        self.indicator_title.configure(text=self.heatmap.last_clicked)

    def clear_table(self):
        for item in self.mini_tree.get_children():
            self.mini_tree.delete(item)

    def setup_table(self):
        for column in self.columns:
            self.mini_tree.heading(column, text=column)
            self.mini_tree.column(column, anchor="center", width=200)

        style = ttk.Style()
        style.theme_use("default")
        # enlarge row size and font
        style.configure("Treeview",
                        background="#151d28",
                        foreground="white",
                        rowheight=40,
                        fieldbackground="#151d28",
                        font=("Segoe UI", 14))
        # style Header cells
        style.configure("Treeview.Heading",
                        background="#25562e",  # <-- Header background
                        foreground="white",  # <-- Header text color
                        font=("Segoe UI", 14, "bold"))
        style.configure("Treeview.Heading", font=("Segoe UI", 16, "bold"))  # enlarge heading fonts
        style.map('Treeview', background=[('selected', '#1f6aa5')])

        self.mini_tree.tag_configure("highlight", background="#1fc500")
        self.mini_tree.grid(row=4, column=0, sticky="nsew", padx=20, pady=1)

    def update_heatmap(self):
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            self.frequency_table = df[["date"]].value_counts()
            self.heatmap.refresh(self.frequency_table)

            date_to_ids = {}
            for row in df.itertuples(index=False):
                date_val = row.date
                tx_id = row.id
                # print(f"{date_val} : {tx_id}")
                if date_val not in date_to_ids:
                    date_to_ids[date_val] = []
                date_to_ids[date_val].append(tx_id)
            self.update_cache(date_to_ids)

    def update_cache(self, new_data):
        with open("Cache.json", "r+") as f:
            file_data = json.load(f)
            new_data = new_data
            file_data["id_lookup"].update(new_data)

            f.seek(0)
            json.dump(file_data, f, indent=4)


class Flashcard(ctk.CTkFrame):

    def __init__(self, master, title, text, color, text_color="#ebede9"):
        super().__init__(master=master, fg_color=color)
        self.title = ctk.CTkLabel(self, text=title, font=("", 16, "bold"), text_color="#ebede9")
        self.text = ctk.CTkLabel(self, text=text, font=("", 14, "bold"), text_color=text_color)
        self.display_text()

    def display_text(self):
        self.title.pack(padx=10, pady=5)
        self.text.pack(padx=10, pady=5)


class Graph(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="#090a14")

        # Pie Chart (Category Data)
        df = self.category_expenses()
        plt.style.use("dark_background")
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(df["Total"], labels=df["Category"], autopct='%1.1f%%')
        ax1.set_title("Category-wise Expenses")
        fig1.set_facecolor('#090a14')
        # self.plot_to_ctk(fig1).pack(padx=10, pady=10, side="left")
        self.plot_to_ctk(fig1).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Line Chart (Income and Expense Data)
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        income = self.income_data()
        expense = self.expense_data()
        income["amount"].plot(ax=ax2, label="Income", marker="o")
        expense["amount"].plot(ax=ax2, label="Expense", marker="x")
        ax2.set_title("Income vs Expense")
        ax2.set_ylabel("Amount")
        ax2.legend()
        fig2.set_facecolor('#090a14')
        self.plot_to_ctk(fig2).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Bar chart (User Data)
        df = self.user_expenses()
        fig3, ax3 = plt.subplots(figsize=(7, 5))
        sns.barplot(data=df, x="Users", y="Total", hue="Users", legend=False)
        fig3.set_facecolor('#090a14')
        ax3.set_title("Total Spend by Users")
        self.plot_to_ctk(fig3).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def user_expenses(self):
        cf = pd.DataFrame({'Users': [], 'Total': []})
        labels = ['You', 'Jane', "John"] + USERS
        cat_label = list(set(labels))
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            df = df.query('type == "Expense"')

            for label in cat_label:
                temp = df.query(f'user == "{label}"')
                total = temp["amount"].sum()
                new_row = {'Users': label, 'Total': total}
                cf = cf._append(new_row, ignore_index=True)

        return cf

    def income_data(self):
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            income_df = df.query('type == "Income"')
            return income_df

    def expense_data(self):
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            expense_df = df.query('type == "Expense"')
            return expense_df

    def category_expenses(self):
        cf = pd.DataFrame({'Category': [], 'Total': []})
        labels = ["food", "clothing", "entertainment", "bills", "repairs", "misc"] + CATEGORIES
        cat_label = list(set(labels))
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            df = df.query('type == "Expense"')

            for label in cat_label:
                temp = df.query(f'category == "{label}"')
                total = temp["amount"].sum()
                new_row = {'Category': label, 'Total': total}
                cf = cf._append(new_row, ignore_index=True)

        return cf

    def plot_to_ctk(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        widget = canvas.get_tk_widget()
        return widget

    def on_close(self):
        # Destroy the window properly
        self.destroy()
        # Optional: also quit if you use .mainloop() externally
        self.quit()
