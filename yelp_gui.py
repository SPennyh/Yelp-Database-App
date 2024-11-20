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
        textbox = CTkTextbox(master=parent, width=100, corner_radius=0)
        textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
        textbox.insert("0.0", f"Error: {error_message}")
    finally:
        cursor.close()
        connection.close()


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

        user_box = CTkEntry(self, placeholder_text="uid")
        user_box.place(relx=0.5, rely=0.45, anchor=CENTER)

        button = CTkButton(
            self,
            text="Login",
            command=lambda: check_user_id(user_box, self, controller)
        )
        button.place(relx=0.5, rely=0.6, anchor=CENTER)


class mainPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        logout_button = CTkButton(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logout_button.place(relx=0.9, rely=0.9, anchor=CENTER)

        business_button = CTkButton(self, text="Search Businesses", command=lambda: controller.show_frame(searchBusiness))
        business_button.place(relx=0.1, rely=0.1, anchor=CENTER)

        user_button = CTkButton(self, text="Search Users", command=lambda: controller.show_frame(searchUsers))
        user_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        friend_button = CTkButton(self, text="Make a Friend", command=lambda: controller.show_frame(makeFriend))
        friend_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        review_button = CTkButton(self, text="Review a Business", command=lambda: controller.show_frame(reviewBusiness))
        review_button.place(relx=0.7, rely=0.1, anchor=CENTER)

class searchBusiness(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        logout_button = CTkButton(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logout_button.place(relx=0.9, rely=0.9, anchor=CENTER)

        business_button = CTkButton(self, text="Search Businesses", command=lambda: controller.show_frame(searchBusiness))
        business_button.place(relx=0.1, rely=0.1, anchor=CENTER)

        user_button = CTkButton(self, text="Search Users", command=lambda: controller.show_frame(searchUsers))
        user_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        friend_button = CTkButton(self, text="Make a Friend", command=lambda: controller.show_frame(makeFriend))
        friend_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        review_button = CTkButton(self, text="Review a Business", command=lambda: controller.show_frame(reviewBusiness))
        review_button.place(relx=0.7, rely=0.1, anchor=CENTER)

class searchUsers(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        logout_button = CTkButton(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logout_button.place(relx=0.9, rely=0.9, anchor=CENTER)

        business_button = CTkButton(self, text="Search Businesses", command=lambda: controller.show_frame(searchBusiness))
        business_button.place(relx=0.1, rely=0.1, anchor=CENTER)

        user_button = CTkButton(self, text="Search Users", command=lambda: controller.show_frame(searchUsers))
        user_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        friend_button = CTkButton(self, text="Make a Friend", command=lambda: controller.show_frame(makeFriend))
        friend_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        review_button = CTkButton(self, text="Review a Business", command=lambda: controller.show_frame(reviewBusiness))
        review_button.place(relx=0.7, rely=0.1, anchor=CENTER)

class makeFriend(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        logout_button = CTkButton(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logout_button.place(relx=0.9, rely=0.9, anchor=CENTER)

        business_button = CTkButton(self, text="Search Businesses", command=lambda: controller.show_frame(searchBusiness))
        business_button.place(relx=0.1, rely=0.1, anchor=CENTER)

        user_button = CTkButton(self, text="Search Users", command=lambda: controller.show_frame(searchUsers))
        user_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        friend_button = CTkButton(self, text="Make a Friend", command=lambda: controller.show_frame(makeFriend))
        friend_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        review_button = CTkButton(self, text="Review a Business", command=lambda: controller.show_frame(reviewBusiness))
        review_button.place(relx=0.7, rely=0.1, anchor=CENTER)

class reviewBusiness(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        logout_button = CTkButton(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logout_button.place(relx=0.9, rely=0.9, anchor=CENTER)

        business_button = CTkButton(self, text="Search Businesses", command=lambda: controller.show_frame(searchBusiness))
        business_button.place(relx=0.1, rely=0.1, anchor=CENTER)

        user_button = CTkButton(self, text="Search Users", command=lambda: controller.show_frame(searchUsers))
        user_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        friend_button = CTkButton(self, text="Make a Friend", command=lambda: controller.show_frame(makeFriend))
        friend_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        review_button = CTkButton(self, text="Review a Business", command=lambda: controller.show_frame(reviewBusiness))
        review_button.place(relx=0.7, rely=0.1, anchor=CENTER)


# cursor.execute('SELECT TOP(10) * FROM dbo.User_yelp')

# ## Iterate through the returned rows
# for row in cursor:
#     print('row:', row)

# conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_sdh13;pwd=7eFr4EfA3bATTLn7;Encrypt=yes;TrustServerCertificate=yes')

# cursor = conn.cursor()

gui = yelp_gui()
gui.mainloop()

# conn.close()

