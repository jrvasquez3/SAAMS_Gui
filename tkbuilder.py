import ttkbootstrap as tb


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


class Table_tab1:
    def __init__(self, frame):
        ROWS = 4
        COLS = 4
        col_names = ["Strip ID", "Strip Qty", "Strip Width (mm)", "Strip Total (mm)" ]
        self.entry = {}
        self.label = {}
        self.var = {}
        counter = 0
        table_entry_style = tb.Style().configure('litera.TEntry', fieldbackground= 'white', foreground='black', insertcolor="black")
        table_label_style = tb.Style().configure('light.TEntry', fieldbackground= '#FF7F7F', foreground='black')
        for rows in range(1, ROWS):
            for col in range(0, COLS):
                if rows == 1:
                    self.label[counter] = tb.Entry(frame, style="light.TEntry", width=20)
                    self.label[counter].grid(row=rows, column=col)
                    self.label[counter].insert(0, col_names[col])
                    self.label[counter].configure(state="readonly")
                elif rows != 1:
                    self.entry[counter] = tb.Entry(frame, style="litera.TEntry", width=20)
                    self.entry[counter].grid(row=rows, column= col)
                    self.entry[counter].bind("<Down>", lambda event, self_ = self.entry, c = counter: self.down(event, self_, c, COLS))
                    self.entry[counter].bind("<Up>", lambda event, self_ = self.entry, c = counter: self.up(event, self_, c, COLS))
                    self.entry[counter].bind("<Left>", lambda event, self_ = self.entry, c = counter: self.left(event, self_, c, COLS))
                    self.entry[counter].bind("<Right>", lambda event, self_ = self.entry, c = counter: self.right(event, self_, c, COLS))
                counter = counter + 1
    
    # Functions to move through the table using keys "Down", "Up", "Left", "Right"
    def down(object_table, event, self_, c, cols):
        self_[c + cols].focus_set()
        return
    def up(object_table, event, self_, c, cols):
        self_[c - cols].focus_set()
        return
    def left(object_table, event, self_, c, cols):
        self_[c - 1].focus_set()
        return
    def right(object_table, event, self_, c, cols):
        self_[c + 1].focus_set()
        return


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

    def convert_mm_to_in(self, list_a):
        list_b = []
        for i in list_a:
            list_b.append(round(float(i) * 0.03937007874, 2))
        return list_b

    def convert_in_to_mm(self, list_a):
        list_b = []
        for i in list_a:
            list_b.append(round(float(i) * 25.4, 2))
        return list_b


    