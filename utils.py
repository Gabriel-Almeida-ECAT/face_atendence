import pickle
import PIL
import os
import face_recognition
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


def recognize(img: PIL.Image, db_path: str) -> str:
    face_scan_result: list[bytes] = face_recognition.face_encodings(img)
    if len(face_scan_result) == 0:
        return 'no_person_found'
    else:
        face_scan_result = face_scan_result[0]

    db_imgs_list: list[str] = sorted(os.listdir(db_path))

    match: bool = False
    ind: int = 0
    while (not match) and (ind < len(db_imgs_list)):
        img_path: str = os.path.join(db_path, db_imgs_list[ind])

        file: file = open(img_path, 'rb')
        test_img: bytes = pickle.load(file)

        match: bool = face_recognition.compare_faces([test_img], face_scan_result)[0]
        ind += 1

    if match:
        return db_imgs_list[ind]
    else:
        return 'person_not_registered'


def main() -> None:
    pass


if __name__ == '__main__':
    main()