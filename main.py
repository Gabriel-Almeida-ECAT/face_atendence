import tkinter as tk

import PIL.Image
import cv2
import numpy as np
import utils

from PIL import Image, ImageTk
from gabriels_openCvPyLib import openCvLib


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = utils.getButton(self.main_window, 'login', 'red', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_usr_button_main_window = utils.getButton(self.main_window, 'Register', 'gray', self.registerNewUsr, fg='black')
        self.register_new_usr_button_main_window.place(x=750, y=400)

        self.webcan_label: tk.Label = utils.getImgLabel(self.main_window)
        self.webcan_label.place(x=10, y=0, width=700, height=500)

        self.addWebcan(self.webcan_label)


    def addWebcan(self, label: tk.Label) -> None:
        if 'cap' not in self.__dict__: #test if the variable is already created
            self.cap: cv2.VideoCapture = cv2.VideoCapture(0)

        self._label: tk.Label = label
        self.processWebcan()

    def processWebcan(self) -> None:
        ret: bool
        frame: np.uint8
        ret, frame = self.cap.read()

        self.most_recent_cap: np.uint8 = frame

        # img_ = cv2.cvtColor(self.most_recent_capture, cv2.COLOR_BGR2RGB)
        img_: np.uint8 = openCvLib.bgr2rgb(self.most_recent_cap)

        self.most_recent_cap_pil: PIL.Image.Image = Image.fromarray(img_)

        img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=self.most_recent_cap_pil)

        self._label.imgtk: ImageTk.PhotoImage = img_tk
        self._label.configure(image=img_tk)

        self._label.after(20, self.processWebcan)


    def login(self) -> None:
        pass


    def registerNewUsr(self) -> None:
        pass

    def start(self) -> None:
        self.main_window.mainloop()

def main() -> None:
    app: App = App()
    app.start()


if __name__ == '__main__':
    main()


