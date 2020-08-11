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

###############################################################################################################################

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
        self.master.refresh_btns()

################################################################################################################################

class OrderProductBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con,  x, y, **kwargs)

    def callback(self):
        self.window = tk.Toplevel()
        self.window.geometry("850x120")
        self.window.title("confirm")
        self.window.resizable(0, 0)
        self.window.grab_set()

        confirm_label = tk.Label(self.window,
                                 text="Do you want to order an existing product or a new one ?",
                                 font=self.text_font
                                 )
        confirm_label.grid(row=0, column=0, columnspan=3, padx=130, pady=20)

        newp_btn = tk.Button(self.window, text="New Product", font=self.text_font, command=self.new_product)
        existingp_btn = tk.Button( self.window, text="Existing Product", font=self.text_font, command=self.existing_product)
        cancel_btn = tk.Button(self.window, text="Cancel", font=self.text_font, command=self.window.destroy) 

        if self.con.get_names('products')==[]:
            existingp_btn.config(state=tk.DISABLED)

        cancel_btn.grid(row=1, column=0)
        newp_btn.grid(row=1, column=1)
        existingp_btn.grid(row=1, column=2)

    def existing_product(self):
        self.window.destroy()
        self.existingp_window = tk.Toplevel()
        self.existingp_window.geometry("670x240")
        self.existingp_window.title("Buy Existing Product")
        self.existingp_window.resizable(0, 0)
        self.existingp_window.grab_set()

        products = self.con.get_names('products')
        self.selected_product = tk.StringVar()
        self.selected_product.set(products[0])

        # Name of Product - Label
        pname_label = tk.Label(self.existingp_window, text="Name of Game to be ordered:  ", font=self.text_font)
        product_list = tk.OptionMenu(self.existingp_window, self.selected_product, *products)

        qty_label = tk.Label( self.existingp_window, text="Enter Quantity: ", font=self.text_font)
        self.qty_box = tk.Entry(self.existingp_window, width=10)

        pname_label.grid(row=0, column=0, padx=25, pady=20)
        product_list.grid(row=0, column=1, pady=20, columnspan=2)
        product_list.grid(row=0, column=1, pady=20, columnspan=2)
        qty_label.grid(row=1, column=0, padx=20, pady=25)
        self.qty_box.grid(row=1, column=1, ipadx=10)

        ok_btn = tk.Button(self.existingp_window, text="OK", command=self.confirm_existing_product)
        cancel_btn = tk.Button(self.existingp_window, text="Cancel", command=self.existingp_window.destroy)

        ok_btn.grid(row=5, column=1, pady=35, padx=30)
        cancel_btn.grid(row=5, column=2, pady=20)

    def confirm_existing_product(self):
        qty = str(self.qty_box.get())
        if qty:
            self.con.crs.execute(
                    f'UPDATE products SET Qty = Qty + {qty} WHERE Gamename = "{self.selected_product.get()}";')
            self.con.commit()
            self.existingp_window.destroy()
        self.master.refresh_btns()

    def new_product(self):
        self.window.destroy()
        self.newp_window = tk.Toplevel()
        self.newp_window.geometry("650x420")
        self.newp_window.resizable(0, 0)
        self.newp_window.title("Order New Product")
        self.newp_window.grab_set()

        pname_label = tk.Label(self.newp_window, text="Name of Game to be ordered:  ", font=self.text_font)
        self.pname_box = tk.Entry(self.newp_window, width=20)

        id_label = tk.Label(self.newp_window, text="Game Id:  ", font=self.text_font)
        self.id_box = tk.Entry(self.newp_window, width=20)

        platform_label = tk.Label(self.newp_window, text="Gaming Platform:  ", font=self.text_font)
        self.platform_box = tk.Entry(self.newp_window, width=20)

        price_label = tk.Label(self.newp_window, text="Price:  ", font=self.text_font)
        self.price_box = tk.Entry(self.newp_window, width=10)

        genre_label = tk.Label(self.newp_window, text="Genre:  ", font=self.text_font)
        self.genre_box = tk.Entry(self.newp_window, width=20)

        qty_label = tk.Label(self.newp_window, text="Enter quantity:  ", font=self.text_font)
        self.qty_box = tk.Entry(self.newp_window, width=10)

        ok_btn = tk.Button(self.newp_window, text="OK", command=self.confirm_new_product)
        cancel_btn = tk.Button(self.newp_window, text="Cancel", command=self.newp_window.destroy)

        pname_label.grid(row=0, column=0, padx=25, pady=20)
        self.pname_box.grid(row=0, column=1, ipadx=10)

        id_label.grid(row=1, column=0)
        self.id_box.grid(row=1, column=1)

        platform_label.grid(row=2, column=0)
        self.platform_box.grid(row=2, column=1, pady=25)

        price_label.grid(row=3, column=0)
        self.price_box.grid(row=3, column=1)

        genre_label.grid(row=4, column=0, pady=30)
        self.genre_box.grid(row=4, column=1, pady=28)

        qty_label.grid(row=5, column=0)
        self.qty_box.grid(row=5, column=1)

        ok_btn.grid(row=7, column=1, pady=35, padx=30)
        cancel_btn.grid(row=7, column=2, pady=20)

    def confirm_new_product(self):
        game_id = self.id_box.get()
        ids = self.con.get_ids()
        if game_id in ids:
            warning = tk.Label(self.newp_window, text="Game Id already taken!", font=self.text_font, fg="red")
            warning.grid(row=6, column=0, pady=20)

            self.newp_window.after(2000, warning.destroy)
        else:
            game_name = self.pname_box.get()
            platform = self.platform_box.get()
            price = self.price_box.get()
            genre = self.genre_box.get()
            qty = self.qty_box.get()

            if game_name and platform and price and genre and qty:
                self.con.crs.execute(
                        f'INSERT INTO products VALUES ({game_id}, "{game_name}", "{platform}", {price}, "{genre}", {qty});')
                self.con.commit()

                self.newp_window.destroy()
            self.window.destroy()
        self.master.refresh_btns()



##############################################################################################################################

class RemoveProductBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con, x, y, **kwargs)

    def callback(self):
        self.window = tk.Toplevel()
        self.window.geometry("670x150")
        self.window.title("Remove Customer")
        self.window.resizable(0, 0)
        self.window.grab_set()

        # getting the product names to be given to tk.OptionMenu
        products = self.con.get_names('products')
        self.selected_product = tk.StringVar()
        self.selected_product.set(products[0])

        pname_label = tk.Label(self.window, text="Name of Game to be removed:  ", font=self.text_font)
        product_list = tk.OptionMenu(self.window, self.selected_product, *products)

        ok_btn = tk.Button(self.window, text="OK", command=self.ok)
        cancel_btn = tk.Button(self.window, text="Cancel", command=self.window.destroy)

        pname_label.grid(row=0, column=0, padx=25, pady=20)
        product_list.grid(row=0, column=1, pady=20, columnspan=2)

        ok_btn.grid(row=5, column=1, pady=35, padx=30)
        cancel_btn.grid(row=5, column=2, pady=20)

    def ok(self):
        self.con.crs.execute(f'DELETE FROM products WHERE Gamename = "{self.selected_product.get()}";')
        self.con.commit()
        self.window.destroy()
        self.master.refresh_btns()


##############################################################################################################################

class RemoveCustomerBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con,  x, y, **kwargs)

    def callback(self):
        self.window = tk.Toplevel()
        self.window.title("Remove Product")
        self.window.resizable(0, 0)
        self.window.grab_set()

        customers = self.con.get_names('customers')
        self.selected_customer = tk.StringVar()
        self.selected_customer.set(customers[0])

        self.text_font = Font(family="system", size=13)

        cname_label = tk.Label(
            self.window, text="Name of Customer to be removed:  ", font=self.text_font)
        customer_list = tk.OptionMenu(self.window, self.selected_customer, *customers)

        cname_label.grid(row=0, column=0, padx=25, pady=20)
        customer_list.grid(row=0, column=1, pady=20, columnspan=2)

        ok_btn = tk.Button(self.window, text="OK", command=self.ok)
        cancel_btn = tk.Button(self.window, text="Cancel", command=self.window.destroy)

        ok_btn.grid(row=5, column=1, pady=35, padx=30)
        cancel_btn.grid(row=5, column=2, pady=20)

    def ok(self):
        self.con.crs.execute(f'DELETE FROM customers WHERE Cname = "{self.selected_customer.get()}";')
        self.con.commit()
        self.window.destroy()
        self.master.refresh_btns()

##############################################################################################################################

class ViewDatabaseBtn(MainButton):
    def __init__(self, con, x, y, **kwargs):
        super().__init__(con, x, y, **kwargs)

    def callback(self):
        self.window = tk.Toplevel()
        self.window.geometry("1360x650")
        self.window.title("View Database")
        self.window.resizable(0, 0)
        self.window.grab_set()

        product_frame = tk.Frame(self.window, bg="lightgray", highlightthickness=3, highlightbackground="black")
        product_frame.place(relwidth=0.6, relheight=1)

        self.product_database_frame = tk.Frame(self.window, bg="lightgray", highlightthickness=3, highlightbackground="black")
        self.product_database_frame.place(relwidth=0.6, relheight=0.83, rely=0.18)

        product_title = tk.Label(product_frame, text="PRODUCTS", font=Font( family="system", size=16), bg="lightgray")
        product_title.grid(row=0, column=0, columnspan=6, pady=20)

        product_search_label = tk.Label( product_frame, text="Search:", font=self.text_font, bg="lightgray")
        product_search_label.grid(row=1, column=0, padx=15)

        product_search_box = tk.Entry(product_frame, width=80, bd=3)
        product_search_box.grid(row=1, column=1, columnspan=5)

        customer_frame = tk.Frame( self.window, bg="white", highlightthickness=3, highlightbackground="black")
        customer_frame.place(relwidth=0.4, relheight=1, relx=0.6)

        self.customer_database_frame = tk.Frame( self.window, bg="white", highlightthickness=3, highlightbackground="black")
        self.customer_database_frame.place( relwidth=0.4, relheight=0.83, rely=0.18, relx=0.6)

        customer_title = tk.Label(customer_frame, text="CUSTOMERS", font=Font(family="system", size=16), bg="white")
        customer_title.grid(row=0, column=0, columnspan=3, pady=20, padx=190)

        customer_search_box = tk.Entry(customer_frame, width=40, bd=3)
        customer_search_box.grid(row=1, column=0, columnspan=3, padx=40)

        product_search_box.bind("<KeyRelease>", self.product_key_up)
        customer_search_box.bind("<KeyRelease>", self.customer_key_up)

        self.draw_product_fields(self.product_database_frame)
        self.draw_customer_fields(self.customer_database_frame)

        self.con.crs.execute("SELECT * FROM products ORDER BY gameid;")
        info = self.con.crs.fetchall()
        database = []
        for i in info:
            database.append(i)

        self.draw_products(self.product_database_frame, database)


        self.con.crs.execute("SELECT * FROM customers;")

        info = self.con.crs.fetchall()
        database = []
        for row in info:
            database.append(row)

        self.draw_customers(self.customer_database_frame, database)


    def draw_product_fields(self, frame):
        attributes = ["Game Id", "Game Name", 'Platform', "Price", "Genre", "Quantity"]

        for attr in attributes:
            heading = tk.Label(frame, text=attr, bg="lightgray", font="system 13 bold")
            heading.grid(row=2, column=attributes.index(attr), padx=2, pady=20)

    def draw_customer_fields(self, frame):
        attributes = ["Game Name", "Customer Name", "Quantity"]

        for attr in attributes:
            heading = tk.Label(frame, text=attr, bg="white", font="system 13 bold")
            heading.grid(row=2, column=attributes.index( attr), padx=2, pady=20)
    
    def draw_products(self, frame, database):
        for game in database:
            for detail in game:
                game_detail = tk.Label(frame, text=detail, bg="lightgray", font="system 11 normal")
                game_detail.grid(row=database.index(game) + 3, column=game.index(detail), padx=15, pady=7)

    def draw_customers(self, frame, database):
        for customer in database:
            for detail in customer:
                c_detail = tk.Label(frame, text=detail, bg="white", font="system 11 normal")
                c_detail.grid(row=database.index(customer)+3, column=customer.index(detail), padx=30, pady=7)

    def product_key_up(self, e):
        search = e.widget.get()

        self.product_database_frame.destroy()

        srch_product_database_frame = tk.Frame(self.window, bg="lightgray", highlightthickness=3, highlightbackground="black")
        srch_product_database_frame.place( relwidth=0.6, relheight=0.83, rely=0.18)

        self.draw_product_fields(srch_product_database_frame)

        self.con.crs.execute(f'SELECT * FROM products WHERE LOWER(Gamename) LIKE "%{search.lower()}%";')

        search_info = self.con.crs.fetchall()
        search_database = []
        for i in search_info:
            search_database.append(i)

        self.draw_products(srch_product_database_frame, search_database)
    
    def customer_key_up(self, e):
        search = e.widget.get()
        self.customer_database_frame.destroy()

        srch_customer_database_frame = tk.Frame(self.window, bg="white", highlightthickness=3, highlightbackground="black")
        srch_customer_database_frame.place(relwidth=0.4, relheight=0.83, rely=0.18, relx=0.6)

        self.draw_customer_fields(srch_customer_database_frame)

        self.con.crs.execute(f'SELECT * FROM customers WHERE LOWER(Cname) LIKE "%{search.lower()}%";')

        search_info = self.con.crs.fetchall()
        search_database = []
        for i in search_info:
            search_database.append(i)

        self.draw_customers(srch_customer_database_frame, search_database)




