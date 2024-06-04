import tkinter as tk

from tkinter import messagebox


class grid_ui:
    def __init__(self, grid_rows: int, grid_cols: int, win_width: int, win_height: int) -> None:
        self.win_width: int = win_width
        self.win_height: int = win_height
        self.grid_rows: int = grid_rows
        self.grid_cols: int = grid_cols

        self.num_pixels_horizontal_cel_unit: int = int(win_width / grid_cols)
        self.num_pixels_vertical_cel_unit: int = int(win_height / grid_rows)


    def getSizeHoriCel(self, num_cels: int = 1):
        return self.num_pixels_horizontal_cel_unit * num_cels


    def getSizeVertiCel(self, num_cels: int = 1):
        return self.num_pixels_vertical_cel_unit * num_cels


    def getXpixelOfCel(self, col_num: int):
        return self.getSizeHoriCel() * col_num


    def getYpixelOfCel(self, row_num: int):
        return self.getSizeVertiCel() * row_num



def getButton(window: tk.Tk, text: str, color, command, fg='white') -> tk.Button:
    return tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        font=('Helvetica bold', 18)
    )


def getImgLabel(window: tk.Tk) -> tk.Label:
    label: tk.Label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def getTxtLabel(window: tk.Tk, text: str) -> tk.Label:
    label: tk.Label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def getEntryText(window) -> tk.Text:
    input_txt: tk.Text = tk.Text(window, height=2, width=15, font=("Arial", 32))
    return input_txt


def msgBox(title, description) -> None:
    messagebox.showinfo(title, description)


def main() -> None:
    pass


if __name__ == '__main__':
    main()