import re
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from PIL import Image, ImageTk
import bcrypt


class SignUp(tk.Frame):
    def __init__(self, signup_window):
        super().__init__(signup_window)
        self.window = signup_window
        self.window.geometry("1500x750")
        self.window.configure(bg="#82AC81")
        self.window.title("Financial Tracker")
        self.window.iconphoto(True, PhotoImage(file="assets/frame0/icon.png"))

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"D:\\Python\\Tkinter-Designer-master\\Sign-up\\build\\assets\\frame0")

        self.canvas = Canvas(
            self.window,
            bg="#82AC81",
            height=750,
            width=1500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.images = {}
        self.setup_database()
        self._setup_ui()
        self.setup_database()


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def load_image(self, path, size=None):
        image_path = self.relative_to_assets(path)
        image = Image.open(image_path)
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)


    def _setup_ui(self):
        self.username_entry = self.create_placeholder_entry("Username", 50, 95)
        self.email_entry = self.create_placeholder_entry("Email (e.g., abc@def.xyz)", 50, 235)
        self.password_entry = self.create_placeholder_entry("Password", 50, 390, show="*")
        self.confirmation_entry = self.create_placeholder_entry("Confirm Password", 50, 595, show="*")

        self.canvas.create_text(
            40.0,
            40.0,
            anchor="nw",
            text="Username",
            fill="#000000",
            font=("Inter SemiBoldItalic", 35 * -1)
        )

        self.images["username_field"] = self.load_image("username_field.png", (500, 90))
        self.canvas.create_image(
            295.0,
            130.0,
            image=self.images["username_field"]
        )
        self.username_entry = self.create_placeholder_entry("Username", 50, 95)

        self.username_entry.place(
            x=50.0,
            y=95.0,
            width=470.0,
            height=70.0
        )

        self.canvas.create_text(
            40.0,
            185.0,
            anchor="nw",
            text="Email",
            fill="#000000",
            font=("Inter SemiBoldItalic", 35 * -1)
        )

        self.images["email_field"] = self.load_image("email_field.png", (500, 90))
        self.canvas.create_image(
            295.0,
            275.0,
            image=self.images["email_field"]
        )
        self.email_entry = self.create_placeholder_entry("Email", 50, 235)
        self.email_entry.place(
            x=50.0,
            y=235.0,
            width=470.0,
            height=70.0
        )

        self.canvas.create_text(
            40.0,
            335.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Inter SemiBoldItalic", 35 * -1)
        )

        self.images["password_field"] = self.load_image("password_field.png", (500, 90))
        self.canvas.create_image(
            295.0,
            430.0,
            image=self.images["password_field"]
        )
        self.password_entry = self.create_placeholder_entry("Password", 50, 390, show="*")
        self.password_entry.place(
            x=50.0,
            y=390.0,
            width=470.0,
            height=70.0
        )

        self.canvas.create_text(
            45.0,
            485.0,
            anchor="nw",
            text="*Password length must be at least 8 characters \n  ,including letters, numbers & symbols",
            fill="#343434",
            font=("Inter BoldItalic", 20 * -1)
        )

        self.canvas.create_text(
            40.0,
            540.0,
            anchor="nw",
            text="Confirm Password",
            fill="#000000",
            font=("Inter SemiBoldItalic", 35 * -1)
        )

        self.images["confirmation_field"] = self.load_image("confirmation_field.png", (500, 90))
        self.canvas.create_image(
            295.0,
            635.0,
            image=self.images["confirmation_field"]
        )
        self.confirmation_entry = self.create_placeholder_entry("Confirm Password", 50, 390, show="*")
        self.confirmation_entry.place(
            x=50.0,
            y=595.0,
            width=470.0,
            height=70.0
        )

        self.canvas.create_text(
            800.0,
            60.0,
            anchor="nw",
            text="Sign up",
            fill="#000000",
            font=("Inter", 100 * -1)
        )

        self.images["signup_image"] = self.load_image("signup_image.png")
        self.canvas.create_image(
            1038.0,
            400.0,
            image=self.images["signup_image"]
        )

        self.images["signup_button"] = self.load_image("confirm_signup_button.png", (267, 93))
        signup_button = Button(
            image=self.images["signup_button"],
            borderwidth=0,
            highlightthickness=0,
            command=self.register_user,
            relief="flat"
        )
        signup_button.place(
            x=1080.0,
            y=630.0,
            width=267.0,
            height=93.0
        )

        self.images["cancel_button"] = self.load_image("cancel_button.png", (267, 93))
        cancel_button = Button(
            image=self.images["cancel_button"],
            borderwidth=0,
            highlightthickness=0,
            command=self.launch_welcome,
            relief="flat"
        )
        cancel_button.place(
            x=800.0,
            y=630.0,
            width=267.0,
            height=93.0
        )



    def create_placeholder_entry(self, placeholder, x, y, show=None):
        entry = Entry(self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter", 15), show=show)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.set_placeholder(entry, placeholder))
        entry.place(x=x, y=y, width=470.0, height=70.0)
        return entry

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            if entry in [self.password_entry, self.confirmation_entry]:
                entry.config(show="*")

    def set_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            if entry in [self.password_entry, self.confirmation_entry]:
                entry.config(show="")

    def setup_database(self):
        self.connection = sqlite3.connect(r"D:\Python\Tkinter-Designer-master\database.db")
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9@$!%*?&#]", password):
            return False
        return True

    def register_user(self):

        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirmation = self.confirmation_entry.get().strip()

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        if not self.validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters with upper/lowercase letters, numbers, and symbols.")
            return

        if password != confirmation:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            self.cursor.execute("INSERT INTO User (user_name, email, password) VALUES (?, ?, ?)",
                                (username, email, password.decode("utf-8")))
            self.connection.commit()
            messagebox.showinfo("Success", "Sign up successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")

    def __del__(self):
        if hasattr(self, "connection"):
            self.connection.close()

    def launch_welcome(self):
        from Welcome import Welcome
        for widget in self.window.winfo_children():
            widget.destroy()
        Welcome(self.window)


if __name__ == "__main__":
    window = Tk()
    app = SignUp(window)
    window.resizable(True, True)
    window.mainloop()
