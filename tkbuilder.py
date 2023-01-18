import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame as Sf
import csv
import pandas as pd


# Function event to allow user to move between widgets using UP and DOWN keys
# To call, use "bind()" function. Example: .bind("<Up>")
def input_frame_down(event):
    event.widget.tk_focusNext().focus_set()
    return

def input_frame_up(event):
    event.widget.tk_focusPrev().focus_set()
    return





# Auto-fills calculation after every keystroke and focus-out
def calculator_key_release(event, operation ,box_label_num, box_2,output_box):
    ''' Example: self.gauge.bind("<KeyRelease>", lambda event, label_num=self.gauge, box_sec=self.gap, out=self.clearance: tkb.calculator_key_release(event, "mult", label_num , box_sec, out))
        
        event: you define as lambda: event

        operation: "mult" or "div" 

        box_label_num: Entry box that is currently being typed on

        box_2        : Entry Box used for the 2nd value in calculation ex. Entry1 * Entry2 OR Entry1/Entry2

        output_box   : Entry box where you want the result to be displayed on'''
        
    gap_per = box_label_num.get()
    box2 = box_2.get()
    if gap_per == "":
        output_box.delete(0, tb.tk.END)
        output_box.insert(0, 0)
        return
    if box2 == "":
        box_2.insert(0, 0)
        box2 = box_2.get()
    if operation == "mult":
        resultant = (float(gap_per)/100) * (float(box2))
        output_box.delete(0, tb.tk.END)
        output_box.insert(0, round(resultant, 2))
    elif operation == "div":
        try:
            resultant = ((float(gap_per))* 100)/(float(box2))
        except ZeroDivisionError:
            resultant = 0
        output_box.delete(0, tb.tk.END)
        output_box.insert(0, round(resultant, 2))
    return


# Allows only numbers and floats to be typed into entry, not strings
def correct_int(key_val):
    '''
    Function used to check wether a pressed key is a number resulting a float

    Ex: Pressing 1-9 will succeed
        Pressing "." resulting in a float will succeed
        Pressing any other character will NOT succeed

    To use , the following is an example of code:

    key_stroke_validation = self.a[i].register(tkb.correct_int)
    self.a[i].config(validate="key", validatecommand=(key_stroke_validation, '%P'))
    
    '''
    # Check if keys is numberic
    if key_val.isnumeric():
        return True
        # Check if keys is empty
    elif key_val == "":
        return True
    else:
        # Check if keys is float 
        try:
            float_test = float(key_val)
        except ValueError:
            float_test = key_val
        if isinstance(float_test, float) == True:
            return True
            # test fails. Prevents key from being typed into box
        else:
            return False



class Tab1_Table:
    def __init__(self, frame):
        # Add Scrollable Frame
        self.frame = Sf(frame, width=1370, height=220)
        self.frame.grid(row=1, column=0, columnspan=5)

        # read dafult values for table from csv
        with open('default_values\Tab1_Table.csv', 'r') as file:
            reader = csv.reader(file)
            data = []
            for line in reader:
                data.append(line)

        # Set Styles for table
        entry_style = tb.Style().configure('litera.TEntry', fieldbackground= 'white', foreground='black', insertcolor="black")
        label_style = tb.Style().configure('light.TEntry', fieldbackground= '#FF7F7F', foreground='black')
        entry_style = tb.Style().configure('end.TEntry', fieldbackground= '#01cdfe', foreground='black', insertcolor="black")
        
        # Create Table and save each entry into a matrix
        self.entry_table = []
        for i in range(0, len(data)):
            row = []
            for j in range(0, len(data[0])):
                if i == 0:
                    entry = tb.Entry(frame, style="light.TEntry", width=20)
                    entry.insert(0, data[i][j])
                    entry.configure(state="readonly")
                    row.append(entry)
                elif i == (len(data) - 1):
                    entry = tb.Entry(frame, style="litera.TEntry", width=20)
                    entry.insert(0, data[i][j])
                    if j == (len(data[0]) - 1):
                        entry.configure(style="end.TEntry")
                    if j != 0:
                        key_stroke_validation = entry.register(correct_int)
                        entry.config(validate="key", validatecommand=(key_stroke_validation, '%P'))
                    entry.grid(row=6, column=j)
                    row.append(entry)
                else:
                    entry = tb.Entry(self.frame, style="litera.TEntry", width=20)
                    entry.insert(0, data[i][j])
                    if i == 1 and j == 0:
                        pass
                    else:
                        key_stroke_validation = entry.register(correct_int)
                        entry.config(validate="key", validatecommand=(key_stroke_validation, '%P'))
                    row.append(entry)
            self.entry_table.append(row)
        
        self.add_grids()
        self.button_total = tb.Button(frame, text="Total", command=self.calculate_total)
        self.button_total.grid(row=7, column=(len(data[0]) -1))

    # function used to update / add binding to each entry and grid them onto the table to show
    def add_grids(self):
        for i in range(0, len(self.entry_table) - 1):
            for j in range(0, len(self.entry_table[0])):
                self.entry_table[i][j].bind("<Down>", lambda event, i = i, j = j: self.down(event, i, j))
                self.entry_table[i][j].bind("<Up>", lambda event, i = i, j = j: self.up(event, i, j))
                self.entry_table[i][j].bind("<Left>", lambda event, i = i, j = j: self.left(event, i, j))
                self.entry_table[i][j].bind("<Right>", lambda event, i = i, j = j: self.right(event, i, j))
                self.entry_table[i][j].bind("<Return>", self.calculate_total)
                self.entry_table[i][j].grid(row=i, column= j)
        

    # function used to "unbind" and remove grid locations on table. Used to re-update position of rows in table   
    def remove_grid(self):
        for i in range(0, len(self.entry_table) - 1):
            for j in range(0, len(self.entry_table[0])):
                self.entry_table[i][j].unbind("<Down>")
                self.entry_table[i][j].unbind("<Up>")
                self.entry_table[i][j].unbind("<Left>")
                self.entry_table[i][j].unbind("<Right>")
                self.entry_table[i][j].unbind("<Return>")
                self.entry_table[i][j].grid_remove()

    # function used to add a New Row to the table
    def add_row(self, frame):
        row = []
        self.remove_grid()
        for j in range(0, len(self.entry_table[0])):
            entry = tb.Entry(self.frame, style="litera.TEntry", width=20)
            if j == 0:
                entry.insert(0, len(self.entry_table) - 2)
            row.append(entry)
        self.entry_table.insert(len(self.entry_table) - 1, row)
        self.add_grids()

    # functions used to move UP, DOWN, RIGHT, LEFT on the table
    def down(self, event, i, j):
        try:
            self.entry_table[i + 1][j].focus_set()
        except IndexError:
            pass
    def up(self, event, i, j):
        try:
            self.entry_table[i - 1][j].focus_set()
        except IndexError:
            pass
    def left(self, event, i, j):
        try:
            self.entry_table[i][j - 1].focus_set()
        except IndexError:
            pass
    def right(self, event, i, j):
        try:
            self.entry_table[i][j + 1].focus_set()
        except IndexError:
            pass

    def calculate_total(self, event= False):
        for row in self.entry_table[1:]:
            val1 = row[1].get()
            val2 = row[3].get()
            total = float(val1)*float(val2)
            row[4].delete(0, tb.tk.END)
            row[4].insert(0, round(total, 2))



class Dash_Tab1:
    def __init__(self, frame):
        # create Selector for Number of Strips
        num = list(range(1, 21))
        tb.Label(frame, text='Select Strips:').grid(row=0, column=0)
        self.strip_num = tb.Combobox(frame, values=num, width=8, state="readonly")
        self.strip_num.set(1)
        self.strip_num.grid(row=1, column=0)

        # Create Current Units
        tb.Label(frame, text='Units: ').grid(row=0, column=1, sticky='w', padx=10)
        self.units = tb.Label(frame, text='')
        self.units.grid(row=1, column=1, sticky='w', padx=10)

        # Saved Units - Obtained
        self.label_units = tb.Label(frame, text="Obtained Data in ")
        self.label_units.grid(row=0, column=2, sticky='w' ,padx=10)
        tb.Label(frame, text='width:').grid(row=1, column=2, sticky='w',padx=10)
        tb.Label(frame, text='Gauge:').grid(row=2, column=2, sticky='w',padx=10)
        tb.Label(frame, text='Clearance:').grid(row=3, column=2, sticky='w',padx=10)
        self.width = tb.Label(frame, text='')
        self.width.grid(row=1, column=2, sticky='e',padx=10)
        self.gauge = tb.Label(frame, text='')
        self.gauge.grid(row=2, column=2, sticky='e',padx=10)
        self.clearance = tb.Label(frame, text='')
        self.clearance.grid(row=3, column=2, sticky='e',padx=10)

        # Saved Units - Converted
        self.label_units_c = tb.Label(frame, text="Data Converted to ")
        self.label_units_c.grid(row=0, column=3, sticky='w' ,padx=10)
        tb.Label(frame, text='width:').grid(row=1, column=3, sticky='w',padx=10)
        tb.Label(frame, text='Gauge:').grid(row=2, column=3, sticky='w',padx=10)
        tb.Label(frame, text='Clearance:').grid(row=3, column=3, sticky='w',padx=10)
        self.width_converted = tb.Label(frame, text='')
        self.width_converted.grid(row=1, column=3, sticky='e',padx=10)
        self.gauge_converted = tb.Label(frame, text='')
        self.gauge_converted.grid(row=2, column=3, sticky='e',padx=10)
        self.clearance_converted = tb.Label(frame, text='')
        self.clearance_converted.grid(row=3, column=3, sticky='e',padx=10)

    # Update Units and values shown on Dash   
    def display_converted_units(self, list_a):
        self.width.configure(text=str(list_a[0]))
        self.gauge.configure(text=str(list_a[1]))
        self.clearance.configure(text=str(list_a[2]))
        self.units.configure(text=str(list_a[3]))
        self.label_units.configure(text="Obtained Data in " + str(list_a[3]))
        if list_a[3] == 'Milimeter (mm)':
            list_b = self.convert_mm_to_in(list_a[0:3])
            self.label_units_c.configure(text="Data Converted to Inches (in)")
        else:
            list_b = self.convert_in_to_mm(list_a[0:3])
            self.label_units_c.configure(text="Data Converted to Milimeter (mm)")
        self.width_converted.configure(text=str(list_b[0]))
        self.gauge_converted.configure(text=str(list_b[1]))
        self.clearance_converted.configure(text=str(list_b[2]))

    # function used to convert units from (mm) to (in)
    def convert_mm_to_in(self, list_a):
        list_b = []
        for i in list_a:
            list_b.append(round(float(i) * 0.03937007874, 2))
        return list_b

    # function used to convert units from (in) to (mm)
    def convert_in_to_mm(self, list_a):
        list_b = []
        for i in list_a:
            list_b.append(round(float(i) * 25.4, 2))
        return list_b



class tree_builder:
    def __init__(self, frame, df):
        '''
        frame = Enter Frame where you want this tree to be created at
        df = Enter pandas dataframe
        '''
        self.tree = tb.Treeview(frame, height=15)
        s = tb.Style()
        s.configure('mystyle.Treeview', background='white', foreground='black')
        #tree_style = tb.Style().configure('litera.TEntry', fieldbackground= 'white', foreground='black', insertcolor="black")

        self.tree.configure(style='mystyle.Treeview')
        self.tree.pack(expand='YES', fill='both', side='left')
        #self.tree.grid(row=0, column=0, padx=1)

        column_names = tuple(df.keys())
        self.tree["columns"] = column_names
        for i in column_names:
            self.tree.column(i, stretch='YES', anchor='w')
            self.tree.heading(i, text=i, anchor='w')

        self.populate_treeview(df)

    def populate_treeview(self, df):
        for i in range(len(df)):
            self.tree.insert('', 'end', values=(df.iloc[i]['Gauge (in)'], 
                                      df.iloc[i]['Customer'], 
                                      df.iloc[i]['Grade'],
                                      df.iloc[i]['Clearance % to use'],
                                      df.iloc[i]['Female Rubber'],
                                      df.iloc[i]['Male rubber'],
                                      df.iloc[i]['MPA Quality Min/Max'],
                                      df.iloc[i]['Comments']))




 



    