import pyodbc
from tkinter import ttk
from customtkinter import *
import passwords

connection = pyodbc.connect(f"driver={{ODBC Driver 18 for SQL Server}};server=cypress.csil.sfu.ca;uid=s_sdh13;pwd={passwords.pwd};Encrypt=yes;TrustServerCertificate=yes")
cursor = connection.cursor()

def check_user_id(entry, parent, controller):
    user_id = entry.get()
    try:

        cursor.execute("SELECT * FROM dbo.helpdesk WHERE username = ?", user_id)
        result = cursor.fetchone()

        if result:
            controller.show_frame(mainPage)
        else:
            raise ValueError("Invalid User ID")
    except (pyodbc.Error, ValueError) as ex:
        error_message = str(ex)
        textbox = CTkTextbox(master=parent, width=200, height=50, corner_radius=5)
        textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
        textbox.insert("0.0", f"Error: {error_message}")

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
            command=lambda: check_user_id(user_box, self, controller), fg_color='#828AFF', corner_radius=5, width=256, height=31, hover_color='#5862E9'
        )
        button.place(x=22, y=84)


class mainPage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=244, y=40)

        user_title = CTkLabel(entry_border, text="Yelp Database", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        load_buttons(self, controller)


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

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=244, y=40)

        user_title = CTkLabel(entry_border, text="Yelp Database - Search for a Business", font=('arial bold', 40), text_color='#828AFF')
        user_title.place(x=16, y=39)

        load_buttons(self, controller)
        self.min_stars()
        self.city()
        self.bus_name()
        self.filter_tab()
        self.instantiate_tree()

        button = CTkButton(
            self,
            text="Review Business",
            font=('arial bold', 32),
            command=self.execute_search, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=51, 
            hover_color='#5862E9', 
            text_color='black'
        )
        button.place(x=244, y=629)

        search = CTkButton(
            self,
            text="Search",
            font=('arial bold', 32),
            command=self.fetch_selected, 
            fg_color='#828AFF', 
            corner_radius=15, 
            width=303, 
            height=120, 
            hover_color='#5862E9', 
            text_color='black'
        )
        search.place(x=244, y=493)

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

    def city(self):
        city_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        city_frame.place(x=244, y=261)

        city_label = CTkLabel(city_frame, text="City \N{Cityscape}", font=('arial bold', 32), text_color='black')
        city_label.place(x=19, y=8)

        self.city_box = CTkEntry(city_frame, placeholder_text="Enter city name", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.city_box.place(x=21, y=52)
    
    def bus_name(self):
        bus_frame = CTkFrame(self, width=303, height=102, corner_radius=20, fg_color='#525252')
        bus_frame.place(x=244, y=375)

        bus_label = CTkLabel(bus_frame, text="Business name \N{Necktie}", font=('arial bold', 32), text_color='black')
        bus_label.place(x=19, y=8)

        self.bus_box = CTkEntry(bus_frame, placeholder_text="Enter business name", width=255, height=30, fg_color='#D9D9D9', border_color='#828AFF', corner_radius=5, text_color='black')
        self.bus_box.place(x=21, y=52)

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
        
        if business_name:
            query += f" AND name LIKE '%{business_name}%'"
        

        if order and order_by:
            query += f" ORDER BY {order_by} {order.upper()}"
        

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            self.populate_treeview(results)
        
        except (pyodbc.Error, ValueError) as ex:
            error_message = str(ex)
            textbox = CTkTextbox(self, width=200, height=50, corner_radius=5)
            textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
            textbox.insert("Database Error", f"Error: {error_message}")

    #generates queried table
    def populate_treeview(self, results):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row_data in results:
            sanitized_row = [str(item).replace(",", " ") for item in row_data]
            self.tree.insert('', 'end', values=sanitized_row)

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

    def fetch_selected(self):
        selected_item = self.tree.selection() 
        if selected_item:
            item_data = self.tree.item(selected_item)  
            values = item_data['values'] 
            print("Selected Item Data:", values) 
        else:
            print("No item selected")      



class searchUsers(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        entry_border = CTkFrame(self, width=994, height=118, fg_color='#525252')
        entry_border.place(x=244, y=40)

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


gui = yelp_gui()
gui.mainloop()

cursor.close()
connection.close()


