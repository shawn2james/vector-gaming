import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
from buttons import BuyProductBtn


class MainWindow(tk.Tk):
    def __init__(self, con):
        super().__init__()
        # ROOT SETTINGS
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
        self.title("Vector Gaming Database Management")

        self.con = con

        self.create_background()
        self.create_btns()


    def create_background(self):
        background_img = Image.open('background.png').resize((self.width, self.height))
        background_img_tk = ImageTk.PhotoImage(background_img)
        background = tk.Label(self, image=background_img_tk)
        background.image = background_img_tk
        #  self.background.place(
        #  anchor="center",
        #  x=680,
        #  y=400
        #  )
        background.place(x=0, y=0, relwidth=1, relheight=1)

        # Title - "VCTR GAMING"
        title_font = Font(
            family="system",
            size=40
        )
        title = tk.Label(
            self,
            text="VCTR GAMING",
            font=title_font,
            bg="coral"
        )
        title.place(anchor="w",
                    x=480,
                    y=70
                    )


    def create_btns(self):
        buy_btn = BuyProductBtn(self.con,
                master = self,
                text="Remove Product",
                width=16,
                height=3,
                bg="black",
                fg="white",
                borderwidth=4,
                )

