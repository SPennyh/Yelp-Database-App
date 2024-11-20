import pyodbc
from customtkinter import *

class yelp_gui(CTk):

    def __init__(self, *args, **kwargs):

        CTk.__init__(self, *args, **kwargs)
        self.geometry('1280x720')

        container = CTkFrame(self)
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (loginPage, mainPage):

            frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with 
			# for loop
            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew")

            self.show_frame(loginPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class loginPage(CTkFrame):
    def __init__(self, parent, controller): 
        CTkFrame.__init__(self, parent)
        
        button = CTkButton(self, text="Login", command = lambda : controller.show_frame(mainPage))
        button.place(relx=0.5, rely=0.6, anchor=CENTER)

        user_box = CTkEntry(self, placeholder_text="uid")
        pwd_box = CTkEntry(self, placeholder_text="password")
        user_box.place(relx=0.5, rely=0.45, anchor=CENTER)
        pwd_box.place(relx=0.5, rely=0.5, anchor=CENTER)

        

class mainPage(CTkFrame):
    def __init__(self, parent, controller): 
        CTkFrame.__init__(self, parent)
        
        button = CTkButton(self, text="Main", command = lambda : controller.show_frame(loginPage))
        button.place(relx=0.5, rely=0.5, anchor=CENTER)

# class searchBusiness():

# class searchUsers():

# class makeFriend():

# class reviewBusiness():


# conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_sdh13;pwd=7eFr4EfA3bATTLn7;Encrypt=yes;TrustServerCertificate=yes')

# cursor = conn.cursor()

# cursor.execute('SELECT TOP(10) * FROM dbo.User_yelp')

# ## Iterate through the returned rows
# for row in cursor:
#     print('row:', row)


gui = yelp_gui()
gui.mainloop()

# conn.close()

