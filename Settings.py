import customtkinter as ctk


class Settings(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master, fg_color="#151d28", bg_color="#151d28")

        self.create_grid()
        self.main_label()

        # buttons
        ctk.CTkLabel(self, text="Appearance Mode", font=(" ", 15)).grid(row=1, column=0, sticky="ns", pady=10)
        self.appearance = ctk.CTkSegmentedButton(self, values=["light", "dark"], font=(" ", 15, "bold"), height=50, width=400,
                                                 unselected_color="#25562e", fg_color="#151d28", selected_color="#75a743")
        self.appearance.set("dark")

        ctk.CTkLabel(self, text="Add new Category", font=(" ", 15)).grid(row=2, column=0, sticky="ns", pady=10)
        self.add_category_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f",)
        self.add_category_button = ctk.CTkButton(self, text="+", font=(" ", 15, "bold"), width=50, fg_color="#468232", hover_color="#1f5f5b")

        self.current_categories = ["food", "clothing", "entertainment", "bills", "repairs", "misc"]
        self.display_current_categories = ctk.CTkSegmentedButton(self, values=self.current_categories, font=(" ", 15, "bold"), fg_color="#151d28",
                                                                 unselected_color="#25562e", selected_color="#75a743", dynamic_resizing=True)

        ctk.CTkLabel(self, text="Add new User", font=(" ", 15)).grid(row=3, column=0, sticky="nsew", pady=10)
        self.add_user_entry = ctk.CTkEntry(self, height=50, fg_color="#10141f")
        self.add_user_button = ctk.CTkButton(self, text="+", font=(" ", 15, "bold"), width=50, fg_color="#468232", hover_color="#1f5f5b")

        self.current_users = ['You', "Jane", "John"]
        self.display_current_users = ctk.CTkSegmentedButton(self, values=self.current_users, font=(" ", 14, "bold"), fg_color="#151d28",
                                                            unselected_color="#25562e", selected_color="#75a743")

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
        self.appearance.grid(row=1, column=1, sticky="nsew", pady=10)
        self.add_category_entry.grid(row=2, column=1, sticky="nsew", pady=10)
        self.add_category_button.grid(row=2, column=2, pady=10, padx=5, sticky="nsew")
        self.display_current_categories.grid(row=2, column=3, sticky="nsew", pady=10, padx=5)
        self.add_user_entry.grid(row=3, column=1, sticky="nsew", pady=10)
        self.add_user_button.grid(row=3, column=2, pady=10, padx=5, sticky="nsew")
        self.display_current_users.grid(row=3, column=3, sticky="nsw", pady=10, padx=5)
