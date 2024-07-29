import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os
import subprocess



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
        self.sample_dir = './sample_dir'
        if not os.path.exists(self.sample_dir):
            os.mkdir(self.sample_dir)
        unknown_img_path = './sample_dir/sample_tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition',self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]
        if name in ['unknown_person','no_persons_found']:
            util.msg_box('Oops!','You either not a human being, or unregistered human being, pls register if u are human')
        else:
            util.msg_box('welcome back!','Hi, {}'.format(name))
        print(name + " from "+ output)
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