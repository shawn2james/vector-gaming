import tkinter as tk
from tkinter.font import Font


class MainButton(tk.Button):
    """
    A base class that all the buttons used in the app inherits from.
    Also inherits from tkinter's Button class
    Parameters:
        con: a Connector class instance imported from connector.py
         x, y, **kwargs: all the arguments that tkinter's Button class requires
    """

    def __init__(self, con, x, y, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.x, self.y = x, y
        self['command'] = self.callback
        self['font'] = Font(family="system",
                            size=13
                            )
        self['width'] = 16
        self['height'] = 3
        self['fg'] = 'white'
        self['bg'] = 'black'
        self['borderwidth'] = 4
        self.text_font = Font(family="system", size=13)

        self.place(
            anchor="center",
            x=self.x,
            y=self.y
                )

    def callback(self):
        pass

    def ok(self):
        pass


class BuyProductBtn(MainButton):
    """
    A subclass of MainButton class.
    The button that provides the functionality to buy a product.
    """

    def __init__(self, con, x, y, **kwargs):
        super().__init__(con,x, y, **kwargs)


    def callback(self):
        # configuring the  popup window when button is pressed
        self.window = tk.Toplevel()
        self.window.geometry("600x300")
        self.window.resizable(0, 0)
        self.window.title("Buy Product")
        self.window.grab_set()

        # getting the product names to be given to tk.OptionMenu
        products = self.con.get_names('products')
        self.selected_product = tk.StringVar()
        self.selected_product.set(products[0])

        # initializing the widgets to be placed in the popup window
        product_name_label = tk.Label(
            self.window, text="Name of Product:  ", font=self.text_font)
        product_list = tk.OptionMenu(
            self.window, self.selected_product, *products)

        qty_label = tk.Label(
            self.window, text="Enter Quantity: ", font=self.text_font)
        self.qty_box = tk.Entry(self.window, width=10)

        cname_label = tk.Label(
            self.window, text="Enter your name: ", font=self.text_font)
        self.cname_box = tk.Entry(self.window, width=35)
#
        # placing the widgets in the popup window
        product_name_label.grid(row=0, column=0, padx=25, pady=20)
        product_list.grid(row=0, column=1, pady=20)
        qty_label.grid(row=1, column=0, padx=20, pady=25)
        self.qty_box.grid(row=1, column=1, ipadx=10)
        cname_label.grid(row=2, column=0, padx=20, pady=25)
        self.cname_box.grid(row=2, column=1, ipadx=10, columnspan=2)

        ok_btn = tk.Button(self.window, text="OK", command=self.ok)
        cancel_btn = tk.Button(self.window, text="Cancel",
                               command=self.window.destroy)

        cancel_btn.grid(row=5, column=2, pady=20)
        ok_btn.grid(row=5, column=1, pady=20)

    def ok(self):
        # getting the values entered by the user
        game_name = self.selected_product.get()
        c_name = self.cname_box.get()
        buying_qty = self.qty_box.get()

        qty = self.con.get_quantity(game_name)

        # if the quantity wanted by the customer is more than the available quantity, sell every piece of the product
        if int(buying_qty) >= qty:
            buying_qty = qty
            self.con.crs.execute(
                f'DELETE FROM products WHERE Gamename = "{game_name}";')
            self.con.commit()

        # update quantity in MySQL table
        self.con.crs.execute(
            f'UPDATE products SET Qty = Qty-{buying_qty} WHERE Gamename = "{game_name}";')

        # add customer to the customer table
        self.con.crs.execute(
            f'INSERT INTO customers VALUES ("{game_name}", "{c_name}", {buying_qty});')
        self.con.commit()

        self.window.destroy()


class OrderProductBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con,  x, y, **kwargs)


class RemoveProductBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con, x, y, **kwargs)




class RemoveCustomerBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con,  x, y, **kwargs)

    def callback(self):
        remove_customer_window = tk.Toplevel()
        remove_customer_window.title("Remove Product")
        remove_customer_window.resizable(0, 0)
        remove_customer_window.grab_set()


        customers = self.con.get_names('customers')
        self.selected_customer = tk.StringVar()
        self.selected_customer.set(customers[0])

        label_font = Font(family="system", size=13)

        cname_label = tk.Label(
            remove_customer_window, text="Name of Customer to be removed:  ", font=label_font)
        customer_list = tk.OptionMenu(remove_customer_window, self.selected_customer, *customers)

        cname_label.grid(row=0, column=0, padx=25, pady=20)
        customer_list.grid(row=0, column=1, pady=20, columnspan=2)

        ok_btn = tk.Button(remove_customer_window, text="OK", command=self.ok)
        cancel_btn = tk.Button(remove_customer_window, text="Cancel", command=remove_customer_window.destroy)

        ok_btn.grid(row=5, column=1, pady=35, padx=30)
        cancel_btn.grid(row=5, column=2, pady=20)


class ViewDatabaseBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con, x, y, **kwargs)
