import pyodbc
from tkinter import ttk
from customtkinter import *
import passwords
from datetime import datetime
import uuid
import base64

connection = pyodbc.connect(f"driver={{ODBC Driver 18 for SQL Server}};server=cypress.csil.sfu.ca;uid={passwords.user_name};pwd={passwords.pwd};Encrypt=yes;TrustServerCertificate=yes")
cursor = connection.cursor()

#self explanatory
def load_buttons(self, controller):
        button_border = CTkFrame(self, width=178, height=640, fg_color='#525252')
        button_border.place(x=31, y=40)

        logout_button = CTkButton(button_border, text="Logout", font=('arial bold',12), fg_color='#828AFF', hover_color='#5862E9',
                                  corner_radius=15, text_color='black', command=lambda: controller.show_frame(loginPage))
        logout_button.place(x=22, y=581)

        business_button = CTkButton(button_border, text="Search Businesses", font=('arial bold',12), fg_color='#828AFF', hover_color='#5862E9',
                                    corner_radius=15, text_color='black',command=lambda: controller.show_frame(searchBusiness))
        business_button.place(x=22, y=22.42)

        user_button = CTkButton(button_border, text="Search Users", font=('arial bold',12), fg_color='#828AFF', hover_color='#5862E9',
                                corner_radius=15, text_color='black',command=lambda: controller.show_frame(searchUsers))
        user_button.place(x=22, y=76.43)

#To keep track of user_id throughout UI
class UserSession:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_user_id = None
        return cls._instance
    
    def set_user_id(self, user_id):
        self.current_user_id = user_id
    
    def get_user_id(self):
        return self.current_user_id

#main loop of frames
class yelp_gui(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)
        self.geometry('1280x720')

        container = CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (loginPage, mainPage, searchBusiness, searchUsers, registerPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(loginPage)

    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if frame:
            frame.tkraise()

#login page
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
            command=lambda: self.check_user_id(user_box, self, controller), fg_color='#828AFF', corner_radius=5, width=256, height=31, hover_color='#5862E9'
        )
        button.place(x=22, y=84)

        #redirects to registering user_id page
        register_button = CTkButton(
            self,
            text="Register",
            font=('arial', 12),
            command=lambda: controller.show_frame(registerPage), fg_color='transparent', corner_radius=5, width=45, height=14, hover_color='#5862E9', text_color='#828AFF'
        )
        register_button.place(x=611, y=463)

    #validates if the entered user_id is registered
    def check_user_id(self, entry, parent, controller):
        user_id = entry.get()
        #decoding uuid
        if user_id:
            user_id1 = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_id))
            user_id1 = base64.urlsafe_b64encode(user_id1.bytes).decode('utf-8').rstrip('=')
            user_id1 = user_id1[:22]
        try:

            cursor.execute("SELECT * FROM user_yelp WHERE user_id = ?", user_id1)
            result = cursor.fetchone()

            if result:
                UserSession().set_user_id(user_id1)
                controller.show_frame(mainPage)
            else:
                raise ValueError("Invalid User ID")
        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(master=parent, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("0.0", f"Error: {error_message}")

#page to register users
class registerPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        self.user_box = None
        self.name_box = None

        title = CTkLabel(self, text="Register", font=('arial bold',40), text_color='#828AFF')
        title.place(x=560, y=141)

        entry_border = CTkFrame(self, width=300, height=211, fg_color='#525252')
        entry_border.place(x=490, y=254)

        user_title = CTkLabel(entry_border, text="Username", font=('arial', 12), text_color='#828AFF')
        user_title.place(x=22, y=19)

        self.user_box = CTkEntry(entry_border, placeholder_text="Enter Username", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.user_box.place(x=23, y=36)

        name_title = CTkLabel(entry_border, text="Name", font=('arial', 12), text_color='#828AFF')
        name_title.place(x=25, y=75)

        self.name_box = CTkEntry(entry_border, placeholder_text="Enter Name", width=256, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.name_box.place(x=23, y=92)

        #button to register user
        button = CTkButton(
            entry_border,
            text="Register",
            font=('arial bold', 12),
            command=self.register_user, fg_color='#828AFF', corner_radius=5, width=256, height=31, hover_color='#5862E9'
        )
        button.place(x=22, y=151)

        #returns to login page
        login_button = CTkButton(
            self,
            text="Login",
            font=('arial', 12),
            command=lambda: controller.show_frame(loginPage), fg_color='transparent', corner_radius=5, width=30, height=14, hover_color='#5862E9', text_color='#828AFF'
        )
        login_button.place(x=625, y=475)

    #function to register user, using uuid and adding to DB
    def register_user(self):
        user_name = self.user_box.get().strip()
        name = self.name_box.get().strip()

        if user_name:
            user_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(user_name))
            user_id = base64.urlsafe_b64encode(user_id.bytes).decode('utf-8').rstrip('=')
            user_id = user_id[:22]

        query = f"INSERT INTO user_yelp(user_id, name) VALUES ('{user_id}', '{name}')"

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print(f"user: {user_id}, is registered")

        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}") 

#first page that opens after logging in
class mainPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        self.entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        self.entry_border.place(x=244, y=40)

        user_title = CTkLabel(self.entry_border, text="Yelp Database", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)
        hello_label = CTkLabel(self.entry_border, text=f"Hello \N{Waving Hand Sign}", font=('arial bold', 32), text_color='#828AFF')
        hello_label.place(x=788, y=22)
        
        load_buttons(self, controller)

#search for business
class searchBusiness(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        #instance variables
        self.slider = None
        self.min_stars_label = None
        self.city_box = None
        self.bus_box = None
        self.orderchoice = StringVar()
        self.bychoice = StringVar()       
        column_name = ['id', 'name', 'address', 'city', 'stars']
        self.tree = ttk.Treeview(self, columns=column_name, show='headings')
        self.toplevel_window = None
        self.business_values = None

        self.entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        self.entry_border.place(x=244, y=40)

        user_title = CTkLabel(self.entry_border, text="Search for a Business", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        hello_label = CTkLabel(self.entry_border, text=f"Hello \N{Waving Hand Sign}", font=('arial bold', 32), text_color='#828AFF')
        hello_label.place(x=788, y=22)

        load_buttons(self, controller)
        self.min_stars()
        self.city()
        self.bus_name()
        self.filter_tab()
        self.instantiate_tree()

        #button to review business
        button = CTkButton(
            self,
            text="Review Business",
            font=('arial bold', 32),
            command=self.review_business, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=51, 
            hover_color='#5862E9', 
            text_color='black'
        )
        button.place(x=244, y=629)

        #button to search business
        search = CTkButton(
            self,
            text="Search",
            font=('arial bold', 32),
            command=self.execute_search, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=120, 
            hover_color='#5862E9', 
            text_color='black'
        )
        search.place(x=244, y=493)

    #min stars slider
    def min_stars(self):
        min_stars_frame = CTkFrame(self, width=303, height=79, corner_radius=20, fg_color='#525252')
        min_stars_frame.place(x=244, y=170)

        def update_star_value(value):
            self.min_stars_label.configure(text=f"Minimum \N{White Medium Star}: {int(value)}")

        self.slider = CTkSlider(min_stars_frame, from_=0, to=5, number_of_steps=5, progress_color=('black', '#828AFF'), height=10, width=269, button_color='white', 
                           command=update_star_value)
        self.slider.place(x=16, y=54)
        self.slider.set(int(0))

        self.min_stars_label = CTkLabel(min_stars_frame, text=f"Minimum \N{White Medium Star}: {self.slider.get()}", font=('arial bold', 32), text_color='black')
        self.min_stars_label.place(x=19, y=8)

    #city entry box
    def city(self):
        city_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        city_frame.place(x=244, y=261)

        city_label = CTkLabel(city_frame, text="City \N{Cityscape}", font=('arial bold', 32), text_color='black')
        city_label.place(x=19, y=8)

        self.city_box = CTkEntry(city_frame, placeholder_text="Enter city name", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.city_box.place(x=21, y=52)
    
    #business entry box
    def bus_name(self):
        bus_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        bus_frame.place(x=244, y=375)

        bus_label = CTkLabel(bus_frame, text="Business name \N{Necktie}", font=('arial bold', 32), text_color='black')
        bus_label.place(x=19, y=8)

        self.bus_box = CTkEntry(bus_frame, placeholder_text="Enter business name", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.bus_box.place(x=21, y=52)

    #performs search and displays updated table
    def execute_search(self):
        min_stars = int(self.slider.get())
        city = self.city_box.get().strip()
        business_name = self.bus_box.get().strip()
        order = self.orderchoice.get()
        order_by = self.bychoice.get()

        #formulate query
        query = "SELECT business_id, name, address, city, stars FROM business WHERE 1=1"

        if min_stars > 0:
            query += f" AND stars >= {min_stars}"
        
        if city:
            query += f" AND city LIKE '%{city}%'"

        #adds another apostrophe if one exist to escape it
        result_string = ""
        for char in business_name:
            result_string += char
            if char == "'":
                result_string += "'"    
        
        if business_name:
            query += f" AND name LIKE '%{result_string}%'"
        

        if order and order_by:
            query += f" ORDER BY {order_by} {order.upper()}"
        
        empty_frame = CTkFrame(self.entry_border, width=200, height=100, corner_radius=20, fg_color='transparent')
        empty_frame.place(x=775, y=9)

        empty_label = CTkLabel(empty_frame, text="ERROR: Empty Result", text_color='#525252', font=('arial bold', 18))
        empty_label.place(relx=0.5, rely=0.5, anchor=CENTER)
 

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            if len(results) == 0:
                empty_label.configure(text_color='red')
            else:
                empty_label.configure(text_color='#525252')
            
            self.populate_treeview(results)
        
        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}")

    #deletes current tables and generates queried table
    def populate_treeview(self, results):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row_data in results:
            sanitized_row = [str(item).replace(",", " ") for item in row_data]
            self.tree.insert('', 'end', values=sanitized_row)

    #filtering variables
    def filter_tab(self):
        filter_frame = CTkFrame(self, width=667, height=76, corner_radius=20, fg_color='#525252')
        filter_frame.place(x=571, y=170)

        filter_label = CTkLabel(filter_frame, text="Filter", font=('arial bold', 32), text_color='black')
        filter_label.place(x=19, y=18)

        order_frame = CTkFrame(filter_frame, width=227, height=38, corner_radius=20, fg_color='transparent', border_color='#828AFF')
        order_frame.place(x=125, y=18)

        by_frame = CTkFrame(filter_frame, width=200, height=38, corner_radius=20, fg_color='transparent', border_color='#828AFF')
        by_frame.place(x=386, y=18)

        order_label = CTkLabel(order_frame, text="Order", font=('arial bold', 20), text_color='black')
        order_label.place(x=5, y=8)

        by_label = CTkLabel(by_frame, text="By", font=('arial bold', 20), text_color='black')
        by_label.place(x=6, y=7)

        desc_radio = CTkRadioButton(order_frame, variable=self.orderchoice, text="Descending", value='DESC',
                                  font=("arial", 12), text_color='black', radiobutton_width=10, radiobutton_height=10, hover_color='#5862E9', fg_color='#828AFF')
        asc_radio = CTkRadioButton(order_frame, variable=self.orderchoice, text="Ascending", value='ASC',
                                  font=("Arial", 12), text_color='black', radiobutton_width=10, radiobutton_height=10, hover_color='#5862E9', fg_color='#828AFF')
        desc_radio.place(x=64, y=13)
        asc_radio.place(x=149, y=13)

        name_radio = CTkRadioButton(by_frame, variable=self.bychoice, text="Name", value='name',
                                  font=("arial", 12), text_color='black', radiobutton_width=10, radiobutton_height=10, hover_color='#5862E9', fg_color='#828AFF')
        city_radio = CTkRadioButton(by_frame, variable=self.bychoice, text="City", value='city',
                                  font=("Arial", 12), text_color='black', radiobutton_width=10, radiobutton_height=10, hover_color='#5862E9', fg_color='#828AFF')
        star_radio = CTkRadioButton(by_frame, variable=self.bychoice, text="Stars", value='stars',
                                  font=("Arial", 12), text_color='black', radiobutton_width=10, radiobutton_height=10, hover_color='#5862E9', fg_color='#828AFF')
        name_radio.place(x=39, y=13)
        city_radio.place(x=97, y=13)
        star_radio.place(x=144, y=13)
    
    #building the initial tree
    def instantiate_tree(self):
        column_name = ['id', 'name', 'address', 'city', 'stars']
        cursor.execute('SELECT business_id, name, address, city, stars FROM business' )
        row = cursor.fetchall()

        tree_frame = CTkFrame(self, width=667, height=422, corner_radius=20, fg_color='#525252')
        tree_frame.place(x=571, y=258)

        self.tree = ttk.Treeview(tree_frame, columns=column_name, show='headings', height=23)

        for column in column_name:
            self.tree.heading(column=column, text=column)
            self.tree.column(column=column, width=157)

        for row_data in row:
            sanitized_row = [str(item).replace(",", " ") for item in row_data]
            self.tree.insert(parent='', index='end', values=sanitized_row)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background='#393939', fieldbackground='#393939', foreground='#828AFF', font=('arial', 12))
        style.configure("Treeview.Heading", background='#393939', fieldbackground='#393939', foreground='#828AFF', font=('arial bold', 12))


        self.tree.place(x=23, y=22)  

    #gets the selected row of the table
    def fetch_selected(self):
        selected_item = self.tree.selection() 
        if selected_item:
            item_data = self.tree.item(selected_item)  
            self.business_values = item_data['values'] 
        else:
            print("No item selected")

    #opens another window to review business
    def review_business(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.fetch_selected()
            self.toplevel_window.bus_id = self.business_values[0]
            self.toplevel_window.bus_name = self.business_values[1]
            self.toplevel_window.id_label.configure(text=f"{self.business_values[0]}")
            self.toplevel_window.bus_name_label.configure(text=f"{self.business_values[1]}")
        else:
            self.toplevel_window.focus()  # if window exists focus it

#pop up window to review a business
class ToplevelWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("419x450")

        self.bus_id = None
        self.bus_name = None

        review_frame = CTkFrame(self, width=393, height=118, corner_radius=20, fg_color='#525252')
        review_frame.place(x=13, y=10)
        review_label = CTkLabel(review_frame, text='Review a Business', font=('arial bold', 40), text_color='#828AFF')
        review_label.place(x=16, y=36)

        business_frame = CTkFrame(self, width=393, height=124, corner_radius=20, fg_color='#525252')
        business_frame.place(x=13, y=140)
        business_label = CTkLabel(business_frame, text='For Business:', font=('arial bold', 32), text_color='black')
        business_label.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.id_label = CTkLabel(business_frame, text="bus_id holder", font=('arial ', 20), text_color='black')
        self.id_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.bus_name_label = CTkLabel(business_frame, text="bus_id holder", font=('arial ', 20), text_color='black')
        self.bus_name_label.place(relx=0.5, rely=0.8, anchor=CENTER)

        stars_frame = CTkFrame(self, width=303, height=79, corner_radius=20, fg_color='#525252')
        stars_frame.place(x=58, y=281)

        def update_star_value(value):
            self.min_stars_label.configure(text=f"Stars \N{White Medium Star}: {int(value)}")

        self.slider = CTkSlider(stars_frame, from_=0, to=5, number_of_steps=5, progress_color=('black', '#828AFF'), height=10, width=269, button_color='white', 
                           command=update_star_value)
        self.slider.place(x=17, y=57)
        self.slider.set(int(0))

        self.min_stars_label = CTkLabel(stars_frame, text=f"Stars \N{White Medium Star}: {self.slider.get()}", font=('arial bold', 32), text_color='black')
        self.min_stars_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        review = CTkButton(
            self,
            text="Submit Review",
            font=('arial bold', 32),
            command=self.execute_review_query, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=51, 
            hover_color='#5862E9', 
            text_color='black'
        )
        review.place(x=58, y=381)

    def execute_review_query(self):
        query_bus_id = self.bus_id
        date = datetime.today()
        date_seconds = int(date.timestamp())
        date = str(date)
        date = date[0:23]
        user_id = str(UserSession().get_user_id())

        base_review_id = user_id + str(date_seconds)
        review_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(base_review_id))
        review_id = base64.urlsafe_b64encode(review_id.bytes).decode('utf-8').rstrip('=')
        review_id = review_id[:22]

        #formulate queries
        insert_query = f"INSERT INTO review(review_id, user_id, business_id, stars, date) VALUES ('{review_id}', '{user_id}', '{query_bus_id}', {self.slider.get()}, '{date}')"
        update_bus_query = f"UPDATE business SET stars = (SELECT ROUND(AVG(CAST(R.stars AS FLOAT)), 2) FROM review R, business b WHERE b.business_id = '{query_bus_id}' AND R.business_id = b.business_id) WHERE business_id = '{query_bus_id}'"
        update_user_query = f"UPDATE user_yelp SET review_count = review_count + 1, average_stars = (SELECT ROUND(AVG(CAST(R.stars AS FLOAT)), 2) FROM review R WHERE R.user_id = '{query_bus_id}') WHERE user_id = '{user_id}'"

        try:
            cursor = connection.cursor()
            cursor.execute(insert_query)
            cursor.execute(update_bus_query)
            cursor.execute(update_user_query)
            cursor.commit()
            print(f"Successfully reviewed: {query_bus_id}, with Updates to businesss and yelp_user")
        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}")    

#page for searching users
class searchUsers(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
      
        self.slider = 0
        self.rev_box = 0
        self.user_box = None
        self.friend_values = None

        self.entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        self.entry_border.place(x=244, y=40)

        user_title = CTkLabel(self.entry_border, text="Search for Users", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        hello_label = CTkLabel(self.entry_border, text=f"Hello \N{Waving Hand Sign}", font=('arial bold', 32), text_color='#828AFF')
        hello_label.place(x=788, y=22)

        load_buttons(self, controller)
        self.min_avg_stars()
        self.min_rev_count()
        self.user_name()
        self.instantiate_tree()

        #button to make friend
        make_friend_but = CTkButton(
            self,
            text="Make Friend",
            font=('arial bold', 32),
            command=self.make_friend_query, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=51, 
            hover_color='#5862E9', 
            text_color='black'
        )
        make_friend_but.place(x=244, y=629)

        #button to search for users
        search = CTkButton(
            self,
            text="Search",
            font=('arial bold', 32),
            command=self.execute_search, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=120, 
            hover_color='#5862E9', 
            text_color='black'
        )
        search.place(x=244, y=493)

    #minimum average stars slider
    def min_avg_stars(self):
        min_stars_frame = CTkFrame(self, width=303, height=79, corner_radius=20, fg_color='#525252')
        min_stars_frame.place(x=244, y=170)

        def update_star_value(value):
            self.min_stars_label.configure(text=f"Minimum \N{White Medium Star}: {int(value)}")

        self.slider = CTkSlider(min_stars_frame, from_=0, to=5, number_of_steps=5, progress_color=('black', '#828AFF'), height=10, width=269, button_color='white', 
                           command=update_star_value)
        self.slider.place(x=16, y=54)
        self.slider.set(int(0))

        self.min_stars_label = CTkLabel(min_stars_frame, text=f"Minimum \N{White Medium Star}: {self.slider.get()}", font=('arial bold', 32), text_color='black')
        self.min_stars_label.place(x=19, y=8)

    #minimum review count entry box
    def min_rev_count(self):
        rev_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        rev_frame.place(x=244, y=261)

        rev_label = CTkLabel(rev_frame, text="Min Review Count", font=('arial bold', 32), text_color='black')
        rev_label.place(x=19, y=8)

        self.rev_box = CTkEntry(rev_frame, placeholder_text="Enter Amount", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.rev_box.place(x=21, y=52)

    #user name entry box
    def user_name(self):
        user_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        user_frame.place(x=244, y=375)

        user_label = CTkLabel(user_frame, text="User name \N{Necktie}", font=('arial bold', 32), text_color='black')
        user_label.place(x=19, y=8)

        self.user_box = CTkEntry(user_frame, placeholder_text="Enter user name", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.user_box.place(x=21, y=52)

    #gets selected row from table
    def fetch_selected(self):
        selected_item = self.tree.selection() 
        if selected_item:
            item_data = self.tree.item(selected_item)  
            self.friend_values = item_data['values'] 
        else:
            print("No item selected")

    #makes friend with selected friend/row
    def make_friend_query(self):
        self.fetch_selected()
        friend = str(self.friend_values[0])
        user_id = str(UserSession().get_user_id())

        query = f"INSERT INTO friendship(user_id, friend) VALUES ('{user_id}', '{friend}')"

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print(f"user: {user_id}, is now friends with {friend}")

        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}") 

    #searches for friend with desired options
    def execute_search(self):
        min_avg_stars = int(self.slider.get())
        if self.rev_box.get():
            min_review = int(self.rev_box.get().strip())
        else:
            min_review = 0
        user_name = self.user_box.get().strip()
        #formulate query
        query = "SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM user_yelp WHERE 1=1"
        
        if min_avg_stars > 0:
            query += f" AND average_stars >= {min_avg_stars}"
        
        if min_review > 0:
            query += f" AND review_count >= {min_review}"
        
        if user_name:
            query += f" AND name LIKE '%{user_name}%'"
        
        query += 'ORDER BY name'

        #error message if empty
        empty_frame = CTkFrame(self.entry_border, width=200, height=100, corner_radius=20, fg_color='transparent')
        empty_frame.place(x=775, y=9)

        empty_label = CTkLabel(empty_frame, text="ERROR: Empty Result", text_color='#525252', font=('arial bold', 18))
        empty_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            if len(results) == 0:
                empty_label.configure(text_color='red')
            else:
                empty_label.configure(text_color='#525252')
            
            self.populate_treeview(results)
        
        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}")
    
    #deletes current table and displays queried table
    def populate_treeview(self, results):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row_data in results:
            sanitized_row = [str(item).replace(",", " ") for item in row_data]
            self.tree.insert('', 'end', values=sanitized_row)

    #initializes table
    def instantiate_tree(self):
        column_name = ['id', 'name', 'review count', 'useful', 'funny', 'cool', 'average stars', 'registered date']
        cursor.execute('SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM user_yelp' )
        row = cursor.fetchall()

        tree_frame = CTkFrame(self, width=667, height=510, corner_radius=20, fg_color='#525252')
        tree_frame.place(x=571, y=170)

        self.tree = ttk.Treeview(tree_frame, columns=column_name, show='headings', height=28)

        for column in column_name:
            self.tree.heading(column=column, text=column)
            self.tree.column(column=column, width=98)

        for row_data in row:
            sanitized_row = [str(item).replace(",", " ") for item in row_data]
            self.tree.insert(parent='', index='end', values=sanitized_row)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background='#393939', fieldbackground='#393939', foreground='#828AFF', font=('arial', 12))
        style.configure("Treeview.Heading", background='#393939', fieldbackground='#393939', foreground='#828AFF', font=('arial bold', 12))


        self.tree.place(x=23, y=22) 


gui = yelp_gui()
gui.mainloop()

cursor.close()
connection.close()


