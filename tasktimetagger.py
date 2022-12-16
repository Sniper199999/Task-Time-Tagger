import time
from tkinter import *
import win32con
from win32gui import GetWindowLong, FindWindow, SetWindowLong, SetWindowPos


class TagTime:
    def __init__(self, window=None, line_color_1="yellow", line_color_2 ="red", line_thickness=10, line_dash=None, transparency=1, animate = False, line_orientation="top"):
        self.window_title = "Line"      #Used to get hwnd
        self.target_color = "#660033"   #Check for this color in tkinter window to make UI components transparent
        
        self.line_color_1 = line_color_1
        self.line_color_2 = line_color_2
        self.line_thickness = line_thickness
        self.line_dash = line_dash
        self.transparency = transparency
        self.animate = animate
        self.line_orientation = line_orientation
        self.progressbar = 0
        self.window = window

        self.CreateOverlay()
        self.SetClickThrough()
        
        if self.animate:
            self.color_range = self.GenerateColors()
            self.AnimateLine()

    def CreateOverlay(self):
        self.window.attributes('-alpha', transparency)
        self.window.attributes('-fullscreen', True)
        self.window.configure(background=self.target_color)
        self.window.wm_attributes('-transparent', self.target_color,'-topmost', 1)
        #self.window.overrideredirect(True)     #Use this to hide from TaskBar
        self.window.update()
        self.max_height, self.max_width = self.window.winfo_height(), self.window.winfo_width()
        self.window.title("Line")

        #Draw Line
        self.canvasScreen = Canvas(self.window, width = self.max_width, height = self.max_height, bg = self.target_color, highlightthickness=0, borderwidth=0)    
        self.canvasScreen.pack()
        if line_orientation == "top":
            line_coordinates = (0, 0, self.max_width, 0)
        elif line_orientation == "bottom":
            line_coordinates = (0, self.max_height, self.max_width, self.max_height)
        elif line_orientation == "right":
            line_coordinates = (self.max_width, 0, self.max_width, self.max_height)
        elif line_orientation == "left":
            line_coordinates = (0, 0, 0, self.max_height)
        self.line = self.canvasScreen.create_line(*line_coordinates, fill = self.line_color_1, width=self.line_thickness, dash=self.line_dash)

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
            #Generate range of colors between 2 colors
            start_color = Color(self.line_color_1)
            end_color = Color(self.line_color_2)
            color_range = list(start_color.range_to(end_color, 50))     
            return color_range
        except:
            import sys
            sys.exit("ERROR: pip install colour package or do animate = False")
        

    #Can animate almost any properties of line
    def AnimateLine(self):
        def ColorIterator(color):
            self.canvasScreen.itemconfig(self.line, fill= color)
            time.sleep(0.03)
            self.window.update()

        for i in self.color_range:
            ColorIterator(i)

        for i in reversed(self.color_range):
            ColorIterator(i)

        self.canvasScreen.after(1, self.AnimateLine)  #(delay ms, fuctions like non blocking while loop)


if __name__ == "__main__":
    #Dash Patterns:     https://stackoverflow.com/questions/41796792/tkinter-canvas-dash-option-is-not-behaving-as-expected
    # -dash .     → -dash {2 4}
    # -dash -     → -dash {6 4}
    # -dash -.    → -dash {6 4 2 4}
    # -dash -..   → -dash {6 4 2 4 2 4}
    # -dash {. }  → -dash {2 8}             Not supported in Windows
    # -dash ,     → -dash {4 4}             Not supported in Windows
    dash_patterns = [None, (2,4), (6,4), (6,4,2,4), (6,4,2,4,2,4), (2,8), (4,4)]
    line_dash = dash_patterns[0]

    orientations = ["top", "bottom", "right", "left"]
    line_orientation = orientations[3]

    line_thickness = 10
    line_color_1 = "yellow"     #Hex
    line_color_2 = "red"        #Hex
    transparency = 0.9          #From 0 to 1
    animate = True

    window = Tk()
    TagTime(window=window, line_color_1=line_color_1, line_color_2 = line_color_2,
                line_thickness=line_thickness, line_dash=line_dash, transparency=transparency, 
                line_orientation=line_orientation, animate=animate)

    window.mainloop()