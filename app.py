# -*- coding: utf-8 -*-
import json
import sys
import os
import time
from tkinter import ttk
from tkinter import *
# import from packages
from packages.tkmain import cashRegister
#from PIL import ImageTk, Image

if __name__=='__main__':
    window=Tk()
    app=cashRegister(window)
    window.mainloop()
