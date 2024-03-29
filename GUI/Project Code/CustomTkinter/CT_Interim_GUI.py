import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("System User Interface")
        self.geometry(f"{1400}x{680}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="User Interface", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Enable Autofocus", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Disable Autofocus", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    
        # create textbox
        self.textbox_1 = customtkinter.CTkTextbox(self, width=750)
        self.textbox_1.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsw")

        self.textbox_2 = customtkinter.CTkTextbox(self, width=400)
        self.textbox_2.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsw")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_11 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=10)
        self.slider_11.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider11_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Brightness Adjustment", anchor="center")
        self.slider11_label.grid(row=3, column=2, padx=10, pady=(10, 0))
        self.slider_12 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=10)
        self.slider_12.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider12_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Contrast Adjustment", anchor="center")
        self.slider12_label.grid(row=4, column=2, padx=10, pady=(10, 0))
        self.slider_13 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=10)
        self.slider_13.grid(row=5, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider13_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Noise Reduction", anchor="center")
        self.slider13_label.grid(row=5, column=2, padx=10, pady=(10, 0))  


        self.slider_progressbar_frame_2 = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame_2.grid(row=1, column=2, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="ne")
        self.slider_progressbar_frame_2.grid_columnconfigure(1, weight=1)
        self.slider_progressbar_frame_2.grid_rowconfigure(4, weight=1)
        self.slider_21 = customtkinter.CTkSlider(self.slider_progressbar_frame_2, from_=0, to=1, number_of_steps=10)
        self.slider_21.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ne")
        self.slider_22 = customtkinter.CTkSlider(self.slider_progressbar_frame_2, from_=0, to=1, number_of_steps=10)
        self.slider_22.grid(row=4, column=1, padx=(20, 10), pady=(10, 10), sticky="ne")
        self.slider_23 = customtkinter.CTkSlider(self.slider_progressbar_frame_2, from_=0, to=1, number_of_steps=10)
        self.slider_23.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ne")
    

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.slider_11.configure(command=self)
        self.slider_12.configure(command=self)
        self.slider_13.configure(command=self)
        self.slider_12.configure(command=self)
        self.slider_21.configure(command=self)
        self.slider_22.configure(command=self)
        self.slider_23.configure(command=self)
       
        self.textbox_1.insert("0.0", "Raspberry Pi Live Camera Feed")
        self.textbox_2.insert("0.0", "Raspberry Pi Camera Image Snapshot")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()