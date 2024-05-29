import os
import datetime
import cv2
import numpy as np
import tkinter as tk
import tkinter_utils as tk_utils
import image_utils as img_utils

from PIL import Image, ImageTk
from gabriels_openCvPyLib import openCvLib
from anti_spoofing.test import test as test_spoofing

# adjust image window to camera resolution

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        main_win_width = 1240
        win_height = 768
        self.main_window.geometry(f"{main_win_width}x{win_height}")

        self.btn_login_main_win = tk_utils.getButton(self.main_window, 'login', 'red', self.login)
        self.btn_login_main_win.place(x=750, y=300)

        self.btn_register_new_usr_main_win: tk.Button = tk_utils.getButton(self.main_window, 'Register',
                                                                     'gray', self.registerNewUsr, fg='black')
        self.btn_register_new_usr_main_win.place(x=750, y=400)

        self.webcan_label: tk.Label = tk_utils.getImgLabel(self.main_window)
        self.webcan_label.place(x=10, y=10, width=640, height=450)

        # make test for webcan identified
        self.addWebcan(self.webcan_label)

        #self.prjt_root_dir: str = os.getcwd()
        self.imgs_db_dir: str = './imgs_db'
        if not os.path.exists(self.imgs_db_dir):
            os.mkdir(self.imgs_db_dir)

        self.log_path = './scan_log.txt'



    def addWebcan(self, label: tk.Label) -> None:
        if 'cap' not in self.__dict__: #test if the variable is already created
            self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('J', 'P', 'E', 'G'))

        self._label: tk.Label = label
        self.processWebcan()


    def processWebcan(self) -> None:
        ret: bool
        self.most_recent_cap: np.uint8
        ret, self.most_recent_cap = self.cap.read()

        # process the image from open-cv tpo PIL format
        img_: np.uint8 = openCvLib.bgr2rgb(self.most_recent_cap)
        self.most_recent_cap_pil: Image.Image = Image.fromarray(img_)

        # config the PIL image in the tk.labels obj
        img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        self._label.imgtk: ImageTk.PhotoImage = img_tk
        self._label.configure(image=img_tk)

        # Update the image to appear like a video
        self._label.after(20, self.processWebcan)


    def login(self) -> None:

        result_spoofing_test = test_spoofing(
            image = self.most_recent_cap,
            model_dir = './anti_spoofing/resources/anti_spoof_models',
            device_id = 0)
        if result_spoofing_test['label'] == 1:
            usr_name: str = img_utils.recognize(self.most_recent_cap, self.imgs_db_dir)

            if usr_name in ['person_not_registered', 'no_person_found']:
                tk_utils.msgBox("Blocked", "Unknow user. Register or try again.")
            else:
                tk_utils.msgBox("Passed", "User {} identified.".format(usr_name))

                # create module for log functions
                with open(self.log_path, 'a') as log_file:
                    log_file.write(f'[match] user \'{usr_name}\' - {datetime.datetime.now()} - conf_spoofing: \
                        {result_spoofing_test["conf"]}\n')
                    log_file.close()

        elif result_spoofing_test['label'] != 1:
            tk_utils.msgBox("Blocked", "Spoof atempt detected")
            print('spoof result: ', result_spoofing_test['label'])
            with open(self.log_path, 'a') as log_file:
                log_file.write(f'[spoof_atempt_detected] - {datetime.datetime.now()}\n')
                log_file.close()


    def registerNewUsr(self) -> None:
        # create function to test if user already exist
        self.window_register_new_usr = tk.Toplevel(self.main_window)
        self.window_register_new_usr.geometry("1200x520+370+120")

        self.btn_accept_new_usr_win: tk.Button = tk_utils.getButton(self.window_register_new_usr,'Accept',
                                                                'green', self.acceptRegisterNewUsr, fg='black')
        self.btn_accept_new_usr_win.place(x=750, y=300)

        self.btn_try_again_new_usr_win: tk.Button = tk_utils.getButton(self.window_register_new_usr, 'Try Again',
                                                                'red', self.tryAgainRegisterNewUsr, fg='black')
        self.btn_try_again_new_usr_win.place(x=750, y=400)

        self.capture_label: tk.Label = tk_utils.getImgLabel(self.window_register_new_usr)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.addImg2Label(self.capture_label)

        self.entry_text_register_new_usr: tk.Text = tk_utils.getEntryText(self.window_register_new_usr)
        self.entry_text_register_new_usr.place(x=750, y=150)

        self.label_text_register_new_usr: tk.Label = tk_utils.getTxtLabel(self.window_register_new_usr,
                                                                    'Plase, input username: ')
        self.label_text_register_new_usr.place(x=750, y=70)

    def tryAgainRegisterNewUsr(self) -> None:
        self.window_register_new_usr.destroy()

    def addImg2Label(self, label: tk.Label) -> None:
        img_tk = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        label.imgtk = img_tk
        label.configure(image=img_tk)

        self.register_new_user_capture: np.uint8 = self.most_recent_cap.copy()


    def acceptRegisterNewUsr(self) -> None:
        name: str = self.entry_text_register_new_usr.get(1.0, "end-1c")

        img_path: str = os.path.join(self.imgs_db_dir, '{}.jpeg'.format(name.upper()))
        cv2.imwrite(img_path, self.register_new_user_capture)
        img_utils.fixCorruptJpeg(input_path=img_path, output_path=img_path)

        self.window_register_new_usr.destroy()
        tk_utils.msgBox('Success.', 'User was registered successfully.')



    def start(self) -> None:
        self.main_window.mainloop()

        #treat empty name input




def main() -> None:
    app: App = App()
    app.start()


if __name__ == '__main__':
    main()


