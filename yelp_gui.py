import pyodbc
from customtkinter import *
import passwords


def check_user_id(entry, parent, controller):
    user_id = entry.get()
    try:
        # Example connection; replace with your actual database connection
        connection = pyodbc.connect(f"driver={{ODBC Driver 18 for SQL Server}};server=cypress.csil.sfu.ca;uid=s_sdh13;pwd={passwords.pwd};Encrypt=yes;TrustServerCertificate=yes")
        cursor = connection.cursor()

        # Use parameterized query to avoid SQL injection
        cursor.execute("SELECT * FROM dbo.helpdesk WHERE username = ?", user_id)
        result = cursor.fetchone()

        if result:
            controller.show_frame(mainPage)  # Show mainPage if user exists
        else:
            raise ValueError("Invalid User ID")
    except (pyodbc.Error, ValueError) as ex:
        error_message = str(ex)
        textbox = CTkTextbox(master=parent, width=200, height=50, corner_radius=5)
        textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
        textbox.insert("0.0", f"Error: {error_message}")
    finally:
        cursor.close()
        connection.close()

def load_buttons(self, controller):
        button_border = CTkFrame(self, width=178, height=640, fg_color='#525252')
        button_border.place(x=31, y=40)

        logout_button = CTkButton(button_border, text="Logout", font=('arial bold',12), fg_color='#828AFF', corner_radius=15, text_color='black', command=lambda: controller.show_frame(loginPage))
        logout_button.place(x=22, y=581)

        business_button = CTkButton(button_border, text="Search Businesses", font=('arial bold',12), fg_color='#828AFF', corner_radius=15, text_color='black',command=lambda: controller.show_frame(searchBusiness))
        business_button.place(x=22, y=22.42)

        user_button = CTkButton(button_border, text="Search Users", font=('arial bold',12), fg_color='#828AFF', corner_radius=15, text_color='black',command=lambda: controller.show_frame(searchUsers))
        user_button.place(x=22, y=76.43)

class yelp_gui(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)
        self.geometry('1280x720')

        container = CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (loginPage, mainPage, searchBusiness, searchUsers, makeFriend, reviewBusiness):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(loginPage)

    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if frame:
            frame.tkraise()


class loginPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        title = CTkLabel(self, text="Yelp Database", font=('arial bold',40), text_color='#828AFF')
        title.place(x=514, y=141)

        entry_border = CTkFrame(self, width=300, height=143, fg_color='#525252')
        entry_border.place(x=490, y=310)

        user_title = CTkLabel(entry_border, text="User ID", font=('arial', 12), text_color='#828AFF')
        user_title.place(x=22, y=19)

        user_box = CTkEntry(entry_border, placeholder_text="Enter your User ID", width=256, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        user_box.place(x=22, y=41)

        button = CTkButton(
            entry_border,
            text="Sign in",
            font=('arial bold', 12),
            command=lambda: check_user_id(user_box, self, controller), fg_color='#828AFF', corner_radius=5, width=256, height=31
        )
        button.place(x=22, y=84)


class mainPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=233, y=40)

        user_title = CTkLabel(entry_border, text="Yelp Database", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        load_buttons(self, controller)

class searchBusiness(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=233, y=40)

        user_title = CTkLabel(entry_border, text="Yelp Database - Search for a Business", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        load_buttons(self, controller)

        slider = CTkSlider(self, from_=0, to=5, number_of_steps=5)
        slider.place(relx=0.3, rely=0.3, anchor=CENTER)

class searchUsers(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=233, y=40)

        user_title = CTkLabel(entry_border, text="Yelp Database - Search for Users", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        load_buttons(self, controller)

class makeFriend(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        load_buttons(self, controller)

class reviewBusiness(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        load_buttons(self, controller)


# cursor.execute('SELECT TOP(10) * FROM dbo.User_yelp')

# ## Iterate through the returned rows
# for row in cursor:
#     print('row:', row)

gui = yelp_gui()
gui.mainloop()

# conn.close()

