# 3D Printed Biomedical Imaging and Classification System GUI
from customtkinter import *
import cv2
from PIL import Image, ImageTk
import threading

#Set up GUI Appearance 
set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Set up GUI Class, customtkinter
class App(CTk):
    def __init__(self):
        super().__init__()
        
        #Setting up the window
        self.title("3D Printed Biomedical Imaging and Classification System GUI")
        self.geometry("1400x680")

        #Setting up the Grid Layout(4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=5)

        #Setting up sidebar fram with buttons
        #Setting up sidebar frame and grid position 
        self.sidebar_frame = CTkFrame(self, width=100)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=0)
        #Sidebar Label
        self.sidebar_label = CTkLabel(self.sidebar_frame, text="GUI Buttons", font=CTkFont(size=18, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Sidebar Buttons
        self.camfeedon_button = CTkButton(self.sidebar_frame, text="Enable Camera Feed", command=self.start_camera_feed) #Enable Camerafeed button
        self.camfeedon_button.grid(row=1, column=0, padx=20, pady=10)
        self.camfeedoff_button = CTkButton(self.sidebar_frame, text="Disable Camera Feed", command=self.stop_camera_feed) #Disable Camerafeed button
        self.camfeedoff_button.grid(row=2, column=0, padx=20, pady=10)
        self.autofocuson_button = CTkButton(self.sidebar_frame, text="Enable Autofocus Routine", command=self.sidebar_button_event) #Enable Autofocus button
        self.autofocuson_button.grid(row=3, column=0, padx=20, pady=10 )
        self.autofocusoff_button = CTkButton(self.sidebar_frame, text="Disable Autofocus Routine", command=self.sidebar_button_event) #Disable Autofocus button
        self.autofocusoff_button.grid(row=4, column=0, padx=20, pady=10 )
        #Appearance Mode Change Menu
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        #UI Scaling Change Menu
        self.scaling_label = CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Adding a frame to show the camera feed
        self.camera_feed_frame = CTkFrame(self, width=600, height=400)
        self.camera_feed_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20)
        self.dispW=320
        self.dispH=240
        self.flip=2
        self.camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, width='+str(self.dispW)+', height='+str(self.dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        self.cam=cv2.VideoCapture(self.camSet)
        self.camera_feed_on = False

    #Defining Change Appearance Mode event
    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)  

    #Definining Change UI scaling event 
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)
    
    #Defining Start Camera Feed event
    def start_camera_feed(self):
        # Starting the camera feed in a new thread
        self.camera_feed_on = True
        self.camera_feed_thread = threading.Thread(target=self.update_camera_feed)
        self.camera_feed_thread.start()
    
    #Defining the Stop Camera feed event
    def stop_camera_feed(self):
        self.camera_feed_on = False

    #Defining the update camera feed event
    def update_camera_feed(self):
        while self.camera_feed_on:
            ret, frame = self.cam.read()
            if ret:
                # Converting the frame to RGB for Tkinter compatibility
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Creating a PhotoImage object to show the frame in the Tkinter label
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                label = CTkLabel(self.camera_feed_frame, image=img)
                label.image = img
                label.pack()
                cv2.waitKey(1) # Adding a delay to make the camera feed look smoother
            else:
                print("Error: Failed to read frame from camera")
                self.stop_camera_feed()
    
    # Release the camera feed capture object when closing the window
    def on_closing(self):
        self.cam.release()
        cv2.destroyAllWindows()
        super().on_closing()

    #Defining Sidebar Button event 
    def sidebar_button_event(self):
        print("sidebar_button click")
 
if __name__ == "__main__":
    app = App()
    app.mainloop()