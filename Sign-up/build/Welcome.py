from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Button, PhotoImage, Frame

class Welcome(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Financial Tracker")
        self.master.geometry("1200x700")
        self.master.configure(bg="#FFFFFF")
        self.master.iconphoto(True, PhotoImage(file="assets/frame0/icon.png"))

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"D:\\Python\\Tkinter-Designer-master\\Sign-up\\build\\assets\\frame0")

        self.images = {}
        self._setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def _load_image(self, path, size=None):
        image = Image.open(self.relative_to_assets(path))
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def _setup_ui(self):

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=700,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        canvas.create_rectangle(
            0.0,
            0.0,
            1200.0,
            700.0,
            fill="#F5F5F5",
            outline=""
        )

        canvas.create_text(
            70.0,
            80.0,
            anchor="nw",
            text="Financial Tracker\n\nWelcome",
            fill="#000000",
            font=("Inter", 60 * -1)
        )

        # Sign-in button
        self.images['signin_button'] = self._load_image("signin_button.png", size=(270, 65))
        signin_button = Button(
            image=self.images['signin_button'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Sign-in clicked"),
            relief="flat"
        )
        signin_button.place(
            x=427.0,
            y=390.0,
            width=267.0,
            height=65.0
        )

        # Icon
        self.images['icon'] = self._load_image("icon.png", size=(250, 250))
        canvas.create_image(
            936.0,
            204.0,
            image=self.images['icon']
        )

        # Sign-up button
        self.images['signup_button'] = self._load_image("signup_button.png", size=(270, 65))
        signup_button = Button(
            image=self.images['signup_button'],
            borderwidth=0,
            highlightthickness=0,
            command=self.launch_signup,
            relief="flat"
        )
        signup_button.place(
            x=427.0,
            y=487.0,
            width=267.0,
            height=65.0
        )



    def launch_signup(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        from SignUp import SignUp
        SignUp(self.master).pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    root = Tk()
    welcome_app = Welcome(root)
    welcome_app.pack(side="top", fill="both", expand=True)
    root.mainloop()