import tkinter as tk

from tkinter import messagebox


def getButton(window: tk.Tk, text: str, color, command, fg='white') -> tk.Button:
    return tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica bold', 20)
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