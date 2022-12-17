import time
from tkinter import *
import win32con
from win32gui import GetWindowLong, FindWindow, SetWindowLong, SetWindowPos

class TagTime:
    def __init__(self, window=None, line_color_1="yellow", line_color_2="red", 
                line_thickness=10, line_dash=None, transparency=1, animate=False, 
                line_orientation="top", timer = "00:00:00"):
        self.window_title = "Line"  # Used to get hwnd
        self.target_color = "#660033"   # Check for this color in tkinter window to make UI components transparent

        self.line_color_1 = line_color_1
        self.line_color_2 = line_color_2
        self.line_thickness = line_thickness
        self.line_dash = line_dash
        self.transparency = transparency
        self.animate = animate
        self.line_orientation = line_orientation

        self.timer = sum([a*b for a,b in zip([3600,60,1], map(int,timer.split(':')))])
        
        self.progressbar = 0
        self.times_up = False

        self.window = window

        self.CreateOverlay()
        self.SetClickThrough()

        if self.animate:
            self.color_range = self.GenerateColors()
            self.progress_block = int(self.line_coordinates[2] / self.timer)
            print(self.progress_block)
            self.start_time = time.time()
            self.ProgressBar()
            self.AnimateLine()
            

    def ProgressBar(self):
        current_time = time.time()
        seconds_passed = current_time - self.start_time
        percent_completed = (seconds_passed/self.timer) * 100
        progressbar_width = int((percent_completed/100)*self.line_coordinates[2])
        #print("Percent:{} Width:{}".format(percent_completed, progressbar_width))

        self.line_coordinates[0][self.line_coordinates[1]] = progressbar_width
        self.canvasScreen.coords(self.line, *self.line_coordinates[0])
        if percent_completed > 100:
            print("Time is up")
            self.times_up = True
        else:
            self.canvasScreen.after(100, self.ProgressBar)


    def CreateOverlay(self):
        self.window.attributes('-alpha', transparency)
        self.window.attributes('-fullscreen', True)
        self.window.configure(background=self.target_color)
        self.window.wm_attributes('-transparent', self.target_color, '-topmost', 1)
        # self.window.overrideredirect(True)     #Use this to hide from TaskBar
        self.window.bind("<Control-w>", self.quit)
        self.window.update()
        self.max_height, self.max_width = self.window.winfo_height(), self.window.winfo_width()
        self.window.title("Line")

        # Draw Line
        self.canvasScreen = Canvas(self.window, width=self.max_width, height=self.max_height,
                                   bg=self.target_color, highlightthickness=0, borderwidth=0)
        self.canvasScreen.pack()
        if self.line_orientation == "top":
            self.line_coordinates = [[0, 0, self.max_width, 0], 2, self.max_width]
        elif self.line_orientation == "bottom":
            self.line_coordinates = [[0, self.max_height, self.max_width, self.max_height], 2, self.max_width]
        elif self.line_orientation == "right":
            self.line_coordinates = [[self.max_width, 0, self.max_width, self.max_height], 3, self.max_height]
        elif self.line_orientation == "left":
            self.line_coordinates = [[0, 0, 0, self.max_height], 3, self.max_height]

        self.line = self.canvasScreen.create_line(*self.line_coordinates[0], fill=self.line_color_1, 
                                                    width=self.line_thickness, dash=self.line_dash)

    def SetClickThrough(self):
        hwnd = FindWindow(None, self.window_title)
        # Get window style and perform a 'bitwise or' operation to make the style layered and transparent, achieving the clickthrough property
        l_ex_style = GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        l_ex_style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        SetWindowLong(hwnd, win32con.GWL_EXSTYLE, l_ex_style)
        # Set the window to appear always on top
        SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)

    def GenerateColors(self):
        try:
            from colour import Color
            # Generate range of colors between 2 colors
            start_color = Color(self.line_color_1)
            end_color = Color(self.line_color_2)
            color_range_list = list(start_color.range_to(end_color, 30))
            color_range = color_range_list.copy()
            color_range_list.reverse()
            print(color_range)
            color_range = color_range + color_range_list
            print(color_range)
            return color_range
        except:
            import sys
            sys.exit("ERROR: pip install colour package or do animate = False")

    # Can animate almost any properties of line
    def AnimateLine(self):
        def ColorIterator(color):
            self.canvasScreen.itemconfig(self.line, fill=color)
            time.sleep(0.03)
            self.window.update()    #To update the GUI
           
        for i in self.color_range:
            ColorIterator(i)
            #self.canvasScreen.after(1)

        self.canvasScreen.after(1, self.AnimateLine)    # (delay ms, fuctions like non blocking while loop)


    def quit(self, event=None):
        print("quiting...", event)
        self.window.quit()




if __name__ == "__main__":
    # Dash Patterns:     https://stackoverflow.com/questions/41796792/tkinter-canvas-dash-option-is-not-behaving-as-expected
    # -dash .     → -dash {2 4}
    # -dash -     → -dash {6 4}
    # -dash -.    → -dash {6 4 2 4}
    # -dash -..   → -dash {6 4 2 4 2 4}
    # -dash {. }  → -dash {2 8}             Not supported in Windows
    # -dash ,     → -dash {4 4}             Not supported in Windows
    dash_patterns = [None, (2, 4), (6, 4), (6, 4, 2, 4), (6, 4, 2, 4, 2, 4), (2, 8), (4, 4)]
    line_dash = dash_patterns[0]

    orientations = ["top", "bottom", "right", "left"]
    line_orientation = orientations[0]

    line_thickness = 10
    line_color_1 = "yellow"     # Hex
    line_color_2 = "red"        # Hex
    transparency = 0.9          # From 0 to 1
    animate = True              # Colour module required
    timer = "00:04:23"          # Hour:Min:Sec

    
    window = Tk()
    TagTime(window=window, line_color_1=line_color_1, line_color_2=line_color_2,
            line_thickness=line_thickness, line_dash=line_dash, transparency=transparency,
            line_orientation=line_orientation, animate=animate, timer=timer)



    window.mainloop()
   
