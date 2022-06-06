import tkinter as tk
from tkinter import Tk, ttk, E, W, N, S, END

from colorama import colorama_text
import PasswordGenerator as pg

window_main_menu = Tk()
window_main_menu.title('Library')


class Member:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def signup(self):
        with open('users.txt', 'r') as reader:
            users_list = reader.readlines()
            for user in users_list:
                assert self.username not in user, 'Username has already taken!'
            
        with open("users.txt", 'a') as f:
            f.write(f"{self.username} {self.password}\n")

    def login(self):
        logged_in = False
        with open("users.txt", 'r') as f:
            while True:
                u = f.readline()
                if (self.username +' '+ self.password) in u:
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
                        user_info_list = user_info.split(' ')
                        if (book_name not in user_info_list) and ((book_name + '\n') not in user_info_list):
                            user_info = user_info.split('\n')[0] + ' ' + book_name + '\n'
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
                    info = user.split(' ')
                elif user == '':
                    break
        return '\n'.join(info[2:])

    def return_book(self, book_name):
        with open("users.txt", 'r') as reader:
            users_list = reader.readlines()
            for user in users_list:
                if self.username in user:
                    index = users_list.index(user)
                    user_info_str = user.split('\n')[0]
                    user_info_list = user_info_str.split(' ')
                    user_info_list.remove(book_name)
                    new_info = ' '.join(user_info_list)
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
                if self.username in user:
                    users_list.remove(user)
                    break

        with open('users.txt', 'w') as writer:
            writer.write(''.join(users_list))

class Book:
    def __init__(self, name=''):
        self.book_name = name

    def list_of_books():
        with open("books.txt", 'r') as f:
            print()
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

def internal_user_menu(user_info):
    window_internal_user_menu = Tk()
    window_internal_user_menu.title('Internal Panel')

    lbl_internal_title = ttk.Label(
        master=window_internal_user_menu,
        text='******* Internal Menu *******',
        font=('Times new roman', 18),
    )
    lbl_user_info = ttk.Label(
        master=window_internal_user_menu,
        text=f'Hi {user_info}',
        font=('Arial', 12),
    )
    lbl_sharp_books = ttk.Label(
        master=window_internal_user_menu,
        text='Books with # sign are not available!',
        font=('Arial', 10),
    )
    books_str = Book.list_of_books()
    books_str = 'List of books:\n'+books_str
    lbl_list_of_books = ttk.Label(
        master=window_internal_user_menu,
        text=books_str,
        font=('Arial', 12),
    )
    member = Member(user_info)
    user_books = member.my_books()
    lbl_user_books = ttk.Label(
        master=window_internal_user_menu,
        text=f'{user_info} books:\n{user_books}',
        font=('Arial', 12),
    )
    ent_book = ttk.Entry(
        master=window_internal_user_menu,
    )

    def borrowing_book():
        book_name = ent_book.get()
        lbl_error = ttk.Label(
            master=window_internal_user_menu,
            font=('Arial', 11)
        )
        if book_name == '':
            lbl_error['text'] = 'Input empty!'
            lbl_error.config(foreground='red')
            lbl_error.grid(
                row=5,
                column=0,
                sticky=(W,)
            )
        else:
            try:
                member = Member(user_info)
                member.borrow( book_name)
            except AssertionError:
                lbl_error['text'] = f'{book_name} is not available'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0
                )
            else:
                lbl_error['text'] = f'{book_name} successfully added'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0,
                    sticky=(W,),
                    padx=3
                )

                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                lbl_list_of_books['text'] = books_str
                lbl_list_of_books.grid(
                    row=6,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

                user_books = member.my_books()
                user_books = f'{user_info}\n'+user_books
                lbl_user_books['text'] = user_books
                lbl_user_books.grid(
                    row=6,
                    column=1,
                    padx=5,
                    pady=5,
                    sticky=(N,),
                )

    btn_borrow = ttk.Button(
        master=window_internal_user_menu,
        text='Borrow',
        width=15,
        command=borrowing_book
    )

    def returning_book():
        book_name = ent_book.get()
        lbl_error = ttk.Label(
            master=window_internal_user_menu,
            font=('Arial', 11)
        )
        if book_name == '':
            lbl_error['text'] = 'Input empty!'
            lbl_error.config(foreground='red')
            lbl_error.grid(
                row=5,
                column=0,
                sticky=(W,)
            )
        else:
            try:
                member = Member(user_info)
                member.return_book(book_name)
            except Exception as e:
                lbl_error['text'] = e
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0
                )
            else:
                lbl_error['text'] = f'{book_name} successfully returned'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0,
                    sticky=(W,),
                    padx=3
                )

                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                lbl_list_of_books['text'] = books_str
                lbl_list_of_books.grid(
                    row=6,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

                user_books = member.my_books()
                user_books = f'{user_info} books:\n'+user_books
                lbl_user_books['text'] = user_books
                lbl_user_books.grid(
                    row=6,
                    column=1,
                    padx=5,
                    pady=5,
                    sticky=(N,),
                )

    btn_return = ttk.Button(
        master=window_internal_user_menu,
        text='Return',
        width=15,
        command=returning_book
    )

    lbl_internal_title.grid(
        row=0,
        column=0,
        columnspan=4,
        pady=10,
        padx=3,
        sticky=(W,),
    )
    lbl_user_info.grid(
        row=1,
        column=0,
        sticky=(W,),
        padx=3
    )
    lbl_sharp_books.grid(
        row=2,
        column=0,
        pady=10,
    )
    ent_book.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(E,W),
        padx=3,
    )
    btn_borrow.grid(
        row=4,
        column=0,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    btn_return.grid(
        row=4,
        column=1,
        pady=(5,),
        sticky=(E,),
    )
    lbl_list_of_books.grid(
        row=6,
        column=0,
        pady=5,
        padx=5,
        sticky=(W,),
    )
    lbl_user_books.grid(
        row=6,
        column=1,
        padx=5,
        pady=5,
        sticky=(N,),
    )

def login():
    """Login window"""
    window_login = Tk()
    window_login.title('Login Panel')

    lbl_login_title = ttk.Label(
        master=window_login,
        text='****** Login ******',
        font=('Times new roman', 18)
    )
    lbl_username = ttk.Label(
        master=window_login,
        text='Username',
    )
    ent_username = ttk.Entry(
        master=window_login,
    )
    lbl_password = ttk.Label(
        master=window_login,
        text='Password',
    )
    ent_password = ttk.Entry(
        master=window_login,
        show='*'
    )

    def login_button(*args):
        username = ent_username.get()
        password = ent_password.get()
        user = Member(username, password)

        lbl_error = ttk.Label(
            master=window_login,
            font=('Arial', 9)
        )
        lbl_error.config(foreground='red')

        if username == '' or password == '':
            lbl_error['text'] = 'Input empty!'
            lbl_error.grid(
                row=4,
                column=0,
                columnspan=2,
            )

        elif username.isdigit():
            lbl_error['text'] = "Username can't be a number!"
            lbl_error.grid(
                row=4,
                column=0,
                columnspan=2,
            )

        else:
            user = Member(username, password)
            
            try:
                user_info = user.login()

            except FileNotFoundError:
                lbl_error['text'] = '"users.txt" file not found!'
                lbl_error.grid(
                    row=4,
                    column=0,
                    columnspan=2,
                )

            except AssertionError:
                lbl_error['text'] = 'Username or password is wrong!'
                lbl_error.grid(
                    row=4,
                    column=0,
                    columnspan=2,
                )

            else:
                lbl_error['text'] = 'Logged in successfully'
                lbl_error.grid(
                    row=4,
                    column=0,
                    columnspan=2,
                )
                internal_user_menu(user_info)

    window_login.bind('<Return>', login_button)
    btn_login = ttk.Button(
        master=window_login,
        text='Login',
        width=20,
        command=login_button
    )

    """Display all here"""
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
    )
    btn_login.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(W,E)
    )

def signup():
    """Signup window"""
    window_signup = Tk()
    window_signup.title('Signup Panel')

    """Creating signup window labels and buttons"""
    lbl_signup_title = ttk.Label(
        master=window_signup,
        text='************** Signup **************',
        font=('Times new roman', 18)
    )
    lbl_username = ttk.Label(
        master=window_signup,
        text='Username',
    )
    ent_username = ttk.Entry(
        master=window_signup,
    )
    lbl_password = ttk.Label(
        master=window_signup,
        text='Password',
    )
    ent_password = ttk.Entry(
        master=window_signup,
    )
    def suggest_password():
        suggested_password = pg.generate()
        ent_password.delete(0, END)
        ent_password.insert(0, suggested_password)
    btn_suggest_password = ttk.Button(
        master=window_signup,
        text='Suggest Password',
        width=25,
        command=suggest_password,
    )
    def save_new_user():
        new_username = ent_username.get()
        new_password = ent_password.get()

        if new_username == '' or new_password == '':
            lbl_error = ttk.Label(
                master=window_signup,
                text="Input empty!"
            )
            lbl_error.grid(
                row=4,
                column=1
            )

        elif new_username.isdigit():
            lbl_error = ttk.Label(
                master=window_signup,
                text="Username can't be a number!"
            )
            lbl_error.grid(
                row=4,
                column=1
            )

        else:
            new_user = Member(new_username, new_password)
            
            try:
                new_user.signup()

            except FileNotFoundError:
                lbl_error = ttk.Label(
                    master=window_signup,
                    text='"users.txt" file not found!'
                )
                lbl_error.grid(
                    row=4,
                    column=1
                )

            except AssertionError:
                lbl_error = ttk.Label(
                    master=window_signup,
                    text='Username has already taken!'
                )
                lbl_error.grid(
                    row=4,
                    column=1
                )

            else:
                lbl_error = ttk.Label(
                    master=window_signup,
                    text='Signed up successfully'
                )
                lbl_error.grid(
                    row=4,
                    column=1
                )

    window_signup.bind('<Return>', save_new_user)
    btn_submit = ttk.Button(
        master=window_signup,
        text='Submit',
        width=20,
        command=save_new_user
    )

    """Display all here"""
    lbl_signup_title.grid(
        row=0,
        column=0,
        columnspan=4,
        pady=10,
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
    )
    btn_suggest_password.grid(
        row=2,
        column=2,
        padx=4,
    )
    btn_submit.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(W,E)
    )

    window_signup.mainloop()

def admin_menu():
    window_admin_menu = Tk()
    window_admin_menu.title('Admin')

    lbl_admin_menu_title = ttk.Label(
        master=window_admin_menu,
        text='***** Admin Menu *****',
        font=('Times new roman', 18),
    )

    def adding_book():
        book_name = ent_book.get()
        lbl_error = ttk.Label(
            master=window_admin_menu,
            font=('Arial', 11)
        )
        if book_name == '':
            lbl_error['text'] = 'Input empty!'
            lbl_error.config(foreground='red')
            lbl_error.grid(
                row=5,
                column=0,
                sticky=(W,)
            )
        else:
            try:
                book = Book(book_name)
                book.add()
            except FileNotFoundError:
                lbl_error['text'] = '"Books.txt" file not found!'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0
                )
            except AssertionError:
                lbl_error['text'] = f'{book_name} already exist!'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0
                )

            else:
                lbl_error['text'] = f'{book_name} successfully added'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0,
                    sticky=(W,),
                    padx=3
                )

                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                lbl_list_of_books['text'] = books_str
                lbl_list_of_books.grid(
                    row=6,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

    btn_add_book = ttk.Button(
        master= window_admin_menu,
        text= 'Add Book',
        width=16,
        command=adding_book
    )

    def removing_book():
        book_name = ent_book.get()
        lbl_error = ttk.Label(
            master=window_admin_menu,
            font=('Arial', 11)
        )
        if book_name == '':
            lbl_error['text'] = 'Input empty!'
            lbl_error.config(foreground='red')
            lbl_error.grid(
                row=5,
                column=0,
                sticky=(W,)
            )
        else:
            try:
                book = Book(book_name)
                book.remove()
            except FileNotFoundError:
                lbl_error['text'] = '"Books.txt" file not found!'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0
                )
            except ValueError:
                book = Book('#'+book_name)
                lbl_error['text'] = f'{book_name} does not exist or is borrowed!'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0,
                    sticky=(W,),
                    padx=3
                )

            else:
                lbl_error['text'] = f'{book_name} successfully removed'
                lbl_error.config(foreground='red')
                lbl_error.grid(
                    row=5,
                    column=0,
                    sticky=(W,),
                    padx=3
                )

                books_str = Book.list_of_books()
                books_str = 'List of books:\n'+books_str
                lbl_list_of_books['text'] = books_str
                lbl_list_of_books.grid(
                    row=6,
                    column=0,
                    pady=5,
                    padx=5,
                    sticky=(W,),
                )

    btn_remove_book = ttk.Button(
        master= window_admin_menu,
        text= 'Remove Book',
        width=16,
        command=removing_book,
    )
    ent_book = ttk.Entry(
        master=window_admin_menu,
    )
    try:
        books_str = Book.list_of_books()
        books_str = 'List of books:\n'+books_str
        lbl_list_of_books = ttk.Label(
            master=window_admin_menu,
            text=books_str,
            font=('Arial', 12),
        )
    except FileNotFoundError as e:
        lbl_list_of_books = ttk.Label(
            master=window_admin_menu,
            text=e,
            font=('Arial', 12),
        )



    """Display all here"""

    lbl_admin_menu_title.grid(
        row=0,
        column=0,
        columnspan=4,
        pady=10,
        padx=3,
        sticky=(W,),
    )
    ent_book.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky=(E,W),
        padx=3,
    )
    btn_add_book.grid(
        row=4,
        column=0,
        sticky=(W,),
        padx=3,
        pady=5,
    )
    btn_remove_book.grid(
        row=4,
        column=1,
        pady=(5,),
        sticky=(E,),
    )
    lbl_list_of_books.grid(
        row=6,
        column=0,
        pady=5,
        padx=5,
        sticky=(W,),
    )


    window_admin_menu.mainloop()

def user_menu():
    """User panel"""
    window_user_menu = Tk()
    window_user_menu.title('User Panel')

    """Creating user menu label and buttons"""

    lbl_user_menu_title = ttk.Label(
        master=window_user_menu,
        text='******** User Menu ********',
        font=('Times new roman', 18)

    )
    btn_signup = ttk.Button(
    master= window_user_menu,
    text= 'Signup',
    width=12,
    command=signup
    )
    btn_login = ttk.Button(
        master= window_user_menu,
        text= 'Login',
        width=12,
        command=login,
    )

    """Display all here"""

    lbl_user_menu_title.grid(
    row=0,
    column=0,
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
        row=2,
        column=0,
        padx=3,
        sticky=(W,)
    )

    window_user_menu.mainloop()


"""Creating main menu panel """

lbl_menu_title = ttk.Label(
    master=window_main_menu,
    text='*********** Main Menu ***********',
    font=('Times new roman', 18)
)

# Three buttons are created here
btn_user = ttk.Button(
    master= window_main_menu,
    text= 'User',
    width=12,
    command=user_menu,
)
btn_admin = ttk.Button(
    master= window_main_menu,
    text= 'Admin',
    width=12,
    command=admin_menu,
)
book_img = tk.PhotoImage(file='book.png')
lbl_book_img = ttk.Label(
    master=window_main_menu,
    image=book_img,
)

"""Display all in window_main_menu"""

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
    sticky=(W,N,S)
)
btn_admin.grid(
    row=3,
    column=0,
    padx=3,
    sticky=(W,N,S)
)
lbl_book_img.grid(
    row=1,
    column=1,
    rowspan=3
)


window_main_menu.mainloop()