from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from matplotlib.widgets import Slider, Button
import numpy as np
import sys
from src.robot import *
from src.utils import *

FACECOLOR = '#2D3536'
FG = '#B8D8DB'
BG = '#424E4F'
TROUGHCOLOR = '#83999C'

class GUI:
    def __init__(self, master):
        # Window design
        self.master = master
        self.master.title("Robot ABB IRB 140")
        self.master.config(bg=FACECOLOR)
        self.master.resizable(width=False, height=False)
        self.master.geometry("1200x600+80+80")
        self.master.tk.call('wm', 'iconphoto', master._w,
                            PhotoImage(file='images/abb-irb140-logo.png'))

        self.fig = Figure(figsize=(7, 7), dpi=110, facecolor=FACECOLOR)
        self.fig.clf()

        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=FACECOLOR)
        self.robot = abb_irb_140()
        self.robot.plot_robot(self.ax, home=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().place(x=-60, y=-100)
        self.canvas.draw()

        self.theta_1 = Scale(master, from_=-180, to=180, tickinterval=15,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 1", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_1.grid(column=1, row=0, padx=680, pady=10)

        self.theta_2 = Scale(master, from_=25, to=110, tickinterval=5,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 2", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_2.grid(column=1, row=1, padx=680, pady=10)
        self.theta_2.set(90)

        self.theta_3 = Scale(master, from_=-230, to=50, tickinterval=15,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 3", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_3.grid(column=1, row=2, padx=680, pady=10)

        self.theta_4 = Scale(master, from_=-200, to=200, tickinterval=20,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 4", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_4.grid(column=1, row=3, padx=680, pady=10)

        self.theta_5 = Scale(master, from_=-115, to=115, tickinterval=15,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 5", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_5.grid(column=1, row=4, padx=680, pady=10)

        self.theta_6 = Scale(master, from_=-400, to=400, tickinterval=40,
                        length=500, resolution=1, showvalue=0,
                        orient='horizontal', command=self.plot,
                        label="THETA 6", sliderrelief=FLAT,
                        bg=BG, fg=FG, troughcolor=TROUGHCOLOR,
                        highlightbackground=BG)
        self.theta_6.grid(column=1, row=5, padx=680, pady=10)

    def plot(self, event):
        self.robot.set_angles([
            self.theta_1.get(),
            self.theta_2.get(),
            self.theta_3.get(),
            self.theta_4.get(),
            self.theta_5.get(),
            self.theta_6.get()
        ])

        self.ax.clear()
        self.robot.plot_robot(self.ax, home=False, facecolor=FACECOLOR)
        self.canvas.draw()

    def exit(self):
        self.master.quit()
        sys.exit()

def main():
    root = Tk()
    rk = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
