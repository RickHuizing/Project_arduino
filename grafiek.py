from tkinter import *
from random import randint
import time
class Plot():
    def __init__(self, master, values, width=600, height=300, borderMarg=30, xAxSpacing=25, yAxisinterval=10, xAxisinterval=10, yAxSpacing = 25, YaxisSpots= 10):
        self.frameWidth = width
        self.frameHeight = height

        self.borderMarge = borderMarg
        self.xAxisSpacing = xAxSpacing
        self.yAxisSpacing = yAxSpacing

        self.xAxisInterval = xAxisinterval
        self.yAxisInterval = yAxisinterval

        self.values = values
        self.maxEntries = len(values)-1
        self.numberOfYaxisSpots = round(max(self.values.values())/self.yAxisInterval)

        # init global vars
        self.s = 0
        self.x2 =  self.borderMarge
        self.y2 = self.value_to_y(randint(0, 100))

        self.canvas = Canvas(master, width= self.frameWidth, height= self.frameHeight, bg='white')  # 0,0 is top left corner
        self.canvas.grid(row=1, column=0, columnspan=4)

        self.canvas.create_line( self.borderMarge,  self.frameHeight -  self.borderMarge,  self.borderMarge + self.maxEntries*self.xAxisSpacing,  self.frameHeight -  self.borderMarge, width=2)  # x-axis
        self.canvas.create_line( self.borderMarge,  self.frameHeight -  self.borderMarge,  self.borderMarge,  self.frameHeight- self.borderMarge-self.numberOfYaxisSpots*self.yAxisSpacing, width=2)  # y-axis

        # x-axis
        #for i in range(self.maxEntries+1):
        i=0
        for y in self.values:
            x =  self.borderMarge + (i * self.xAxisSpacing)
            self.canvas.create_line(x,  self.frameHeight- self.borderMarge, x,  self.frameHeight- self.borderMarge-self.numberOfYaxisSpots*self.yAxisSpacing, width=1, dash=(2, 5))
            self.canvas.create_text(x,  self.frameHeight- self.borderMarge, text='%s' % (y), anchor=N)
            i+=1

        # y-axis
        for i in range(self.numberOfYaxisSpots+1):
            y =  self.frameHeight- self.borderMarge - (i * self.yAxisSpacing)
            self.canvas.create_line( self.borderMarge, y,  self.borderMarge+self.maxEntries*self.xAxisSpacing, y, width=1, dash=(2, 5))
            self.canvas.create_text( self.borderMarge-10, y, text='%s' % (self.yAxisInterval * i), anchor=E)

        self.canvas.after(300, self.step)
    def step(self):
        for x in self.values:
            x1 = self.x2
            y1 = self.y2
            self.x2 =  self.borderMarge + self.s * self.xAxisSpacing
            self.y2 = self.frameHeight-(self.values[x]/self.yAxisInterval*self.yAxisSpacing)-self.borderMarge
            self.canvas.create_line(x1, y1, self.x2, self.y2, fill='blue', tags='temp')
            # print(s, x1, y1, x2, y2)
            self.s = self.s + 1


    def value_to_y(self, val):
        return self.frameHeight - self.borderMarge - self.yAxisSpacing / self.numberOfYaxisSpots * val


