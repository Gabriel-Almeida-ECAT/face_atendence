import os
import datetime
import cv2
import numpy as np
import tkinter as tk
import ui_utils
import image_utils as img_utils
import log_utils

from ui_utils import grid_ui
from PIL import Image, ImageTk
from gabriels_openCvPyLib import openCvLib
from anti_spoofing.test import test as test_spoofing


main_win_width: int = 560
main_win_height: int = 840

webcan_img_width: int = 480
webcan_img_height: int = 720

grid_calc: grid_ui = grid_ui(grid_rows=24, grid_cols=20, win_width=main_win_width, win_height=main_win_height)


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        #self.main_window.geometry(f"1200x520+350+100")
        self.main_window.geometry(f"{main_win_width}x{main_win_height}")

        '''
        GOAL: get rid of the login button, use a yolo model to detect the presence od a person face and use it to
        trigger the identification.
        OBSTACLE: Don't have GPU and can't be sure the yolo model perfomrance will be acceptable ToT
        '''
        self.btn_login_main_win = ui_utils.getButton(self.main_window, 'login', 'red', self.login)
        self.btn_login_main_win.place(x=160, y=750, width=170, height=60)
        '''self.btn_login_main_win.place(x=grid_calc.getXpixelOfCel(4), y=grid_calc.getYpixelOfCel(21),
                                            width=grid_calc.getSizeHoriCel(7), height=grid_calc.getSizeVertiCel(2))'''

        self.btn_register_new_usr_main_win: tk.Button = ui_utils.getButton(self.main_window, 'Register',
                                                                     'gray', self.registerNewUsr, fg='black')
        self.btn_register_new_usr_main_win.place(x=340, y=750, width=170, height=60)
        '''self.btn_register_new_usr_main_win.place(x=grid_calc.getXpixelOfCel(12), y=grid_calc.getYpixelOfCel(21),
                                            width=grid_calc.getSizeHoriCel(7), height=grid_calc.getSizeVertiCel(2))'''

        self.img_intended_rotation: int = 0
        self.btn_rotate_img_clock_wise: tk.Button = ui_utils.getButton(self.main_window, '↻',
                                                                    'gray', self.incrementAngleClockWise, fg='black')
        self.btn_rotate_img_clock_wise.place(x=40, y=750, width=50, height=60)
        self.btn_rotate_img_anti_clock_wise: tk.Button = ui_utils.getButton(self.main_window, '↺',
                                                                'gray', self.incrementAngleAntiClockWise, fg='black')
        self.btn_rotate_img_anti_clock_wise.place(x=100, y=750, width=50, height=60)

        self.webcan_label: tk.Label = ui_utils.getImgLabel(self.main_window)
        '''self.webcan_label.place(x=grid_calc.getXpixelOfCel(1), y=grid_calc.getYpixelOfCel(1), 
                                            width=grid_calc.getSizeHoriCel(18), height=grid_calc.getSizeVertiCel(18))'''
        self.webcan_label.place(x=40, y=10, width=480, height=720)


        # make test for webcan identified
        self.addWebcan(self.webcan_label)

        #self.prjt_root_dir: str = os.getcwd()
        self.imgs_db_dir: str = r'./imgs_db'
        os.makedirs(self.imgs_db_dir, exist_ok=True)

        os.makedirs(r'./logs/', exist_ok=True)
        self.scan_log_path = './logs/scan_log.txt'



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
        self.most_recent_cap: np.uint8 = self.rotateImg(self.most_recent_cap)
        img_: np.uint8 = openCvLib.bgr2rgb(self.most_recent_cap)
        self.most_recent_cap_pil: Image.Image = Image.fromarray(img_)

        # config the PIL image in the tk.labels obj
        img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        self._label.imgtk: ImageTk.PhotoImage = img_tk
        self._label.configure(image=img_tk)

        # Update the image to appear like a video
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self._label.after(int((1/self.frame_rate)*1000), self.processWebcan)

    def rotateImgClockWise(self):
        pass


    def incrementAngleClockWise(self):
        self.img_intended_rotation = self.img_intended_rotation - 90 \
            if self.img_intended_rotation != 0 \
            else 270


    def incrementAngleAntiClockWise(self):
        self.img_intended_rotation = self.img_intended_rotation + 90 \
            if self.img_intended_rotation != 270 \
            else 0


    def rotateImg(self, img_obj: np.uint8) -> np.uint8:
        if self.img_intended_rotation == 90:
            return np.transpose(img_obj, (1, 0, 2))

        elif self.img_intended_rotation == 180:
            return cv2.flip(img_obj, -1)

        elif self.img_intended_rotation == 270:
            img_obj: np.uint8 = cv2.flip(img_obj, -1)
            return np.transpose(img_obj, (1, 0, 2))

        elif self.img_intended_rotation == 0:
            return img_obj



    def login(self) -> None:

        result_spoofing_test = test_spoofing(
            image = self.most_recent_cap,
            model_dir = './anti_spoofing/resources/anti_spoof_models',
            device_id = 0)
        if result_spoofing_test['label'] in [1, 0]:
            usr_name: str = img_utils.recognize(self.most_recent_cap, self.imgs_db_dir)

            if usr_name in ['person_not_registered', 'no_person_found']:
                ui_utils.msgBox("Blocked", "Unknow user. Register or try again.")
                unkown_msg: str = f'[unkown] unknown person atempt - {datetime.datetime.now()} - real_face_score: \
                                        {result_spoofing_test["conf"]:.2f}\n'
                log_utils.scan_log(self.scan_log_path, unkown_msg)

            else:
                ui_utils.msgBox("Passed", "User {} identified.".format(usr_name))

                match_msg: str = f'[match] user \'{usr_name}\' - {datetime.datetime.now()} - real_face_score: \
                        {result_spoofing_test["conf"]:.2f}\n'
                log_utils.scan_log(self.scan_log_path, match_msg)

        elif result_spoofing_test['label'] not in [1, 0]:
            ui_utils.msgBox("Blocked", "Spoof atempt detected")
            print('spoof result: ', result_spoofing_test['label'])

            spoof_msg: str = f'[spoof_atempt_detected] - {datetime.datetime.now()} - fake_face_score: \
                        {result_spoofing_test["conf"]:.2f}\n'
            log_utils.scan_log(self.scan_log_path, spoof_msg)


    def registerNewUsr(self) -> None:
        # create function to test if user already exist
        self.window_register_new_usr = tk.Toplevel(self.main_window)
        self.window_register_new_usr.geometry("1200x520+370+120")

        self.btn_accept_new_usr_win: tk.Button = ui_utils.getButton(self.window_register_new_usr,'Accept',
                                                                'green', self.acceptRegisterNewUsr, fg='black')
        self.btn_accept_new_usr_win.place(x=750, y=300)

        self.btn_try_again_new_usr_win: tk.Button = ui_utils.getButton(self.window_register_new_usr, 'Try Again',
                                                                'red', self.tryAgainRegisterNewUsr, fg='black')
        self.btn_try_again_new_usr_win.place(x=750, y=400)

        self.capture_label: tk.Label = ui_utils.getImgLabel(self.window_register_new_usr)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.addImg2Label(self.capture_label)

        self.entry_text_register_new_usr: tk.Text = ui_utils.getEntryText(self.window_register_new_usr)
        self.entry_text_register_new_usr.place(x=750, y=150)

        self.label_text_register_new_usr: tk.Label = ui_utils.getTxtLabel(self.window_register_new_usr,
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
        ui_utils.msgBox('Success.', 'User was registered successfully.')



    def start(self) -> None:
        self.main_window.mainloop()

        #treat empty name input




def main() -> None:
    app: App = App()
    app.start()


if __name__ == '__main__':
    main()