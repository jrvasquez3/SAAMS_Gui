import ttkbootstrap as tb



class background_image:
    def __init__(self, window_name, bg_image_name, bg_width, bg_height ):
        self.bg_image = tb.PhotoImage(file=bg_image_name)
        self.place = tb.Canvas(window_name, width=bg_width, height= bg_height )
        self.place.pack(fill="both", expand=True)
        self.place.create_image(0,0, image= self.bg_image, anchor="nw") 


# Function event to allow user to move between widgets using UP and DOWN keys
# To call, use "bind()" function. Example: .bind("<Up>")
def input_frame_down(event):
    event.widget.tk_focusNext().focus_set()
    return

def input_frame_up(event):
    event.widget.tk_focusPrev().focus_set()
    return

def key_input(object, event):
    print(object)
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
