import customtkinter as ctk


class Table(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master=master)
        self.create_grid()

        self.transactor = TransactionEngine(self)
        self.transactor.grid(row=0, column=0, sticky="nsew")

    def create_grid(self):
        self.rowconfigure(0, weight=25)
        self.rowconfigure(1, weight=50)
        self.columnconfigure(0, weight=1)


class TransactionEngine(ctk.CTkFrame):
    def __init__(self, master,):

        super().__init__(master=master, fg_color="#FF6500")

        # Users Combo-Box
        self.user_values = ['You']
        self.users = ctk.CTkComboBox(master=self, values=self.user_values, height=40, width=200, justify="center",
                                     fg_color="#FFBD73", text_color="black")

        # Amount Entry-Box
        self.amount = ctk.CTkEntry(master=self, placeholder_text="$ ", height=40, fg_color="#FFBD73",
                                   text_color="black")

        # Transaction type Combo-Box
        self.type = ctk.CTkComboBox(master=self, values=["Income", "Expense"], height=40, width=200, justify="center",
                                    fg_color="#FFBD73", text_color="black")

        # Category Combo-Box
        self.categories = ["Food", "clothing", "entertainment", "bills", "repairs", "misc"]
        self.category = ctk.CTkComboBox(master=self, values=self.categories, height=40, width=200, justify="center"
                                        , fg_color="#FFBD73", text_color="black")

        self.grid_widgets()

    def grid_widgets(self):
        self.users.set("select user")
        self.users.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

        ctk.CTkLabel(self, text="Enter Amount:", text_color="black", font=("", 12, "bold")).grid(row=0, column=2,
                                                                                                 padx=10, pady=10)
        self.amount.grid(row=0, column=3, padx=10, pady=10)

        self.type.set("Transaction type")
        self.type.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

        self.category.set("select category")
        self.category.grid(row=2, column=2, sticky="nw", padx=10, pady=10)


