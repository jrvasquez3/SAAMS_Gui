'''Author: Jose R Vasquez Perez'''

import ttkbootstrap as tb
import tkbuilder as tkb
from ttkbootstrap.scrolled import ScrolledFrame as Sf
import csv


class assembly(tb.Frame):
    def __init__(self, parent, *args, **kwargs):
        tb.Frame.__init__(self, parent, *args, **kwargs)
        self.table_frame = tb.Frame(self)
        self.dash_frame = tb.Frame(self)
        self.dash_frame.grid(row=0, column=6)
        self.table_frame.grid(row=4, column=6)

        self.dash = tkb.Dash_Tab1(self.dash_frame)
        self.table = tkb.Tab1_Table(self.table_frame)
        self.add_strip = tb.Button(self.dash_frame, text="Add Strip", command= lambda a = self.table_frame: self.update_strip(a)).grid(row=4, column=0)

    def update_strip(self, frame):
        self.table.add_row(frame)


        
  