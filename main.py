import os
import datetime
import cv2
import numpy as np
import tkinter as tk
import ui_utils
import image_utils as img_utils
import log_utils

from PIL import Image, ImageTk
from gabriels_openCvPyLib import openCvLib
from anti_spoofing.test import test as test_spoofing

#treat empty name input
# make test to asure webcan is available

class App:
    def __init__(self):
        # UI Consts
        self.webcan_img_width: int = 480
        self.webcan_img_height: int = 720

        self.v_space: int = 1
        self.h_space: int = int(720 * 0.05)
        self.main_win_width: int = self.webcan_img_width + 2 * self.h_space
        self.main_win_height: int = self.webcan_img_height + 4 * self.v_space + 120

        self.text_y_pos: int = self.webcan_img_height + 1 * self.v_space

        self.btns_heigth: int = 50
        #self.btns_y_pos: int = self.webcan_img_height + 2*self.v_space + self.btns_heigth
        self.btns_y_pos: int = self.webcan_img_height + 2 * self.v_space + 45

        # main window creation
        self.main_window = tk.Tk()
        self.main_window.geometry(f"{self.main_win_width}x{self.main_win_height}")

        '''
        GOAL: get rid of the login button, use a yolo model to detect the presence od a person face and use it to
        trigger the identification.
        OBSTACLE: Don't have GPU and can't be sure the yolo model perfomrance will be acceptable ToT
        '''
        # login button
        self.btn_login_main_win = ui_utils.getButton(self.main_window, 'login', 'red', self.login)
        self.btn_login_main_win.place(x=160, y=self.btns_y_pos, width=170, height=self.btns_heigth)

        # register button
        self.btn_register_new_usr_main_win: tk.Button = ui_utils.getButton(self.main_window, 'Register',
                                                                     'gray', self.registerNewUsr, fg='black')
        self.btn_register_new_usr_main_win.place(x=340, y=self.btns_y_pos, width=170, height=self.btns_heigth)

        # image rotation image
        self.img_intended_rotation: int = 0
        self.btn_rotate_img_clock_wise: tk.Button = ui_utils.getButton(self.main_window, '↻',
                                                            'gray', self.incrementAngleClockWise, fg='black')
        self.btn_rotate_img_clock_wise.place(x=self.h_space, y=self.btns_y_pos, width=50, height=self.btns_heigth)
        self.btn_rotate_img_anti_clock_wise: tk.Button = ui_utils.getButton(self.main_window, '↺',
                                                        'gray', self.incrementAngleAntiClockWise, fg='black')
        self.btn_rotate_img_anti_clock_wise.place(x=100, y=self.btns_y_pos, width=50, height=self.btns_heigth)

        # text
        self.output_msg: str = 'Waiting scan.'
        self.label_text_scan_ouput: tk.Label = ui_utils.getTxtLabel(self.main_window,self.output_msg)
        self.label_text_scan_ouput.place(x=self.h_space, y=self.text_y_pos)

        # add webcan image
        self.webcan_label: tk.Label = ui_utils.getImgLabel(self.main_window)
        self.webcan_label.place(x=self.h_space, y=0, width=480, height=720)

        self.addWebcan(self.webcan_label)

        #self.prjt_root_dir: str = os.getcwd()
        self.imgs_db_dir: str = r'./imgs_db'
        os.makedirs(self.imgs_db_dir, exist_ok=True)



    def addWebcan(self, label: tk.Label) -> None:
        if 'cap' not in self.__dict__: #test if the variable is already created
            self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('J', 'P', 'E', 'G'))

        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.ms_until_next_frame = int((1 / self.frame_rate) * 1000)

        self._label: tk.Label = label
        self.processWebcan()


    def processWebcan(self) -> None:
        ret: bool
        self.most_recent_cap: np.uint8
        ret, self.most_recent_cap = self.cap.read()

        # process the image from open-cv tpo PIL format
        self.rotated_crt_cap: np.uint8 = self.rotateImg(self.most_recent_cap)
        img_: np.uint8 = openCvLib.bgr2rgb(self.rotated_crt_cap)
        self.rotated_crt_cap_pil: Image.Image = Image.fromarray(img_)

        # config the PIL image in the tk.labels obj
        img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=self.rotated_crt_cap_pil)
        self._label.imgtk: ImageTk.PhotoImage = img_tk
        self._label.configure(image=img_tk)

        # Update the image to appear like a video
        self._label.after(self.ms_until_next_frame, self.processWebcan)

        # update output text
        self.label_text_scan_ouput.configure(text=self.output_msg)


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
        if result_spoofing_test['conf'] < 0.70:
            usr_name: str = img_utils.recognize(self.most_recent_cap, self.imgs_db_dir)

            if usr_name in ['person_not_registered', 'no_person_found']:
                #ui_utils.msgBox("Blocked", "Unknow user. Register or try again.")
                unkown_msg: str = f'[unkown] unknown person atempt - {datetime.datetime.now()} - real_face_score: \
                                        {result_spoofing_test["conf"]:.2f}\n'
                log_utils.scan_log(unkown_msg)

                self.output_msg: str = "Blocked: unknown/not registered user."

            else:
                #ui_utils.msgBox("Passed", "User {} identified.".format(usr_name))

                match_msg: str = f'[match] user \'{usr_name}\' - {datetime.datetime.now()} - real_face_score: \
                        {result_spoofing_test["conf"]:.2f}\n'
                log_utils.scan_log(match_msg)

                self.output_msg: str = f'Passed: match user \'{usr_name}\'.'

        elif result_spoofing_test['conf'] >= 0.70:
            #ui_utils.msgBox("Blocked", "Spoof atempt detected")

            spoof_msg: str = f'[spoof_atempt_detected] - {datetime.datetime.now()} - fake_face_score: \
                        {result_spoofing_test["conf"]:.2f}\n'
            log_utils.scan_log(spoof_msg)

            self.output_msg: str = f'Blocked: spoof atempt  detected with {result_spoofing_test["conf"]:.2f} confidence.'


    def registerNewUsr(self) -> None:
        # create function to test if user already exist
        self.window_register_new_usr = tk.Toplevel(self.main_window)
        self.window_register_new_usr.geometry(f"{self.main_win_width}x{self.main_win_height}")

        self.btn_accept_new_usr_win: tk.Button = ui_utils.getButton(self.window_register_new_usr,'Accept',
                                                                'green', self.acceptRegisterNewUsr, fg='black')
        self.btn_accept_new_usr_win.place(x=360, y=self.text_y_pos)

        self.btn_try_again_new_usr_win: tk.Button = ui_utils.getButton(self.window_register_new_usr, 'Try Again',
                                                                'red', self.tryAgainRegisterNewUsr, fg='black')
        self.btn_try_again_new_usr_win.place(x=360, y=self.text_y_pos+50)

        self.capture_label: tk.Label = ui_utils.getImgLabel(self.window_register_new_usr)
        self.capture_label.place(x=40, y=10, width=self.webcan_img_width, height=self.webcan_img_height)

        self.addImg2Label(self.capture_label)

        self.entry_text_register_new_usr: tk.Text = ui_utils.getEntryText(self.window_register_new_usr)
        self.entry_text_register_new_usr.place(x=self.h_space, y=self.text_y_pos + self.btns_heigth)

        self.label_text_register_new_usr: tk.Label = ui_utils.getTxtLabel(self.window_register_new_usr,
                                                                    'Plase, input username: ')
        self.label_text_register_new_usr.place(x=self.h_space, y=self.text_y_pos)

    def tryAgainRegisterNewUsr(self) -> None:
        self.window_register_new_usr.destroy()

    def addImg2Label(self, label: tk.Label) -> None:
        img_tk = ImageTk.PhotoImage(image=self.rotated_crt_cap_pil)
        label.imgtk = img_tk
        label.configure(image=img_tk)

        self.register_new_user_capture: np.uint8 = self.most_recent_cap.copy()


    def acceptRegisterNewUsr(self) -> None:
        name: str = self.entry_text_register_new_usr.get(1.0, "end-1c")
        name: str = name.upper()

        img_path: str = os.path.join(self.imgs_db_dir, '{}.jpeg'.format(name))
        cv2.imwrite(img_path, self.register_new_user_capture)
        img_file_fixed: bool = img_utils.fixCorruptJpeg(input_path=img_path, output_path=img_path)
        if img_file_fixed:
            register_msg: str = f'[saved_user] \'{name}\' - {datetime.datetime.now()}\n'
            log_utils.register_log(register_msg)

        self.window_register_new_usr.destroy()
        ui_utils.msgBox('Success.', f'User \'{name}\' was registered successfully.')


    def start(self) -> None:
        self.main_window.mainloop()


def main() -> None:
    app: App = App()
    app.start()


if __name__ == '__main__':
    main()