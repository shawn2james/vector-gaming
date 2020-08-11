import tkinter as tk
from tkinter.font import Font
import mysql.connector
from main_window import MainWindow
from connection import Connection


class PasswordWindow(tk.Tk):
    """
    The opening window that asks for the username and password to be used to login to the MySQL server
    - a subclass of tkinter.Toplevel class
    """

    def __init__(self):
        super().__init__()
        # window settings
        self.geometry("500x300")
        self.resizable(0, 0)
        self.title("Enter Password")

        # labels and input boxes
        self.username_label = tk.Label(
            master=self, text="Enter username:",
            font=Font(family="system", size=13))
        self.username_box = tk.Entry(self, width=20)

        self.password_label = tk.Label(
            master=self, text="Enter MySQL Password:",
            font=Font(family="system", size=13))
        self.password_box = tk.Entry(self, show="*", width=20)

        # ok and cancel buttons
        self.ok_btn = tk.Button(self, text="OK", command=self.login_result)
        self.cancel_btn = tk.Button(self, text="Cancel", command=self.cancel)

        # positioning all the labels, input boxes and buttons
        self.username_label.grid(row=0, column=0, padx=20, pady=30)
        self.username_box.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0, padx=20, pady=30)
        self.password_box.grid(row=1, column=1)
        self.ok_btn.grid(row=2, column=2)
        self.cancel_btn.grid(row=2, column=1)

    def login_result(self):
        """
        checks if the given username and password is correct
        """
        password = self.password_box.get()
        username = self.username_box.get()

        try:
            # try connecting to the mysql server with the entered username and password
            con = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password
            )
        except:
            # if password is wrong, display a warning
            wrong_password = tk.Label(
                self, text='Incorrect Password !', fg='red')
            wrong_password.grid(row=2, column=0)
        else:
            # if the password is correct, close the password window and display main window
            con = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password
            )
            self.con = Connection('localhost', username, password)
            self.con.create_database()
            self.con.create_products()
            self.con.create_customers()
            self.destroy()
            self.init_main_window()

    def cancel(self):
        """
        callback function for the cancel button
        """
        self.destroy()

    def init_main_window(self):
        main_window = MainWindow(self.con)
        main_window.mainloop()


if __name__ == "__main__":
    password_window = PasswordWindow()
    password_window.mainloop()
