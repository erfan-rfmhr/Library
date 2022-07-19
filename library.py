from tkinter import Tk, ttk, E, W, N, END, messagebox, PhotoImage, Text
import PasswordGenerator as pg
from os import system, chdir

# ! do not delete the next line
counter = 1

class Member:
    def __init__(self, username='', password='', email=''):
        self.username = username
        self.password = password
        self.email = email

    def signup(self):
        with open('users.txt', 'r') as reader:
            users_list = reader.readlines()
            for user in users_list:
                assert self.username not in user, 'Username has been already taken!'
            
        with open("users.txt", 'a') as writer:
            writer.write(f"{self.username} {self.password} {self.email}\n")

    def login(self):
        logged_in = False
        with open("users.txt", 'r') as reader:
            while True:
                u = reader.readline()
                if (self.username in u) and (self.password in u):
                    logged_in = True
                    break
                elif u == '':
                    break
        assert logged_in is True, 'Username or password is wrong!'
        return self.username
        
    def borrow(self, book_name):
        with open("books.txt", 'r') as books_file:
            books_list = books_file.read().split('\n')
            assert book_name in books_list, 'Book is not available'
            with open("users.txt", 'r') as users_file:
                while True:
                    user_info = users_file.readline()
                    if self.username in user_info:
                        user_info_list = user_info.split('#')
                        if (book_name not in user_info_list) and ((book_name + '\n') not in user_info_list):
                            user_info = user_info.split('\n')[0] + ' #' + book_name + '\n'
                            with open("users.txt", 'r') as reader:
                                users_list = reader.readlines()
                                for i, u in enumerate(users_list):
                                    if self.username in u:
                                        users_list[i] = user_info

                                with open("users.txt", 'w') as writer:
                                    writer.write(''.join(users_list))

                            with open("books.txt", 'w') as writer:
                                index = books_list.index(book_name)
                                books_list[index] = '#'+book_name
                                writer.write('\n'.join(books_list))
                            break
                        break

    def my_books(self):
        with open("users.txt", 'r') as reader:
            while True:
                user = reader.readline()
                if self.username in user:
                    info = user.split(' #')
                elif user == '':
                    break
        return '\n'.join(info[1:])

    def return_book(self, book_name):
        with open("users.txt", 'r') as reader:
            users_list = reader.readlines()
            for user in users_list:
                if self.username in user:
                    index = users_list.index(user)
                    user_info_str = user.split('\n')[0]
                    user_info_list = user_info_str.split(' #')
                    user_info_list.remove(book_name)
                    new_info = ' #'.join(user_info_list)
                    users_list[index] = new_info + '\n'
                    break
        with open("users.txt", 'w') as writer:
            writer.write(''.join(users_list))

        with open("books.txt", 'r') as reader:
            books_list = reader.readlines()
            for book in books_list:
                if book_name in book:
                    index = books_list.index(book)
                    returned_book_list = book.split('#')
                    returned_book_str = ''.join(returned_book_list)
                    books_list[index] = returned_book_str
                    break
        with open("books.txt", 'w') as writer:
            writer.write(''.join(books_list))

    def delete_account(self):
        with open('users.txt', 'r') as reader:
            users_list = reader.readlines()
            for user in users_list:
                exist_ac = False
                if self.username in user:
                    exist_ac = True
                    assert (self.password in user) and ('#' not in user), 'Make sure the password is correct or you\'ve already returned all of your books.'
                    users_list.remove(user)
                    break
            assert exist_ac == True, 'Wrong username!'

        with open('users.txt', 'w') as writer:
            writer.write(''.join(users_list))

class Book:
    def __init__(self, name=''):
        self.book_name = name

    @staticmethod
    def list_of_books():
        with open("books.txt", 'r') as f:
            return f.read()

    def add(self):
        with open('books.txt', 'r') as reader:
            all_books = reader.read()
            assert self.book_name not in all_books, f'{self.book_name} already exist!'
            with open("books.txt", 'a') as f:
                f.write(f"{self.book_name}\n")

    def remove(self):
        with open("books.txt", 'r') as f:
            all_books = f.readlines()
            all_books.remove(self.book_name+'\n')
        with open("books.txt", 'w') as f:
            f.writelines(all_books)

def main_menu(other_window):
    other_window.destroy()
    """Creating main menu panel """
    window_main_menu = Tk()
    window_main_menu.title('Library')
    window_main_menu.config(background='#88AB75')
    window_main_menu.bind('<Escape>', lambda *args: window_main_menu.destroy())

    lbl_menu_title = ttk.Label(
        master=window_main_menu,
        text='******* Main Menu *******',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )

    # Three buttons are created here
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')]) 

    btn_user = ttk.Button(
        master= window_main_menu,
        text= 'User',
        width=12,
        command=lambda: user_menu(window_main_menu),
    )

    btn_admin = ttk.Button(
        master= window_main_menu,
        text= 'Admin',
        width=12,
        command=lambda: admin_menu(window_main_menu),
    )
    book_img = PhotoImage(file='book.png')
    lbl_book_img = ttk.Label(
        master=window_main_menu,
        image=book_img,
    )

    # Display all in window_main_menu

    lbl_menu_title.grid(
        row=0,
        column=0,
        columnspan=3,
        pady=10
    )
    btn_user.grid(
        row=1,
        column=0,
        pady=(5,),
        padx=3,
    )
    btn_admin.grid(
        row=1,
        column=1,
        padx=3,
    )
    lbl_book_img.grid(
        row=2,
        column=0,
        columnspan=2,
        rowspan=3,
    )

    window_main_menu.mainloop()

def internal_user_menu(user_info, other_window):
    other_window.destroy()
    window_internal_user_menu = Tk()
    window_internal_user_menu.title('Internal Panel')
    window_internal_user_menu.config(background='#88AB75')

    lbl_internal_title = ttk.Label(
        master=window_internal_user_menu,
        text='*************** Internal Menu ***************',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )
    lbl_user_info = ttk.Label(
        master=window_internal_user_menu,
        text=f'Hi {user_info}',
        font=('Arial', 12),
        background='#342E37',
        foreground='white',
    )
    lbl_sharp_books = ttk.Label(
        master=window_internal_user_menu,
        text='Books with # sign are not available!',
        font=('Arial', 10),
        background='#342E37',
        foreground='white',
    )
    lbl_lib_books = ttk.Label(
        master=window_internal_user_menu,
        text='List of books',
        font=('Times new roman', 15),
        background='#88AB75',
    )
    books_str = Book.list_of_books()
    txt_list_of_books = Text(
        master=window_internal_user_menu,
        height=5,
        width=18,
        font=('Arial', 12),
    )
    txt_list_of_books.insert(1.0, books_str)

    lbl_user_books = ttk.Label(
        master=window_internal_user_menu,
        text=f'{user_info} books',
        font=('Times new roman', 15),
        background='#88AB75',
    )
    member = Member(user_info)
    user_books = member.my_books()
    txt_user_books = Text(
        master=window_internal_user_menu,
        height=5,
        width=18,
        font=('Arial', 12),
    )
    txt_user_books.insert(1.0, user_books)


    ent_book = ttk.Entry(
        master=window_internal_user_menu,
        justify='center',
        font=('Arial', 14),
    )

    def borrowing_book():
        book_name = ent_book.get()
        if book_name == '':
            messagebox.showwarning('Input empty', 'Please fill the box')
        else:
            try:
                member = Member(user_info)
                member.borrow( book_name)
            except AssertionError:
                messagebox.showerror('Result', f'{book_name} is not available')
            else:
                messagebox.showinfo('Result', f'{book_name} is successfully added')
                books_str = Book.list_of_books()
                txt_list_of_books.grid(
                    row=5,
                    rowspan=4,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

                txt_list_of_books.delete(1.0, END)
                txt_list_of_books.insert(1.0, books_str)

                user_books = member.my_books()
                txt_user_books.grid(
                    row=5,
                    rowspan=4,
                    column=2,
                    padx=5,
                    pady=5,
                    sticky=(N,),
                )
                txt_user_books.delete(1.0, END)
                txt_user_books.insert(1.0, user_books)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.configure('TButton', font=('Helvetica', 12))
    style.map('TButton', background=[('active','red')],) 

    btn_borrow = ttk.Button(
        master=window_internal_user_menu,
        text='Borrow',
        width=15,
        command=borrowing_book
    )

    def returning_book():
        book_name = ent_book.get()
        if book_name == '':
            messagebox.showwarning('Input empty', 'Please fill the box')
        else:
            try:
                member = Member(user_info)
                member.return_book(book_name)
            except Exception as e:
                messagebox.showerror('Error', e)
            else:
                messagebox.showinfo('Result', f'{book_name} is successfully returned')

                books_str = Book.list_of_books()
                txt_list_of_books.grid(
                    row=5,
                    rowspan=4,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )
                txt_list_of_books.delete(1.0, END)
                txt_list_of_books.insert(1.0, books_str)

                user_books = member.my_books()
                txt_user_books.grid(
                    row=5,
                    rowspan=4,
                    column=2,
                    padx=5,
                    pady=5,
                    sticky=(N,),
                )
                txt_user_books.delete(1.0, END)
                txt_user_books.insert(1.0, user_books)

    btn_return = ttk.Button(
        master=window_internal_user_menu,
        text='Return',
        width=15,
        command=returning_book
    )

    btn_back = ttk.Button(
        master=window_internal_user_menu,
        text='Back',
        width=15,
        command=lambda: user_menu(window_internal_user_menu)
    )
    window_internal_user_menu.bind('<Escape>', lambda *args: user_menu(window_internal_user_menu))

    lbl_internal_title.grid(
        row=0,
        column=0,
        columnspan=5,
        pady=10,
        padx=3,
        sticky=(W,)
    )
    lbl_user_info.grid(
        row=1,
        column=1,
        pady=2,
    )
    lbl_sharp_books.grid(
        row=2,
        column=0,
        columnspan=3,
        pady=(0,6),
    )
    ent_book.grid(
        row=3,
        column=0,
        columnspan=3,
        sticky=(E,W),
        padx=3,
    )
    btn_borrow.grid(
        row=5,
        column=1,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    btn_return.grid(
        row=6,
        column=1,
        padx=3,
        pady=(5,),
        sticky=(E,),
    )
    btn_back.grid(
        row=7,
        column=1,
        pady=(5,),
    )
    lbl_lib_books.grid(
        row=4,
        column=0,
        pady=5,
        padx=8,
        sticky=(W,),
    )
    txt_list_of_books.grid(
        row=5,
        rowspan=4,
        column=0,
        pady=5,
        padx=5,
        sticky=(W,),
    )
    lbl_user_books.grid(
        row=4,
        column=2,
        padx=5,
        pady=5,
        sticky=(N,),
    )
    txt_user_books.grid(
        row=5,
        rowspan=4,
        column=2,
        padx=5,
        pady=5,
        sticky=(N,),
    )

def login(other_window):
    other_window.destroy()
    """Login window"""
    window_login = Tk()
    window_login.title('Login Panel')
    window_login.config(background='#88AB75')

    lbl_login_title = ttk.Label(
        master=window_login,
        text='******* Login *******',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',

    )
    lbl_username = ttk.Label(
        master=window_login,
        text='Username',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_username = ttk.Entry(
        master=window_login,
        font=('Arial', 12),
    )
    lbl_password = ttk.Label(
        master=window_login,
        text='Password',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_password = ttk.Entry(
        master=window_login,
        font=('Arial', 12),
        show='*',
    )


    def login_button(*args):
        username = ent_username.get()
        password = ent_password.get()
        user = Member(username, password)

        if username == '' or password == '':
            messagebox.showwarning('Input empty', 'Please fill the box')

        elif username.isdigit():
            messagebox.showwarning('Invalid username', "Username can't be a number!")

        else:
            user = Member(username, password)
            
            try:
                user_info = user.login()

            except FileNotFoundError as e:
                messagebox.showerror('Users file', e)
                
            except AssertionError:
                messagebox.showerror('Users file', 'Username or password is wrong!')

            else:
                internal_user_menu(user_info, window_login)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')])

    # ? a better solution ?
    def show_pass():
        global counter
        if counter&1 == 1:
            ent_password.config(show='')
            counter += 1
        else:
            ent_password.config(show='*')
            counter += 1

    btn_reveal_password = ttk.Checkbutton(
        master=window_login,
        text = "Show", 
        onvalue = 1,
        offvalue = 0,
        command=lambda: show_pass(),
    )

    btn_login = ttk.Button(
        master=window_login,
        text='Login',
        width=20,
        command=login_button
    )
    window_login.bind('<Return>', login_button)

    def forgot_password():
        # ! run the exe file in the same directory as library.py is !
        # ? is there any better solution to run this file ?
        chdir('.')
        try:
            system('start RecoverPassword.exe')
        except:
            messagebox.showerror('exe file', 'Make sure that the exe file is  in the same directory as library.py is')

    btn_forgot_password = ttk.Button(
        master=window_login,
        text='Forget Password?',
        width=19,
        command=forgot_password
    )

    btn_back = ttk.Button(
        master=window_login,
        text='Back',
        width=10,
        command=lambda: user_menu(window_login)
    )
    window_login.bind('<Escape>', lambda *args: user_menu(window_login))

    # Display all here
    lbl_login_title.grid(
        row=0,
        column=0,
        columnspan=6,
        pady=(10,),
        padx=3,
        sticky=(W,)
    )
    lbl_username.grid(
        row=1,
        column=0,
        sticky=(W,),
        padx=3,
    )
    ent_username.grid(
        row=1,
        column=1,
        ipady=1,
        ipadx=1,
        padx=3,
    )
    lbl_password.grid(
        row=2,
        column=0,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    ent_password.grid(
        row=2,
        column=1,
        ipady=1,
        ipadx=1,
        pady=5,
        padx=3,
    )
    btn_reveal_password.grid(
        row=2,
        column=2,
        padx=4,
    )
    btn_login.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(W,E),
        ipady=3,
    )
    btn_forgot_password.grid(
        row=4,
        column=1,
        padx=3,
        ipady=3,
    )
    btn_back.grid(
        row=4,
        column=0,
        pady=5,
        ipady=3,
    )

def signup(other_window):
    """Signup panel"""
    other_window.destroy()
    window_signup = Tk()
    window_signup.title('Signup Panel')
    window_signup.config(background='#88AB75')

    # Creating signup window labels and buttons
    lbl_signup_title = ttk.Label(
        master=window_signup,
        text='************** Sign Up **************',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )
    lbl_username = ttk.Label(
        master=window_signup,
        text='Username',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_username = ttk.Entry(
        master=window_signup,
        font=('Arial', 12),
    )

    # ? a better solution ?
    def show_pass():
        global counter
        if counter&1 == 1:
            ent_password.config(show='')
            counter += 1
        else:
            ent_password.config(show='*')
            counter += 1

    btn_reveal_password = ttk.Checkbutton(
        master=window_signup,
        text = "Show", 
        onvalue = 1,
        offvalue = 0,
        command=lambda: show_pass(),
    )

    lbl_email = ttk.Label(
        master=window_signup,
        text='Email',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_email = ttk.Entry(
        master=window_signup,
        font=('Arial', 12),
    )
    lbl_password = ttk.Label(
        master=window_signup,
        text='Password',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_password = ttk.Entry(
        master=window_signup,
        font=('Arial', 12),
        show='*',
    )
    def suggest_password():
        suggested_password = pg.generate()
        ent_password.delete(0, END)
        ent_password.insert(0, suggested_password)
    btn_suggest_password = ttk.Button(
        master=window_signup,
        text='Suggest Password',
        width=19,
        command=suggest_password,
    )
    def save_new_user(*args):
        new_username = ent_username.get()
        new_password = ent_password.get()
        new_email = ent_email.get()

        if new_username == '' or new_password == '' or new_email == '':
            messagebox.showwarning('Input Empty', 'Please fill the box')
        elif new_username.isdigit():
            messagebox.showwarning('Invalid Username', 'Username can not be a number')
        elif (new_email.isdigit()) or ('@' not in new_email) or ('gmail' not in new_email) or ('com' not in new_email):
            messagebox.showwarning('Invalid Email', 'Email address must be a gmail account')
        else:
            new_user = Member(new_username, new_password, new_email)
            
            try:
                new_user.signup()
            except FileNotFoundError as e:
                messagebox.showerror('Users file', e)
            except AssertionError:
                messagebox.showwarning('Invalid username', 'Username has been already taken!')
            else:
                messagebox.showinfo('Result', 'Signed up successfully')
                internal_user_menu(new_username, window_signup)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')]) 

    btn_submit = ttk.Button(
        master=window_signup,
        text='Submit',
        width=20,
        command=save_new_user
    )
    window_signup.bind('<Return>', save_new_user)

    btn_back = ttk.Button(
        master=window_signup,
        text='Back',
        width=10,
        command=lambda: user_menu(window_signup)
    )
    window_signup.bind('<Escape>', lambda *args: user_menu(window_signup))


    # Display all here
    lbl_signup_title.grid(
        row=0,
        column=0,
        columnspan=5,
        pady=10,
        padx=3,
    )
    lbl_username.grid(
        row=1,
        column=0,
        sticky=(W,),
        padx=3,
    )
    ent_username.grid(
        row=1,
        column=1,
        ipadx=1,
        ipady=1,
    )
    btn_reveal_password.grid(
        row=3,
        column=2,
        padx=4,
    )
    lbl_email.grid(
        row=2,
        column=0,
        sticky=(W,),
        padx=3,
        pady=(5,0)
    )
    ent_email.grid(
        row=2,
        column=1,
        ipadx=1,
        ipady=1,
        pady=(5,0)
    )
    lbl_password.grid(
        row=3,
        column=0,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    ent_password.grid(
        row=3,
        column=1,
        ipadx=1,
        ipady=1,
        pady=5,
    )
    btn_suggest_password.grid(
        row=3,
        column=3,
        columnspan=2,
        padx=4,
    )
    btn_submit.grid(
        row=4,
        column=0,
        columnspan=2,
        padx=3,
        sticky=(W,E),
    )
    btn_back.grid(
        row=5,
        column=0,
        pady=5
    )

    window_signup.mainloop()

def deleting_account(other_window):
    other_window.destroy()

    # Delete account window

    window_del_account = Tk()
    window_del_account.title('Delete account Panel')
    window_del_account.config(background='#88AB75')

    # Creating signup window labels and buttons

    lbl_del_account_title = ttk.Label(
        master=window_del_account,
        text='******* Delete account *******',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )
    lbl_username = ttk.Label(
        master=window_del_account,
        text='Username',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_username = ttk.Entry(
        master=window_del_account,
        font=('Arial', 12),
    )
    lbl_password = ttk.Label(
        master=window_del_account,
        text='Password',
        background='#88AB75',
        font=('Arial', 12),
    )
    ent_password = ttk.Entry(
        master=window_del_account,
        show='*',
        font=('Arial', 12),
    )

    #create buttons

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')]) 

    def del_btn(*args):
        username = ent_username.get()
        password = ent_password.get()
        user = Member(username, password)

        if username == '' or password == '':
            messagebox.showwarning('Input empty', 'Please fill the box')

        elif username.isdigit():
            messagebox.showwarning('Invalid username', "Username can't be a number!")

        else:
            user = Member(username, password)
            
            try:
                user.delete_account()

            except FileNotFoundError as e:
                messagebox.showerror('Users file', e)
                
            except AssertionError as a:
                messagebox.showerror('Users file', a)

            else:
                messagebox.showinfo('Delete account', f'{username} account is deleted successfully')
                user_menu(window_del_account)

    btn_del_account = ttk.Button(
        master=window_del_account,
        text='Delete',
        command=del_btn
    )
    window_del_account.bind('<Return>', del_btn)

    # ? a better solution ?
    def show_pass():
        global counter
        if counter&1 == 1:
            ent_password.config(show='')
            counter += 1
        else:
            ent_password.config(show='*')
            counter += 1

    btn_reveal_password = ttk.Checkbutton(
        master=window_del_account,
        text = "Show", 
        onvalue = 1,
        offvalue = 0,
        command=lambda: show_pass(),
    )

    btn_back = ttk.Button(
        master=window_del_account,
        text='Back',
        width=10,
        command=lambda: user_menu(window_del_account)
    )
    window_del_account.bind('<Escape>', lambda *args: user_menu(window_del_account))

    # Display all here

    lbl_del_account_title.grid(
        row=0,
        column=0,
        columnspan=6,
        pady=(10,),
        padx=3,
        sticky=(W,)
    )
    btn_reveal_password.grid(
        row=2,
        column=2,
        padx=4,
    )
    lbl_username.grid(
        row=1,
        column=0,
        sticky=(W,),
        padx=3,
    )
    ent_username.grid(
        row=1,
        column=1,
        sticky=(W,E),
    )
    lbl_password.grid(
        row=2,
        column=0,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    ent_password.grid(
        row=2,
        column=1,
        pady=5,
        sticky=(W,E),
    )
    btn_del_account.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(W,E),
        padx=3,
    )
    btn_back.grid(
        row=4,
        column=0,
        pady=5
    )

def admin_menu(other_window):
    other_window.destroy()
    window_admin_menu = Tk()
    window_admin_menu.title('Admin')
    window_admin_menu.config(background='#88AB75')

    lbl_admin_menu_title = ttk.Label(
        master=window_admin_menu,
        text='******* Admin Menu *******',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')]) 

    def adding_book(*args):
        book_name = ent_book.get()
        if book_name == '':
            messagebox.showwarning('Input empty', 'Please fill the box')
        else:
            try:
                book = Book(book_name)
                book.add()
                
            except FileNotFoundError as e:
                messagebox.showwarning('books file', e)

            except AssertionError:
                messagebox.showwarning('book exists', f'{book_name} already exist!')

            else:
                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                txt_list_of_books.delete(1.0, END)
                txt_list_of_books.insert(1.0, books_str)
                txt_list_of_books.grid(
                    row=2,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

    btn_add_book = ttk.Button(
        master= window_admin_menu,
        text= 'Add Book',
        width=15,
        command=adding_book
    )
    window_admin_menu.bind('<Return>', adding_book)

    def removing_book():
        book_name = ent_book.get()
        if book_name == '':
            messagebox.showwarning('Input empty', 'Please fill the box')
        else:
            try:
                book = Book(book_name)
                book.remove()
                
            except FileNotFoundError as e:
                messagebox.showerror('book file', e)

            except ValueError:
                book = Book('#'+book_name)
                messagebox.showwarning('book not found', f'{book_name} does not exist or is borrowed!')

            else:
                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                txt_list_of_books.delete(1.0, END)
                txt_list_of_books.insert(1.0, books_str)
                txt_list_of_books.grid(
                    row=2,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

    btn_remove_book = ttk.Button(
        master= window_admin_menu,
        text= 'Remove Book',
        width=15,
        command=removing_book,
    )
    ent_book = ttk.Entry(
        master=window_admin_menu,
        justify='center',
        font=('Arial', 14),
    )
    btn_back = ttk.Button(
        master= window_admin_menu,
        width=15,
        text= "Back",
        command=lambda: main_menu(window_admin_menu)
    )
    window_admin_menu.bind('<Escape>', lambda *args: main_menu(window_admin_menu))

    try:
        books_str = Book.list_of_books()
        books_str = 'List of books:\n'+books_str
        txt_list_of_books = Text(
            master=window_admin_menu,
            height=10,
            width=18,
            font=('Arial', 12),
        )
        txt_list_of_books.insert(1.0, books_str)
    except FileNotFoundError as e:
        txt_list_of_books = Text(
            master=window_admin_menu,
            height=10,
            width=18,
            font=('Arial', 12),
        )
        txt_list_of_books.insert(1.0, e)

    # Display all here

    lbl_admin_menu_title.grid(
        row=0,
        column=0,
        columnspan=4,
        pady=10,
        padx=3,
        sticky=(W,),
    )
    ent_book.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky=(E,W),
        padx=3,
    )
    btn_add_book.grid(
        row=2,
        column=1,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    btn_remove_book.grid(
        row=3,
        column=1,
        pady=(5,),
        sticky=(E,),
    )
    txt_list_of_books.grid(
        row=2,
        rowspan=7,
        column=0,
        pady=5,
        padx=5,
        sticky=(W,),
    )
    
    btn_back.grid(
        row=4,
        column=1,
        columnspan=2,
        pady=(7,),
        padx=3,
        sticky=(N)
    )

    window_admin_menu.mainloop()

def user_menu(other_window):
    other_window.destroy()
    """User panel"""
    window_user_menu = Tk()
    window_user_menu.title('User Panel')
    window_user_menu.config(background='#88AB75',)

    """Creating user menu label and buttons"""

    lbl_user_menu_title = ttk.Label(
        master=window_user_menu,
        text='******** User Menu ********',
        font=('Times new roman', 18),
        background='#88AB75',
        foreground='black',
    )

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TButton', background = '#342E37', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','red')]) 

    btn_signup = ttk.Button(
        master= window_user_menu,
        text= 'Signup',
        width=15,
        command=lambda: signup(window_user_menu),
    )
    btn_login = ttk.Button(
        master= window_user_menu,
        text= 'Login',
        width=15,
        command=lambda: login(window_user_menu),
    )
    btn_back = ttk.Button(
        master= window_user_menu,
        width=15,
        text= "Back",
        command=lambda: main_menu(window_user_menu)
    )
    window_user_menu.bind('<Escape>', lambda *args: main_menu(window_user_menu))

    btn_delete_account = ttk.Button(
        master=window_user_menu,
        text='Delete account',
        width=15,
        command=lambda: deleting_account(window_user_menu)
    )

    """Display all here"""

    lbl_user_menu_title.grid(
        row=0,
        column=0,
        columnspan=3,
        pady=(10,),
        padx=3,
    )
    btn_signup.grid(
        row=1,
        column=0,
        pady=(7,),
        padx=3,
        sticky=(W,)
    )
    btn_login.grid(
        row=1,
        column=1,
        padx=3,
        sticky=(W,)
    )
    btn_delete_account.grid(
        row=2,
        column=0,
        pady=(7,),
        padx=3,
        sticky=(W,)
    )
    btn_back.grid(
        row=2,
        column=1,
        padx=3,
        sticky=(W,)
    )
    window_user_menu.mainloop()

x = Tk()
main_menu(x)
