import customtkinter as ctk
from tkinter import ttk


class Settings(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master, fg_color="#151d28", bg_color="#151d28")

        self.create_grid()
        self.main_label()

        # buttons
        ctk.CTkLabel(self, text="Add new Category", font=(" ", 15)).grid(row=2, column=0, sticky="ns", pady=10)
        self.add_category_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f",)
        self.add_category_button = ctk.CTkButton(self, text="+", font=(" ", 15, "bold"), width=50, fg_color="#468232", hover_color="#1f5f5b")

        self.current_categories = ["food", "clothing", "entertainment", "bills", "repairs", "misc"]

        ctk.CTkLabel(self, text="Add new User", font=(" ", 15)).grid(row=3, column=0, sticky="nsew", pady=10)
        self.add_user_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f")
        self.add_user_button = ctk.CTkButton(self, text="+", font=(" ", 15, "bold"), width=50, fg_color="#468232", hover_color="#1f5f5b")

        self.current_users = ['You', "Jane", "John"]

        self.cat_tree = ttk.Treeview(self, columns=["Categories"], show="headings", height=6)
        self.us_tree = ttk.Treeview(self, columns=["Users"], show="headings", height=4)

        self.category_tree()
        self.user_tree()

        self.delete_button = ctk.CTkButton(self, text="     🗑️", font=(" ", 12), width=50,
                                           fg_color="#f51168", hover_color="#f51150", height=1)
        self.delete_button.grid(row=4, column=2, pady=10, padx=10, sticky="new")

        # grid widgets
        self.grid_buttons()

    def create_grid(self):
        self.rowconfigure(1, weight=25)
        self.rowconfigure(2, weight=25)
        self.rowconfigure(3, weight=25)

    def main_label(self):
        label = ctk.CTkLabel(master=self, text="Settings", font=("", 30, "bold"))
        label.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

    def grid_buttons(self):
        self.add_category_entry.grid(row=2, column=1, sticky="nsew", pady=10)
        self.add_category_button.grid(row=2, column=2, pady=10, padx=5, sticky="nsew")

        self.add_user_entry.grid(row=3, column=1, sticky="nsew", pady=10)
        self.add_user_button.grid(row=3, column=2, pady=10, padx=5, sticky="nsew")

    def category_tree(self):
        self.cat_tree.heading("Categories", text="Categories")
        self.cat_tree.column("Categories", anchor="center", width=200)

        for row in self.current_categories:
            self.cat_tree.insert("", ctk.END, values=[row])

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

        self.cat_tree.grid(row=4, column=0, sticky="nsew", pady=10)

    def user_tree(self):
        self.us_tree.heading("Users", text="Users")
        self.us_tree.column("Users", anchor="center", width=200)

        for row in self.current_users:
            self.us_tree.insert("", ctk.END, values=[row])

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

        self.us_tree.grid(row=4, column=1, sticky="nsew", pady=10, padx=20)
