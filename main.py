'''Author: Jose R Vasquez Perez'''

import ttkbootstrap as tb
import tkbuilder as tkb
from ttkbootstrap.scrolled import ScrolledFrame as Sf


# Create Main Window
class Window_main:
    def __init__(self, root):
        # Add title and geometry
        self.root = root
        self.title = self.root.title("Slitter Arbor Management System")
        self.geometry = self.root.geometry("2200x1000")

        # Create bg image frame
        self.bg_image = tb.PhotoImage(file="img\saams_main.png")
        self.bg_img = tb.Canvas(self.root, width=2000, height= 1400)
        self.bg_img.pack(fill="both", expand=True)
        self.bg_img.create_image(0,0, image= self.bg_image, anchor="nw") 
        

        # Create Navigation Frame
        self.nav = tb.Frame(self.bg_img)
        self.nav.grid(row=0, column=0, columnspan=4)

        self.save = tb.Button(self.nav, text="Save").grid(row=0, column=0, ipadx=100)
        self.tool_mg = tb.Button(self.nav, text="Tool Management").grid(row=0, column=1, padx=10, ipadx=100)
        self.exit = tb.Button(self.nav, text="Exit", command=self.root.destroy).grid(row=0, column=2, ipadx=100)

        # Create Notebook with Tab 1 and Tab 2
        self.tabs = tb.Notebook(self.bg_img, style='primary')

        self.tab1 = tb.Frame(self.tabs)
        self.tab2 = tb.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Enter Specifications")
        self.tabs.add(self.tab2, text="Standard Table")

        self.tabs.grid(row=1, columnspan=6 , pady=15)

        # --------------------------Add to tab 1 ----------------------------------------------
        # Add Labels
        label1 = tb.Label(self.tab1, text="-         Coil Specifications         -", font='', background='white', foreground='black').grid(row=0, column=0, pady=30, columnspan=5)
        lbl1 = tb.Label(self.tab1, text="SAP Batch Number:").grid(row=1, column=0, columnspan=3, sticky="e")
        lbl2 = tb.Label(self.tab1, text="Customer Name:").grid(row=2, column=0, columnspan=3, sticky="e")
        lbl3 = tb.Label(self.tab1, text="Coil's Width:").grid(row=3, column=0, columnspan=3, sticky="e")
        lbl4 = tb.Label(self.tab1, text="Coil's Gauge:").grid(row=4, column=0, columnspan=3, sticky="e")
        lbl5 = tb.Label(self.tab1, text="Cutting Gap %:").grid(row=5, column=0, columnspan=3, sticky="e")
        lbl6 = tb.Label(self.tab1, text="Clearance:").grid(row=6, column=0, columnspan=3, sticky="e")
        lbl7 = tb.Label(self.tab1, text="Units:").grid(row=7, column=0, columnspan=3, sticky="e")
        
        # Add Entry
        self.batch, self.name, self.width, self.gauge, self.gap, self.clearance = self.create_entry_tab1(self)

        self.gauge.bind("<KeyRelease>", lambda event, label_num=self.gauge, box_sec=self.gap, out=self.clearance: tkb.calculator_key_release(event, "mult", label_num , box_sec, out))
        self.gap.bind("<KeyRelease>", lambda event, label_num=self.gap, box_sec=self.gauge, out=self.clearance: tkb.calculator_key_release(event, "mult", label_num , box_sec, out))
        self.clearance.bind("<KeyRelease>", lambda event, label_num=self.clearance, box_sec=self.gauge, out=self.gap: tkb.calculator_key_release(event, "div", label_num , box_sec, out))

        # Add Buttons
        self.unit = tb.Combobox(self.tab1, values=['Milimeter (mm)', 'Inches (in)'], width=15, state="readonly")
        self.unit.set('Milimeter (mm)')
        self.unit.grid(row=7, column=4)
        self.submit = tb.Button(self.tab1, command=self.submit_tab1, text="submit").grid(row=8, column=4)
        self.clear = tb.Button(self.tab1, command=self.clear_tab1, text="Clear").grid(row=8, column=2)


        # Add Tab1 Expansion after Submit
        self.tab1_expand = tb.Frame(self.bg_img)
        self.tab1_expand_dash = tb.Frame(self.tab1_expand)
        self.tab1_expand_table = tb.Frame(self.tab1_expand)
        self.tab1_expand_dash.grid(row=0, column=6, rowspan=4, padx=25)
        self.tab1_expand_table.grid(row=4, column=6, rowspan=8, padx=25)
        self.dash = tkb.Dash_Tab1(self.tab1_expand_dash)
        self.table = tkb.Tab1_Table(self.tab1_expand_table)
        self.update = tb.Button(self.tab1_expand_dash, text="Add Strips", command= lambda a = self.tab1_expand_table: self.update_strip(a)).grid(row=4, column=0)
        self.tab1_expand.grid_remove()


        
        # ---------------------------------- Add to tab 2 ---------------------------------------------
        label2 = tb.Label(self.tab2, text="This is Tab 2").grid(row=0, column=0)


    # Creation of Entry for Tab 1 ------------------------------------------
    # Submit Button function
    def submit_tab1(self):
        batch = self.batch.get()
        name = self.name.get()
        width = self.width.get()
        gauge = self.gauge.get()
        gap = self.gap.get()
        clearance = self.clearance.get()
        unit = self.unit.get()
        self.tab1_expand.grid(row=1, column=6, rowspan=20, padx=25)
        self.dash.display_converted_units([width, gauge, clearance, unit])

    # Enter Key - Submit function 
    def enter_key_tab1(self, event):
        self.submit_tab1()
    

    def create_entry_tab1(self, event):
        self.a = {}
        numeric = [True, False, True, True, True, True]
        for i in range(1, 7):
            self.a[i] = tb.Entry(self.tab1)
            self.a[i].grid(row=i, column=4, sticky="w")
            self.a[i].bind("<Down>", tkb.input_frame_down)
            self.a[i].bind("<Up>", tkb.input_frame_up)
            self.a[i].bind("<Return>", self.enter_key_tab1)
            if numeric[i - 1] == True:
                key_stroke_validation = self.a[i].register(tkb.correct_int)
                self.a[i].config(validate="key", validatecommand=(key_stroke_validation, '%P'))
                self.a[i].insert(0, 0)
        return [self.a[1], self.a[2], self.a[3], self.a[4], self.a[5], self.a[6]]

    
    def clear_tab1(self):
        a = [self.batch, self.name, self.width, self.gauge, self.gap, self.clearance]
        self.tab1_expand.grid_remove()
        for i in a:
            i.delete(0, tb.tk.END)
            i.insert(0, 0)
        return

    def update_strip(self, frame):
        #add_row = int(self.dash.strip_num.get())
        self.table.add_row(frame)

        #self.table = tkb.Table_tab1(self.tab1_expand_table, ROWS=4 + add_row)










# Define theme and create App
root = tb.Window(themename='superhero')
app = Window_main(root)


app.root.mainloop()