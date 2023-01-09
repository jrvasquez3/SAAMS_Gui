import ttkbootstrap as tb
from tkinter import filedialog
import subprocess
import openpyxl as op


class ToolManagement(tb.Frame):
    def __init__(self, parent, *args, **kwargs):
        tb.Frame.__init__(self, parent, *args, **kwargs)
        self.label = tb.Label(self, text="Enter Link")
        self.label.grid(row=0, column=1)
        self.link = tb.Entry(self)
        self.link.insert(0, "default_values\\tool_management.xlsx")
        self.link.grid(row=1, column=1)
        self.browse = tb.Button(self, text="Browse", command=self.browse_file)
        self.browse.grid(row=1, column=2)
        self.open_excel = tb.Button(self, text="Open in Excel", command=self.open_file)
        self.open_excel.grid(row=2, column=1)
        self.open = tb.Button(self, text="Open", command=self.open_here)
        self.open.grid(row=2, column=2)

        self.notebook = tb.Notebook(self)
        self.sheet1 = tb.Frame(self.notebook)
        self.sheet2 = tb.Frame(self.notebook)
        self.sheet3 = tb.Frame(self.notebook)
        self.notebook.add(self.sheet1, text="Knife")
        self.notebook.add(self.sheet2, text="Rubber")
        self.notebook.add(self.sheet3, text="Tooling")
        self.sheet_list = [self.sheet1, self.sheet2, self.sheet3]

        self.notebook.grid(row=4, column=1)


    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.link.delete(0, tb.tk.END)
        self.link.insert(0, file_path)

    def open_file(self):
        link = self.link.get()
        print(link)
        subprocess.run(["C:\\Program Files\\Microsoft Office\\root\\Office16\\excel.exe", link ])

    def open_here(self):
        link = self.link.get()
        wb = op.load_workbook(link)
        k = 0
        for sheet in wb.worksheets:
            print(sheet.title)
            a = [self.sheet1, self.sheet2, self.sheet3]
            print(k)
            sheet_name = wb.get_sheet_by_name(sheet.title)
            i = 4
            for row in sheet_name.rows:
                j = 1
                row_entry = []
                for cell in row:
                    entry = tb.Entry(a[k])
                    entry.insert(0, cell.value)
                    entry.grid(row=i, column=j)
                    row_entry.append(entry)
                    j = j + 1
                i = i + 1
            k = k + 1
                

