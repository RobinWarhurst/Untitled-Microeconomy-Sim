# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 20:42:53 2024

@author: Clive
"""

# this code creates the UI

# concepts:

# window - the window that opens
# widget - component of the UI that user can interact with 
    # there are a lot of cool widgets to be discovered!   
# signals - notifications emitted by widgets when something happens (such as button press)
# slots - receivers of signals (like functions, methods, or other widgets)
# layout - how the widgets are arranged in the window


from PyQt6 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

# create a new class called MainWindow with WtWidgets.QMainWindow as the parent class

class MainWindow(QtWidgets.QMainWindow):

    # the __init__ function is called when the class is initiated
    # it is used to assign values to object properties
    
    def __init__(self, *args, **kwargs):
        
        # self represents the instance of the class and can be used to access attributes and methods of the class
        # *args is used in function definitions to pass a variable number of arguments to the function
        # *kwargs is used in function definitions to pass a keyworded, variable-length argument list
        
        # the super function refers to the parent class
        # it allows you to call methods defined in the superclass from the subclass
        
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # creates an instance of the PlotWidget object (a special Widget) called graphWidget
        # this widget can be accessed because the term self has been used
        
        self.graphWidget = pg.PlotWidget()        
        # now sets this widget as the central widget of the window
        self.setCentralWidget(self.graphWidget)

        # create two lists called hour and temperature
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        # this plots the lists on the widget
        self.graphWidget.plot(hour, temperature)

# creates a new function called main

def main():
    
    # create instance of QApplication called app
    app = QtWidgets.QApplication(sys.argv)
    
    # creates instance of MainWindow (defined above) called main
    main = MainWindow()
    
    # makes the widget visible (invisible by default)
    main.show()
    
    # exits the interpreter and starts the event loop
    sys.exit(app.exec())

# https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/

if __name__ == '__main__':
    main()

# plotWidget basics 

# setBackground method sets the colour of the widget's background
# self.graphWidget.setBackground((100,50,255)) 

# lines in the widget are drawn using the QPen object
# pen = pg.mkPen(color=(255, 0, 0))
# self.graphWidget.plot(hour, temperature, pen=pen)
# the appearance of the line can be changed
# pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)


