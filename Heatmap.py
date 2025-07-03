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
import calendar
import json
import pandas as pd
from datetime import date, datetime, timedelta


class App(ctk.CTk):
    def __init__(self, title, size):

        # main-setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        current_year = datetime.now().year
        start_date = date(current_year, 1, 1)

        with open("Transactions.json", "r+") as f:
            file_data = json.load(f)
            data = file_data["Transactions"]
            df = pd.DataFrame(data)
            frequency_table = df[["date"]].value_counts()

        self.heatmap = Heatmap(self, start_date, frequency_table, None)
        self.heatmap.pack(pady=90)

        self.mainloop()

# orientation="horizontal",
#                          scrollbar_button_color="#1b1c1c"


class Heatmap(ctk.CTkFrame):

    def __init__(self, master, start_date, freq_table, color_gradient=None):

        # main-setup
        super().__init__(master=master, fg_color="black", width=600, height=250)

        # Starting Date for Calendar
        self.start_date = start_date

        # Frequency Table { "Date" , "frequency", "meta-data"}
        self.freq_table = freq_table

        # stores last clicked value
        self.last_clicked = ""

        # Default colour gradient [Github style Green]
        if not color_gradient:
            self.color_gradient = ["#0c0d0d", "#7bc96f", "#239a3b", "#196127"]
        else:
            self.color_gradient = color_gradient

        self.add_month_labels()
        self.create_buttons()
        self.add_color_index()

    def add_month_labels(self):
        month_labels = {}

        for m in range(1, 13):
            first_day = date(2025, m, 1)
            delta = (first_day - self.start_date).days
            week_col = delta // 7
            month_labels[week_col] = calendar.month_abbr[m]  # e.g., Jan, Feb, etc.

        # Add labels
        for col, month in month_labels.items():
            label = ctk.CTkLabel(self, text=month, font=("", 12, "bold"))
            label.grid(row=0, column=col + 1, pady=2)

    def create_buttons(self):

        for week in range(52):
            for day in range(1, 8):
                grid_date = (self.start_date + timedelta(days=week * 7 + day)).strftime("%Y-%m-%d")

                # Get count if exists, else 0
                count = self.freq_table.get(grid_date, 0)

                # Clamp count to max 3
                value = min(count, 4)

                index = min(3, max(0, int(value)))
                color = self.color_gradient[index]

                btn = ctk.CTkButton(
                    self,
                    width=18,
                    height=18,
                    text="",
                    fg_color=color,
                    corner_radius=6,
                    border_width=0,
                    command=lambda d=grid_date, v=value: self.handle_click(d, v)
                )

                btn.grid(row=day, column=week, padx=1, pady=1)

    def handle_click(self, date, value):
        print(f"Clicked on {date} with Transactions: {value}")
        result = f"Clicked on {date} with Transactions: {value}"
        self.last_clicked = result
        return result

    def add_color_index(self):
        less = ctk.CTkLabel(self, text="Less", font=("", 10, "bold"))
        less.grid(row=8, column=45)
        col = 46
        for color in self.color_gradient:
            f = ctk.CTkFrame(self, width=16, height=16, fg_color=color)
            f.grid(row=8, column=col, padx=1, pady=1)
            col += 1
        more = ctk.CTkLabel(self, text="More", font=("", 10, "bold"))
        more.grid(row=8, column=50)


if __name__ == "__main__":
    App("Heatmap", (1300, 400))
