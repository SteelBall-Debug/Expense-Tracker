import customtkinter as ctk
import tkinter as tk
from tkinter import font, ttk
from tkcalendar import DateEntry
import json
from Scripts.Utilities import Filterer
from Scripts.Settings import import_cache_data
import os

transaction_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Transactions.json')


class Table(ctk.CTkScrollableFrame):

    def __init__(self, master, dashboard):

        super().__init__(master=master, fg_color="#090a14", bg_color="#090a14")
        self.parent = master
        self.dashboard = dashboard
        self.create_grid()

        # import lists
        categories, users = import_cache_data()

        # Transactor inside a frame
        self.transactor = TransactionEngine(self.parent, self, categories, users)
        # self.transactor.grid(row=0, column=0, sticky="nsw", pady=10)

        # Label
        self.label = ctk.CTkLabel(self, text="      Transaction Table", font=("Segoe UI", 24, "bold"))
        self.label.grid(row=1, column=0, sticky="n", pady=10)

        # Refresh Button
        self.transactions = None
        self.refresh = ctk.CTkButton(self, text="↻", font=("", 24, "bold"), width=100, fg_color="#468232", hover_color="#1f5f5b", command=self.refresh_table)
        self.refresh.grid(row=1, column=0, sticky="nw", pady=10, padx=10)

        # Filtration system
        self.current_filter = ()
        self.toggle = False
        self.toggle2 = False
        self.filter_butt = ctk.CTkButton(self, text="☰", text_color="white", width=60, height=35, fg_color="#468232", hover_color="#1f5f5b", command=self.show_filter_menu)
        self.filter_menu = Filterer(self.parent, self)
        self.filter_butt.grid(row=1, column=0, sticky="nw", pady=10, padx=120)

        # Add transaction button
        self.add = ctk.CTkButton(self, text="+", width=60, height=35, font=("", 16, "bold"), fg_color="#468232", hover_color="#1f5f5b", command=self.show_transaction_menu)
        self.add.grid(row=1, column=0, sticky="nw", pady=10, padx=190)

        # Table view frame
        self.table_frame = ctk.CTkFrame(self, height=100)
        self.table_frame.grid(row=2, column=0, sticky='nsew', pady=10)

        # Table view variables
        self.columns = ("Sr.no.", "Date", "User", "Type", "Category", "Amount", "Note")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=40)

        self.delete_selected = ctk.CTkButton(self, text="Delete Selected",font=("", 16, "bold"), height=35, text_color="white", fg_color="#f51168",hover_color="#f51150", command=self.delete_entry)
        self.delete_selected.grid(row=1, column=0, sticky="ne", pady=10, padx=10)

        self.entry_id = 0
        self.setup_table()

    def create_grid(self):
        # self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=10)
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
                        background="#151d28",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#151d28",
                        font=("Segoe UI", 16))
        # style Header cells
        style.configure("Treeview.Heading",
                        background="#25562e",  # <-- Header background
                        foreground="white",  # <-- Header text color
                        font=("Segoe UI", 14, "bold"))
        style.configure("Treeview.Heading", font=("Segoe UI", 20, "bold"))  # enlarge heading fonts
        style.map('Treeview', background=[('selected', '#1f6aa5')])

        with open(transaction_path, "r+") as f:
            file_data = json.load(f)
            self.transactions = file_data["Transactions"]
            self.entry_id = len(self.transactions)
            for entry in self.transactions:
                row = [entry["id"], entry["date"], entry["user"], entry["type"], entry["category"], entry["amount"], entry["note"]]
                self.tree.insert("", tk.END, values=row)

        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        self.clear_treeview()
        self.setup_table()

    def delete_entry(self):
        selected_entry = self.tree.selection()
        entry_values = self.tree.item(selected_entry[0])['values']
        selected_id = entry_values[0]

        if selected_entry:

            self.tree.delete(selected_entry[0])

            with open(transaction_path, "r+") as f:
                file_data = json.load(f)
                for entry in file_data["Transactions"]:
                    if entry["id"] == selected_id:
                        try:
                            file_data["Transactions"].remove(entry)
                            f.seek(0)
                            json.dump(file_data, f, indent=4)
                            f.truncate()
                        except Exception as e:
                            print(f"Error while deleting file {e}")

    def show_filter_menu(self):
        if self.toggle:
            self.filter_menu.grid_forget()
            self.toggle = False
        else:
            self.filter_menu.grid(row=0, column=1)
            self.filter_menu.lift()
            self.toggle = True

    def show_transaction_menu(self):
        if self.toggle2:
            self.transactor.grid_forget()
            self.toggle2 = False
        else:
            self.transactor.grid(row=0, column=1)
            self.transactor.lift()
            self.toggle2 = True

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)


class TransactionEngine(ctk.CTkFrame):
    def __init__(self, master, table, cat, users):

        super().__init__(master=master, fg_color="#1f1f1f", width=470, height=400)
        self.create_grid()
        self.parent = master
        self.table = table

        # Add Transaction Button
        self.add_transaction = ctk.CTkButton(self, text="+", font=("", 25, "bold"),  fg_color="#468232", hover_color="#1f5f5b",
                                             command=self.get_values)

        # exit button
        self.exit_button = ctk.CTkButton(self, text="x", fg_color="red", bg_color="red", text_color="white",
                                    hover_color="white", command=self.table.show_transaction_menu, width=3, font=("", 18, "bold"))

        # Users Combo-Box
        self.user_values = users
        self.users = ctk.CTkComboBox(master=self, values=self.user_values, height=40, width=200, justify="center",
                                     fg_color="#151d28")

        # Amount Entry-Box
        self.amount = ctk.CTkEntry(master=self, placeholder_text="$ ", height=40, width=110,
                                    fg_color="#10141f")

        # Transaction type Combo-Box
        self.types = ["Income", "Expense"]
        self.type = ctk.CTkComboBox(master=self, values=self.types, height=40, width=200, justify="center",
                                    fg_color="#151d28")

        # Category Combo-Box
        self.categories = cat
        self.category = ctk.CTkComboBox(master=self, values=self.categories, height=40, width=200, justify="center"
                                        , fg_color="#151d28")

        # Calendar widget
        my_font = font.Font(family="Arial", size=12, weight="bold")
        self.date = DateEntry(self, date_pattern="dd-mm-yyyy", height=100, font=my_font, bg="#151d28")

        # Note widget
        self.note = ctk.CTkTextbox(self, fg_color="#10141f", height=100, width=160)

        self.grid_propagate(False)
        self.grid_widgets()

    def grid_widgets(self):
        ctk.CTkLabel(self, text="Add Transaction : ", font=("", 25, "bold"), pady=10, padx=10).grid(row=0, column=1, sticky="nsew")
        self.add_transaction.grid(row=0, column=2, sticky="nsw", pady=10)

        self.exit_button.grid(row=0, column=2, sticky="ne", pady=10)

        self.users.set("Select user")
        self.users.grid(row=1, column=1, sticky="nw", padx=10, pady=10)

        ctk.CTkLabel(self, text="Enter Amount:", font=("", 12, "bold")).grid(row=1, column=2, pady=10, padx=10, sticky="nsw")
        self.amount.grid(row=1, column=2, pady=10, padx=10, sticky="nse")

        self.type.set("Transaction type")
        self.type.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

        self.category.set("Select category")
        self.category.grid(row=2, column=2, sticky="nw", padx=10, pady=10)

        ctk.CTkLabel(self, text="Date: ", font=("", 12, "bold")).grid(row=3, column=1, pady=10, padx=10, sticky="nsw")
        self.date.grid(row=3, column=1, sticky="nse", padx=10, pady=10, ipadx=10)

        ctk.CTkLabel(self, text="Note: ", font=("", 12, "bold")).grid(row=4, column=1, pady=10, padx=10, sticky="nsw")
        self.note.grid(row=4, column=1, sticky="nse", padx=10, pady=10)

    def create_grid(self):

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def get_values(self):

        # assign values to local variables
        num = self.table.entry_id + 1
        user_value = self.users.get()
        amount = float(self.amount.get())
        type_value = self.type.get()
        category = self.category.get()
        date = str(self.date.get_date())
        note = self.note.get(1.0, ctk.END)

        # check for missing values
        if user_value in self.user_values and type_value in self.types and category in self.categories:
            if amount >= 0:
                with open(transaction_path, "r+") as f:
                    file_data = json.load(f)

                    new_data = {
                        "id": num,
                        "date": date,
                        "user": user_value.lower(),
                        "type": type_value,
                        "category": category.lower(),
                        "amount": amount,
                        "note": note.lower()
                    }

                    file_data["Transactions"].append(new_data)
                    f.seek(0)

                    json.dump(file_data, f, indent=4)

                    row = [new_data["id"], new_data["date"], new_data["user"], new_data["type"], new_data["category"],
                           new_data["amount"], new_data["note"]]

                    self.parent.transactions.append(new_data)
                    self.parent.tree.insert("", tk.END, values=row)

                    # update heatmap
                    self.parent.dashboard.update_heatmap()

                    # update entry id
                    self.parent.entry_id += 1
        else:
            print("please fill all the required fields")