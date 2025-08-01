import customtkinter as ctk
from tkinter import ttk
import json

CATEGORIES = None
USERS = None


def import_cache_data():
    with open("Cache.json", "r+") as f:
        file_data = json.load(f)
        global CATEGORIES
        CATEGORIES = file_data["categories"]
        global USERS
        USERS = file_data["users"]


import_cache_data()  # import user and category lists from Cache


class Settings(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master, fg_color="#151d28", bg_color="#151d28")

        self.parent = master

        self.create_grid()
        self.main_label()

        # buttons
        ctk.CTkLabel(self, text="Add new Category", font=(" ", 15)).grid(row=2, column=0, sticky="ns", pady=10)
        self.add_category_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f",)
        self.add_category_button = ctk.CTkButton(self, text="+", font=(" ", 20, "bold"), width=50, fg_color="#468232",
                                                 hover_color="#1f5f5b", command=self.add_category)

        self.current_categories = CATEGORIES

        ctk.CTkLabel(self, text="Add new User", font=(" ", 15)).grid(row=3, column=0, sticky="nsew", pady=10)
        self.add_user_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f")
        self.add_user_button = ctk.CTkButton(self, text="+", font=(" ", 20, "bold"), width=50, fg_color="#468232",
                                             hover_color="#1f5f5b", command=self.add_user)

        self.current_users = USERS

        self.cat_tree = ttk.Treeview(self, columns=["Categories"], show="headings", height=6)
        self.us_tree = ttk.Treeview(self, columns=["Users"], show="headings", height=4)

        self.category_tree()
        self.user_tree()

        delete_cat = ctk.CTkButton(self, text="delete category", text_color="white", fg_color="red", hover_color="orange",
                                   font=(" ", 15, "bold"), width=10, command=self.delete_category)
        delete_cat.grid(row=5, column=0, sticky="nsew", pady=5, padx=10)

        delete_user = ctk.CTkButton(self, text="   delete user   ", text_color="white", fg_color="red", hover_color="orange",
                                    font=(" ", 15, "bold"), width=6, command=self.delete_user)
        delete_user.grid(row=5, column=1, sticky="nsew", pady=5, padx=10)

        # grid widgets
        self.grid_buttons()

    def create_grid(self):
        self.rowconfigure(1, weight=25)
        self.rowconfigure(2, weight=25)
        self.rowconfigure(3, weight=25)

    def main_label(self):
        label = ctk.CTkLabel(master=self, text="Settings", font=("", 30, "bold"))
        label.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

    def apply_updates(self):
        self.parent.apply_updates()

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

        self.cat_tree.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)

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

        self.us_tree.grid(row=4, column=1, sticky="nsew", pady=10, padx=10)

    def delete_category(self):
        selected_entry = self.cat_tree.selection()

        if selected_entry:
            for item_id in selected_entry:
                cat = str(self.cat_tree.item(item_id)['values'][0])

                with open("Cache.json", "r+") as file:
                    data = json.load(file)
                    for category in data["categories"]:
                        if category == cat:
                            try:
                                data["categories"].remove(cat)
                                file.seek(0)
                                json.dump(data, file, indent=4)
                                file.truncate()
                            except Exception as e:
                                print(f"Error while deleting file {e}")

                self.cat_tree.delete(item_id)

            import_cache_data()
            self.apply_updates()

    def delete_user(self):
        selected_entry = self.us_tree.selection()

        if selected_entry:
            for item_id in selected_entry:

                us = str(self.us_tree.item(item_id)['values'][0])

                with open("Cache.json", "r+") as file:
                    data = json.load(file)
                    for user in data["users"]:
                        if user == us:
                            try:
                                data["users"].remove(us)
                                file.seek(0)
                                json.dump(data, file, indent=4)
                                file.truncate()
                            except Exception as e:
                                print(f"Error while deleting file {e}")

                self.us_tree.delete(item_id)
            import_cache_data()
            self.apply_updates()

    def add_category(self):
        new_category = str(self.add_category_entry.get()).lower()

        with open("Cache.json", "r+") as file:
            data = json.load(file)

            if new_category in data["categories"]:
                print("category already exists")
            else:
                data["categories"].append(new_category)
                file.seek(0)
                json.dump(data, file, indent=4)

                self.cat_tree.insert("", ctk.END, values=[new_category])
            import_cache_data()
            self.apply_updates()

    def add_user(self):
        new_user = str(self.add_user_entry.get()).lower()

        with open("Cache.json", "r+") as file:
            data = json.load(file)

            if new_user in data["users"]:
                print("user already exists")
            else:
                data["users"].append(new_user)
                file.seek(0)
                json.dump(data, file, indent=4)

                self.us_tree.insert("", ctk.END, values=[new_user])
            import_cache_data()
            self.apply_updates()
