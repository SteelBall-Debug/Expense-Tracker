import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("600x400")

        # Frame for the table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Use a standard Treeview inside the CTkFrame
        self.setup_table()

    def setup_table(self):

        columns = ("Date", "Category", "Amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=10)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2b2b2b")
        style.map('Treeview', background=[('selected', '#1f6aa5')])

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Sample data
        expenses = [
            ("2025-06-09", "Food", 200),
            ("2025-06-08", "Transport", 50),
            ("2025-06-07", "Books", 300)
        ]

        for row in expenses:
            self.tree.insert("", tk.END, values=row)

        self.tree.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
