import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os
import subprocess
import numpy as np
from datetime import datetime
from io import BytesIO
import face_recognition
import time


class App:
    dir_path = os.path.dirname(os.path.realpath(__file__))+"/face_sample"
    print("current path: "+dir_path)
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750,y=300)
        self.register_button_main_window = util.get_button(self.main_window, 'register', 'gray', self.register_new_user, fg='black')
        self.register_button_main_window.place(x=750,y=400)
        
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10,y=0,width=700,height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        
        self.log_path = './logs/log.txt'


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            
        self._label = label

        self.process_webcam()
    
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        face_detector = cv2.CascadeClassifier("face_ref_alt.xml")
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
       

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20,self.process_webcam)

    
    def login(self):
        
        start_time = time.time()
        unknown_img_path = './scanned_img_tmp/scanned.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        try:
            print('starting process')
            processing = subprocess.check_output(['face_recognition', '--tolerance', '0.2', self.db_dir, unknown_img_path])
            
            output = processing.decode('utf-8').strip()
            
            name = output.split(',')[1].split()[0].strip()
        

            if name in ['unkown_person', 'no_persons_found']:
                util.msg_box('PERINGATAN!','User tidak dikenal!')
            else:
                print(name)
                util.msg_box('Registrasi Berhasil', 'Selamat Datang, {}'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{} - {} \n'.format(name, datetime.now()))
                    f.close()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"elapsed time: {elapsed_time:.3f} seconds")
        except subprocess.CalledProcessError as e:
            util.msg_box('Error!', f'terjadi error: {e}')
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"elapsed time: {elapsed_time:.3f} seconds")

        os.remove(unknown_img_path)
        

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
    
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=850,y=300)
        self.try_again_button_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.accept_register_new_user)
        self.try_again_button_user_window.place(x=850,y=400)

        self.capture_label =  util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10,y=0,height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=800,y=190,height=50)
        
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Input your username')
        self.text_label_register_new_user.place(x=750,y=150)


    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0,"end-1c")
        cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Success','User Successfully Registered!')

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()




if __name__ == '__main__':
    app = App()
    app.start()