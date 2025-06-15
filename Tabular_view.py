import customtkinter as ctk
import tkinter as tk
from tkinter import font, ttk
from tkcalendar import DateEntry
import json
# github is annoying


class Table(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master)
        self.create_grid()

        # Transactor inside a frame
        self.transactor = TransactionEngine(self)
        self.transactor.grid(row=0, column=0, sticky="nsw", pady=10)

        # Label
        self.label = ctk.CTkLabel(self, text="Transaction Table", font=("Segoe UI", 24, "bold"))
        self.label.grid(row=1, column=0, sticky="n", pady=10)

        # Refresh Button
        self.transactions = None
        self.refresh = ctk.CTkButton(self, text="↻", font=("", 24, "bold"), command=self.refresh_table)
        self.refresh.grid(row=1, column=0, sticky="nw", pady=10, padx=10)

        # Table view frame
        self.table_frame = ctk.CTkFrame(self, fg_color="black")
        self.table_frame.grid(row=2, column=0, sticky='nsew', pady=10)

        # Table view variables
        self.columns = ("Date", "User", "Type", "Category","Amount", "Note")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=10)
        self.setup_table()

    def create_grid(self):
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=70)
        self.columnconfigure(0, weight=1)

    def setup_table(self):
        for column in self.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center", width=200)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("default")
        # enlarge row size and font
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=40,
                        fieldbackground="#2b2b2b",
                        font=("Segoe UI", 14))
        # style Header cells
        style.configure("Treeview.Heading",
                        background="#1054c2",  # <-- Header background
                        foreground="white",  # <-- Header text color
                        font=("Segoe UI", 14, "bold"))
        style.configure("Treeview.Heading", font=("Segoe UI", 16, "bold"))  # enlarge heading fonts
        style.map('Treeview', background=[('selected', '#1f6aa5')])

        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            self.transactions = file_data["Transactions"]

            for entry in self.transactions:
                row = [entry["date"], entry["user"], entry["type"], entry["category"], entry["amount"], entry["note"]]
                self.tree.insert("", tk.END, values=row)

        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            transactions = file_data["Transactions"]

            for entry in transactions:
                if entry in self.transactions:
                    print("no new entries")
                else:
                    row = [entry["date"], entry["user"], entry["type"], entry["category"], entry["amount"], entry["note"]]
                    self.transactions.append(entry)
                    self.tree.insert("", tk.END, values=row)


class TransactionEngine(ctk.CTkFrame):
    def __init__(self, master):

        super().__init__(master=master, fg_color="#1054c2", width=500)
        self.create_grid()
        self.parent = master

        # Add Transaction Button
        self.add_transaction = ctk.CTkButton(self, text="+", font=("", 25, "bold"), fg_color="#f51168", text_color="black",
                                             command=self.get_values)

        # Users Combo-Box
        self.user_values = ['You']
        self.users = ctk.CTkComboBox(master=self, values=self.user_values, height=40, width=200, justify="center",
                                     fg_color="#478af5", text_color="black")

        # Amount Entry-Box
        self.amount = ctk.CTkEntry(master=self, placeholder_text="$ ", height=40, width=110,
                                   text_color="black", fg_color="white")

        # Transaction type Combo-Box
        self.types = ["Income", "Expense"]
        self.type = ctk.CTkComboBox(master=self, values=self.types, height=40, width=200, justify="center",
                                    fg_color="#478af5", text_color="black")

        # Category Combo-Box
        self.categories = ["Food", "clothing", "entertainment", "bills", "repairs", "misc"]
        self.category = ctk.CTkComboBox(master=self, values=self.categories, height=40, width=200, justify="center"
                                        , fg_color="#478af5", text_color="black")

        # Calendar widget
        my_font = font.Font(family="Arial", size=12, weight="bold")
        self.date = DateEntry(self, date_pattern="dd-mm-yyyy", height=100, font=my_font, bg="orange")

        # Note widget
        self.note = ctk.CTkTextbox(self,fg_color="#478af5", height=100, width=160, text_color="black")

        self.grid_widgets()

    def grid_widgets(self):
        ctk.CTkLabel(self, text="Add Transaction : ", font=("", 25, "bold"), pady=10, padx=10, text_color="black").grid(row=0, column=1, sticky="nsew")
        self.add_transaction.grid(row=0, column=2, sticky="nsw", pady=10)

        self.users.set("Select user")
        self.users.grid(row=1, column=1, sticky="nw", padx=10, pady=10)

        ctk.CTkLabel(self, text="Enter Amount:", text_color="black", font=("", 12, "bold")).grid(row=1, column=2, pady=10, padx=10, sticky="nsw")
        self.amount.grid(row=1, column=2, pady=10, padx=10, sticky="nse")

        self.type.set("Transaction type")
        self.type.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

        self.category.set("Select category")
        self.category.grid(row=2, column=2, sticky="nw", padx=10, pady=10)

        ctk.CTkLabel(self, text="Date: ", text_color="black", font=("", 12, "bold")).grid(row=3, column=1, pady=10, padx=10, sticky="nsw")
        self.date.grid(row=3, column=1, sticky="nse", padx=10, pady=10, ipadx=10)

        ctk.CTkLabel(self, text="Note: ", text_color="black", font=("", 12, "bold")).grid(row=4, column=1, pady=10, padx=10, sticky="nsw")
        self.note.grid(row=4, column=1, sticky="nse", padx=10, pady=10)

    def create_grid(self):

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def get_values(self):

        # assign values to local variables
        user_value = self.users.get()
        amount = float(self.amount.get())
        type_value = self.type.get()
        category = self.category.get()
        date = str(self.date.get_date())
        note = self.note.get(1.0, ctk.END)

        # check for missing values
        if user_value in self.user_values and type_value in self.types and category in self.categories:
            if amount >= 0:
                with open("Transactions.json", "r+") as f:
                    file_data = json.load(f)

                    new_data = {
                        "date": date,
                        "user": user_value,
                        "type": type_value,
                        "category": category,
                        "amount": amount,
                        "note": note
                    }

                    file_data["Transactions"].append(new_data)

                    f.seek(0)

                    json.dump(file_data, f, indent=4)

                    row = [new_data["date"], new_data["user"], new_data["type"], new_data["category"], new_data["amount"],
                           new_data["note"]]

                    self.parent.transactions.append(new_data)
                    self.parent.tree.insert("", tk.END, values=row)
        else:
            print("please fill all the required fields")
