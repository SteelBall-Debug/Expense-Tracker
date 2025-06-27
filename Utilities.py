import customtkinter as ctk
from tkinter import font
from tkcalendar import DateEntry
import json


class Filterer(ctk.CTkFrame):
    def __init__(self, master, table, reset_callback=None):
        super().__init__(master=master, width=200, height=300, fg_color="#1f1f1f")

        self.table = table

        self.reset_callback = reset_callback
        self.grid_propagate(False)  # Keeps the frame size fixed

        # Configure 1 column layout
        self.columnconfigure(0, weight=1)

        # Title
        self.title = ctk.CTkLabel(self, text="Filter Transactions", font=("", 14, "bold"))
        self.title.grid(row=0, column=0, pady=(10, 15), padx=20, sticky="ew")

        # Date Entry
        my_font = font.Font(family="Arial", size=12, weight="bold")
        self.date_entry = DateEntry(self, date_pattern="dd-mm-yyyy", font=my_font, width=18, height=9)
        self.date_entry.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Category
        self.category_box = ctk.CTkComboBox(self, values=["Food", "Clothing", "Entertainment", "Bills", "Repairs", "Misc"], width=180)
        self.category_box.set("Select Category")
        self.category_box.grid(row=2, column=0, pady=5, padx=20, sticky="ew")

        # Users
        self.user_list = self.table.transactor.user_values
        self.users = ctk.CTkComboBox(self, values=self.user_list, width=180)
        self.users.set("Select User")
        self.users.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

        # Keyword
        self.keyword_entry = ctk.CTkEntry(self, placeholder_text="Keyword", width=180)
        self.keyword_entry.grid(row=4, column=0, pady=5, padx=20, sticky="ew")

        # Button Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=5, column=0, pady=(10, 5), padx=20, sticky="ew")

        self.reset_btn = ctk.CTkButton(self.button_frame, text="Reset", width=80, command=self.on_reset)
        self.apply_btn = ctk.CTkButton(self.button_frame, text="Apply", width=80, command=self.apply_filters)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.reset_btn.grid(row=0, column=0, padx=5)
        self.apply_btn.grid(row=0, column=1, padx=5)

        self.filter_list = []

    def on_reset(self):
        self.category_box.set("Select Category")
        self.keyword_entry.delete(0, 'end')
        if self.reset_callback:
            self.reset_callback()

    def apply_filters(self):
        with open("Transactions.json", "r") as f:
            data = json.load(f)["Transactions"]

        # date = self.date_entry.get().strip()
        category = self.category_box.get().strip().lower()
        user = self.users.get().strip().lower()
        keyword = self.keyword_entry.get().strip().lower()

        filtered = []
        for entry in data:
            if category != "select category" and category != entry["category"].lower():
                continue
            if keyword and keyword not in entry["note"].lower():
                continue
            if user and user not in entry["user"].lower():
                continue
            filtered.append(entry)

        # Clear and repopulate
        self.table.clear_treeview()
        for entry in filtered:
            self.table.tree.insert("", "end", values=([entry["id"], entry["date"], entry["user"], entry["type"], entry["category"],
                                                       entry["amount"], entry["note"]]))
