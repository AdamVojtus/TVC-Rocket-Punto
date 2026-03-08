import customtkinter as ctk
import telemetryRead as tr
from PIL import Image
import os

PASSWORD = "31"
script_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(script_dir, "image.png")

class ScintillaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Scintilla Telemetry Display - IGNIS Project")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")

        self.label = ctk.CTkLabel(self, text="IGNIS - SCINTILLA TELEMETRY", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        try:
            pil_img = Image.open(IMAGE_PATH)
            self.logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(200, 100))
            self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"DEBUG - Hľadaná cesta: {IMAGE_PATH}")
            print(f"Chyba: {e}")
            self.logo_label = ctk.CTkLabel(self, text="[ Logo Missing ]")
            self.logo_label.pack(pady=10)

        self.data_frame = ctk.CTkFrame(self)
        self.data_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.pressure_label = ctk.CTkLabel(self.data_frame, text="Pressure: --- Pa", font=("Roboto", 20))
        self.pressure_label.pack(pady=10)

        self.temp_label = ctk.CTkLabel(self.data_frame, text="Temperature: --- °C", font=("Roboto", 20))
        self.temp_label.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.data_frame, text="RAW: ---", font=("Roboto", 12))
        self.info_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Initializing...", text_color="yellow")
        self.status_label.pack(side="bottom", pady=10)

        if tr.connect_system('COM3', 9600):
            self.status_label.configure(text="Status: Connected to IGNIS", text_color="green")
        else:
            self.status_label.configure(text="Status: Connection Failed!", text_color="red")

        self.update_telemetry()

    def update_telemetry(self):
        raw_line = tr.get_latest_data()
        
        if raw_line:
            self.info_label.configure(text=f"RAW: {raw_line}")
            
            if "Pressure:" in raw_line:
                self.pressure_label.configure(text=raw_line)
            
            if "Temp:" in raw_line:
                self.temp_label.configure(text=raw_line)

        self.after(100, self.update_telemetry)

def run_login():
    ctk.set_appearance_mode("dark")
    
    dialog = ctk.CTkInputDialog(text="Type in a password:", title="Login to Scintilla")
    input_password = dialog.get_input()

    if input_password == PASSWORD:
        app = ScintillaApp()
        app.mainloop()
    else:
        print("Access Denied: Incorrect Password")

if __name__ == "__main__":
    run_login()