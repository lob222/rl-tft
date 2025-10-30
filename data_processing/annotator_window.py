import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
CHAMPION_NAMES_FILE = "../game_info/champions.txt"
EMPTY_IDX = -1
INVALID_IDX = -2

BENCH_SPOTS = 9
BOARD_ROWS = 8
BOARD_COLS = 7

LOGGER = True

root = tk.Tk()
root.title("Annotator")

champion_dict = dict()

try:
    with open(CHAMPION_NAMES_FILE, 'r') as file:
        champions = file.readlines()
        for c in range(len(champions)):
            champion_dict[champions[c].strip()] = c
except FileNotFoundError:
    print(f"Error: File '{CHAMPION_NAMES_FILE}' not found.")

    


class AnnotatorGUI(tk.Tk):
    def __init__(self, champion_dict):
        super().__init__()
        self.title("Annotator")
        self.geometry("1200x800")
        self.champion_dict = champion_dict

        self.init_board()
        self.fill_board()
        self.create_buttons()


    def init_board(self):
        self.boxes = [[tk.StringVar() for _ in range(BENCH_SPOTS)]] + [[tk.StringVar() for _i in range(BOARD_COLS)] for _j in range(BOARD_ROWS)] + [[tk.StringVar() for _ in range(BENCH_SPOTS)]]
        
        self.sliders = [[tk.IntVar() for _ in range(BENCH_SPOTS)]] + [[tk.IntVar() for _i in range(BOARD_COLS)] for _j in range(BOARD_ROWS)] + [[tk.IntVar() for _ in range(BENCH_SPOTS)]]

    def fill_board(self):

        row_idx = 0

        self.create_row(BENCH_SPOTS, row_idx)
        row_idx += 1
        self.create_line()
        for _ in range(2):
            for _ in range(BOARD_ROWS // 2):
                self.create_row(BOARD_COLS, row_idx)
                row_idx += 1
            self.create_line()
        self.create_row(BENCH_SPOTS, row_idx)

        self.create_line()


    def create_row(self, count, row_idx):
        frame = tk.Frame(self)

        frame.pack(pady=2)

        for i in range(count):
            cb = AutocompleteCombobox(frame, completevalues=list(champion_dict.keys()), width=10, textvariable=self.boxes[row_idx][i])
            cb.grid(row=0, column=i, padx=1, pady=1)

            # ensure variable is updated when a value is selected
            cb.bind("<<ComboboxSelected>>", lambda e, var=self.boxes[row_idx][i], w=cb: var.set(w.get()))
            cb.bind("<Return>", lambda e, var=self.boxes[row_idx][i], w=cb: var.set(w.get()))


            sl = tk.Scale(frame, from_=0, to=2, orient='horizontal', 
                            showvalue=False, resolution=1, length=90, variable=self.sliders[row_idx][i])
            sl.grid(row=1, column=i, padx=1, pady=(0,1))


    def create_line(self):
        line_canvas = tk.Canvas(self, height=5, bg="black", highlightthickness=0)
        line_canvas.pack(fill="x", pady=10)
        line_canvas.create_line(0, 2, self.winfo_width(), 2, fill="black", width=5)


    def create_buttons(self):
        # Complete or Reset
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)  # bigger vertical gap

        btn_font = ("Helvetica", 14)  # slightly larger text

        reset_btn = tk.Button(button_frame, text="Reset", font=btn_font, width=12)
        reset_btn.pack(side="left", padx=20)  # larger horizontal gap
        complete_btn = tk.Button(button_frame, text="Complete", font=btn_font, width=12, command=self.get_board)
        complete_btn.pack(side="left", padx=20)


    def get_board(self):

        board_log = ''

        for row_idx in range(2 + BOARD_ROWS):
            
            board_log_row = ''

            boxes = self.boxes[row_idx]
            sliders = self.sliders[row_idx]
            for b in boxes:
                
                if len(b.get()) == 0:
                    board_log_row = board_log_row + "None "
                else:
                    board_log_row = board_log_row + b.get() + " "
            
            board_log += board_log_row + '\n'

        if LOGGER: print(board_log)


if __name__ == "__main__":
    app = AnnotatorGUI(champion_dict)
    app.mainloop()
