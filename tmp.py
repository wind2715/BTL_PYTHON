import tkinter as tk

class HourlySchedule(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_hourly_table()

    def create_hourly_table(self):
        self.cell_width = 50
        self.cell_height = 30

        for row in range(24):
            for col in range(6):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = (col + 1) * self.cell_width
                y2 = (row + 1) * self.cell_height

                self.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags=f"{row * 6 + col}")

    def highlight_cells(self, a, b, c, d):
        start_cell = 6 * a + b // 10
        end_cell = 6 * c + d // 10

        for cell_num in range(start_cell, end_cell + 1):
            self.itemconfig(f"{cell_num}", fill="red")

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Hourly Schedule Table")

        self.hourly_schedule = HourlySchedule(master, width=300, height=720)
        self.hourly_schedule.pack()

        self.a_entry = tk.Entry(master, width=5)
        self.b_entry = tk.Entry(master, width=5)
        self.c_entry = tk.Entry(master, width=5)
        self.d_entry = tk.Entry(master, width=5)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_values)

        self.a_entry.pack()
        self.b_entry.pack()
        self.c_entry.pack()
        self.d_entry.pack()
        self.submit_button.pack()

    def submit_values(self):
        try:
            a = int(self.a_entry.get())
            b = int(self.b_entry.get())
            c = int(self.c_entry.get())
            d = int(self.d_entry.get())

            self.hourly_schedule.highlight_cells(a, b, c, d)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid integer values for a, b, c, and d.")

root = tk.Tk()
app = App(root)
root.mainloop()
