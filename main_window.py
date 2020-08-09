import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
from buttons import *


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

    def create_background(self):
        # creates the main menu
        background_img = Image.open('background.png').resize(
            (self.width, self.height))
        background_img_tk = ImageTk.PhotoImage(background_img)
        background = tk.Label(self, image=background_img_tk)
        background.image = background_img_tk
        background.place(x=0, y=0, relwidth=1, relheight=1)

        # title settings
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

        self.create_btns()

    def create_btns(self):
        # BUY BUTTON
        buy_btn = BuyProductBtn(
            self.con,
            x=130,
            y=160,
            master=self,
            text="Buy Product",
        )

        order_product_btn = OrderProductBtn(
            self.con,
            x=360,
            y=160,
            master=self,
            text="Order Product"
        )

        remove_product_btn = RemoveProductBtn(
            self.con,
            x=620,
            y=160,
            master=self,
            text="Remove Product",
        )

        remove_customer_btn = RemoveCustomerBtn(
            self.con,
            x=910,
            y=160,
            master=self,
            text="Remove Customer"
        )

        view_database_btn = ViewDatabaseBtn(
                self.con,
                x=1200,
                y=160,
                master=self, 
                text="View Database"
                )

        if self.con.table_is_empty('products'):
            buy_btn.config(state=tk.DISABLED)
            remove_product_btn.config(state=tk.DISABLED)
        if self.con.table_is_empty('customers'):
            remove_customer_btn.config(state=tk.DISABLED)
