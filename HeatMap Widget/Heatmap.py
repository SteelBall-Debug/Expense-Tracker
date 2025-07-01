# Notes for later:
# [
#    1. Use pandas library, value_counts() function to get frequency of transactions occurred on dates
#    2. Use frequency data to create a cache file that stores dates along with transaction ID's and frequency of
#    Transactions.
#    3. Use said "cache" file to assign color values to the generated buttons
#    4. Write function to fetch transactions using ID's stored in Cache File
#    5. Hook Said function to buttons using lambda function [refer test.py file]
#    6. Don't forget to be hungry
# ]


import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self, title, size):

        # main-setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        self.heatmap = Heatmap(self, "date", None, None)
        self.heatmap.pack(pady=90)

        self.mainloop()


class Heatmap(ctk.CTkScrollableFrame):

    def __init__(self, master, start_date, freq_table,color_gradient=None):

        # main-setup
        super().__init__(master=master, fg_color="black", width=400, height=150, orientation="horizontal",
                         scrollbar_button_color="#1b1c1c")

        # Starting Date for Calendar
        self.start_date = start_date

        # Frequency Table { "Date" , "frequency", "meta-data"}
        self.freq_table = freq_table

        # Default colour gradient [Github style Green]
        if not color_gradient:
            self.color_gradient = ["#0c0d0d", "#7bc96f", "#239a3b", "#196127"]
        else:
            self.color_gradient = color_gradient

        self.create_buttons()

    def create_buttons(self):

        for week in range(52):
            for day in range(7):
                btn = ctk.CTkButton(self, border_color="white", width=20, height=20, fg_color="#0c0d0d", text="", corner_radius=4)
                btn.grid(row=day, column=week, pady=1, padx=1)


if __name__ == "__main__":
    App("Heatmap", (600, 400))
