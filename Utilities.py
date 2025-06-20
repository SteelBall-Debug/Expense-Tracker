import customtkinter as ctk
import json


class Filterer(ctk.CTkFrame):

    def __init__(self, master, apply_callback=None, reset_callback=None):
        super().__init__(master=master, width=200, height=250, fg_color="#1f1f1f")

        self.apply_callback = apply_callback
        self.reset_callback = reset_callback

        self.title = ctk.CTkLabel(self, text="Filter Transactions", font=("", 14, "bold"))
        self.title.pack(pady=(10, 15), padx=20)

        self.date_entry = ctk.CTkEntry(self, placeholder_text="MM/DD/YYYY", width=180)
        self.date_entry.pack(pady=5)

        self.category_box = ctk.CTkComboBox(self, values=["Food", "clothing", "entertainment", "bills", "repairs", "misc"], width=180)
        self.category_box.set("Select Category")
        self.category_box.pack(pady=5)

        self.keyword_entry = ctk.CTkEntry(self, placeholder_text="Keyword", width=180)
        self.keyword_entry.pack(pady=5)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(10, 5))

        self.reset_btn = ctk.CTkButton(self.button_frame, text="Reset", width=80, command=self.on_reset)
        self.apply_btn = ctk.CTkButton(self.button_frame, text="Apply", width=80, command=self.on_apply)
        self.reset_btn.grid(row=0, column=0, padx=5)
        self.apply_btn.grid(row=0, column=1, padx=5)

        self.pack_propagate(False)

    def on_apply(self):
        if self.apply_callback:
            filters = {
                "date": self.date_entry.get(),
                "category": self.category_box.get(),
                "keyword": self.keyword_entry.get()
            }
            self.apply_callback(filters)

    def on_reset(self):
        self.date_entry.delete(0, 'end')
        self.category_box.set("Select Category")
        self.keyword_entry.delete(0, 'end')
        if self.reset_callback:
            self.reset_callback()

