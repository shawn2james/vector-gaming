import tkinter as tk
from tkinter.font import Font


class MainButton(tk.Button):
    def __init__(self, con,  **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self['command'] = self.callback
        self['font'] = Font(family="system",
                         size=13
                         )
        self.text_font = Font(family="system", size=13)
        

    def cancel(self):
        self.master.destroy()

    def ok(self):
        pass

    def callback(self):
        pass


class BuyProductBtn(MainButton):
    def __init__(self, con, **kwargs):
        super().__init__(con, **kwargs)

        self.place(
            anchor="center",
            x=130,
            y=160
        )
        
        products = self.con.get_product_names()
        if products==[]:
            self.config(state=tk.DISABLED)

    def callback(self):
        self.window = tk.Toplevel()
        self.window.geometry("600x300")
        self.window.resizable(0, 0)
        self.window.title("Buy Product")
        self.window.grab_set()

        products = self.con.get_product_names() 
        print(products)

        self.selected_product = tk.StringVar()
        self.selected_product.set(products[0])
#
#
        product_name_label = tk.Label(self.window, text="Name of Product:  ", font=self.text_font)
        product_list = tk.OptionMenu(self.window, self.selected_product, *products)

        qty_label = tk.Label(self.window, text="Enter Quantity: ", font=self.text_font)
        self.qty_box = tk.Entry(self.window, width=10)

        cname_label = tk.Label(self.window, text="Enter your name: ", font=self.text_font)
        self.cname_box = tk.Entry(self.window, width=35)
#
        product_name_label.grid(row=0, column=0, padx=25, pady=20)
        product_list.grid(row=0, column=1, pady=20)
        qty_label.grid(row=1, column=0, padx=20, pady=25)
        self.qty_box.grid(row=1, column=1, ipadx=10)
        cname_label.grid(row=2, column=0, padx=20, pady=25)
        self.cname_box.grid(row=2, column=1, ipadx=10, columnspan=2)

        ok_btn = tk.Button(self.window, text="OK", command=self.ok)
        cancel_btn = tk.Button(self.window, text="Cancel", command=self.cancel)

        cancel_btn.grid(row=5, column=2, pady=20)
        ok_btn.grid(row=5, column=1, pady=20)


    def ok(self):
        game_name = self.selected_product.get()
        c_name = self.cname_box.get()
        buying_qty = self.qty_box.get()

        qty = self.con.get_quantity(game_name)

        if int(buying_qty) >= qty:
            buying_qty = qty
            self.con.crs.execute(f'DELETE FROM products WHERE Gamename = "{game_name}";')
            self.con.commit()

        self.con.crs.execute(f'UPDATE products SET Qty = Qty-{buying_qty} WHERE Gamename = "{game_name}";')

        self.con.crs.execute(f'INSERT INTO customers VALUES ("{game_name}", "{c_name}", {buying_qty});')
        self.con.commit()
        self.window.destroy()

        if self.con.table_is_empty("products"):
            self.config(state=tk.DISABLED)
