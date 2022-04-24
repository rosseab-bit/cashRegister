# -*- coding: utf-8 -*-
import json
import sys
import sqlite3
import os
import time
from tkinter import ttk
from tkinter import *
from packages.dbSqlite import dbSqlite
import tkinter.font as tkFont

class cashRegister:
    def __init__(self, window):
        self.window=window
        window.title('cashRegister')
        window.attributes('-fullscreen', True)
        frame=LabelFrame(window, text="Registrar")
        frame.grid(row=0, column=0, columnspan=2, pady=10)
        window.bind('<Return>', self.addItem)
        # input products
        #
        Label(frame, text="Codigo").grid(row=1, column=0)
        self.inputCode=Entry(frame)
        self.inputCode.grid(row=1, column=1)
        self.inputCode.focus()
        # input count
        #
        Label(frame, text="Cantidad").grid(row=2, column=0)
        self.inputCount=Entry(frame)
        self.inputCount.grid(row=2, column=1)
        self.inputCount.insert(10, 1)
        ttk.Button(frame, text='Agregar', command=self.addManual).grid(row=3, columnspan=2, sticky= W + E)

        self.message = Label(window, text = '', fg = 'red')
        self.message.grid(row=2, column=0, columnspan=3, sticky = W + E)
        # listado de productos
        # Add a Treeview widget
        frameTree=LabelFrame(window, text="Detalle")
        #
        frameTree.grid(row=7, column=0, columnspan=6, pady=5)
        self.tree = ttk.Treeview(frameTree, column=("c0", "c1", "c2", "c3"), show='headings', height=30)
        self.tree.grid(row=0)
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="Producto")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Cantidad")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="Precio")
        self.tree.column("# 4", anchor=CENTER)
        self.tree.heading("# 4", text="Codigo")
        fontStyle=tkFont.Font(family="Lucida Grande", size=30)
        self.total=Label(window, text='Total: $ 0', font=fontStyle)
        self.total.grid(row=0, column=3)
        ttk.Button(window, text='Cancelar compra', command=self.dellAll).grid(row=2, column=3, columnspan=2, sticky= W + E)
        ttk.Button(frameTree, text='Borrar', command=self.dellItem).grid(row=9, column=0, padx=10, columnspan=3, sticky= W + E)
        ttk.Button(frameTree, text='Cobrar', command=self.setCharge).grid(row=10, column=0, pady=10, padx=10, columnspan=3, sticky= W + E)
        verscrlbar = ttk.Scrollbar(frameTree,
                           orient ="vertical",
                           )

        # lista de compras
        self.listCompra=[]

        # lista de stock
        self.stockList=[]

        # codigo de venta
        self.codigoVenta=int(time.strftime("%d%m%Y%H%M%S"))

    def detailItems(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for product in self.listCompra:
            self.tree.insert('', 1, text='', value=(product[4], product[6], product[3], product[1]))

    def addItem(self, event):
        self.message['text']=''
        #product=(self.inputCode.get(), self.inputCount.get())
        if len(self.inputCode.get())==0 or len(self.inputCount.get())==0:
            self.message['text']='Error: Codigo inexistente o producto sin stock.'
            return
        queryProduct='select * from Stock where Stock>%s and Codigo=%s;'%(self.inputCount.get(), self.inputCode.get())
        executeDB=dbSqlite()
        queryResult=executeDB.selectDB(queryProduct)
        if queryResult:
            add_code=list(queryResult[0])
            add_code.append(self.codigoVenta)
            add_code.append(self.inputCount.get())
            product=tuple(add_code)
            self.listCompra.append(product)
            print(product)
        else:
            print('producto sin stock o inexistente.')
            self.message['text']='Error: Codigo inexistente o producto sin stock.'
            self.inputCode.delete(0, END)
            self.inputCount.delete(0, END)
            self.inputCount.insert(10, 1)
        self.detailItems()
        total=0
        for product in self.listCompra:
            subTotal=product[3]*float(product[6])
            total=total+subTotal
        self.total['text']='Total: '+str(round(total, 2))
        self.inputCode.delete(0, END)
        self.inputCount.delete(0, END)
        self.inputCount.insert(10, 1)
        self.inputCode.focus()

    def addManual(self):
        self.message['text']=''
        if len(self.inputCode.get())==0 or len(self.inputCount.get())==0:
            self.message['text']='Error: Codigo inexistente o producto sin stock.'
            return
        product=(self.inputCode.get(), self.inputCount.get())
        queryProduct='select * from Stock where Stock>%s and Codigo=%s;'%(self.inputCount.get(), self.inputCode.get())
        executeDB=dbSqlite()
        queryResult=executeDB.selectDB(queryProduct)
        if queryResult:
            add_code=list(queryResult[0])
            add_code.append(self.codigoVenta)
            add_code.append(self.inputCount.get())
            product=tuple(add_code)
            self.listCompra.append(product)
            print(product)
        else:
            print('producto sin stock o inexistente.')
            self.message['text']='Error: Codigo inexistente o producto sin stock.'
            self.inputCode.delete(0, END)
            self.inputCount.delete(0, END)
            self.inputCount.insert(10, 1)
        self.detailItems()
        total=0
        for product in self.listCompra:
            subTotal=product[3]*float(product[6])
            total=total+subTotal
        self.total['text']='Total: $ '+str(round(total, 2))
        self.inputCode.delete(0, END)
        self.inputCount.delete(0, END)
        self.inputCount.insert(10, 1)
        self.inputCode.focus()

    def dellItem(self):
        self.message['text']=''
        if len(self.inputCode.get())==0 or len(self.inputCount.get())==0:
            self.message['text']='Error: Codigo inexistente o producto sin stock.'
            return
        print(self.tree.item(self.tree.selection())['values'])
        list_temp=[]
        for product in self.listCompra:
            if self.tree.item(self.tree.selection())['values'][3] == product[1]:
                self.listCompra.remove(product)

        self.detailItems()
        if len(self.listCompra)>0:
            total=0
            for product in self.listCompra:
                subTotal=product[3]*float(product[6])
                total=total+subTotal
            self.total['text']='Total: $ '+str(round(total,2))
            self.inputCode.focus()
        else:
            self.total['text']='Total: $ 0'

        return 'ok'

    def setCharge(self):
        # envio la venta a la tabla de ventas de la base de datos
        updateVentas=dbSqlite()
        updateVentas.putVentas(self.listCompra)
        #
        # actualizo tabla de stock
        upStock=dbSqlite()
        upStock.updateStock(self.listCompra)
        #
        # luego de cobrar vacio todo para un nuevo cobro.
        self.listCompra=[]
        self.detailItems()
        self.codigoVenta=int(time.strftime("%d%m%Y%H%M%S"))
        self.total['text']='Total: $ 0'
        self.inputCode.delete(0, END)
        self.inputCount.delete(0, END)
        self.inputCount.insert(10, 1)
        self.inputCode.focus()
        return 'update succes'

    def dellAll(self):
        self.total['text']='Total: $ 0'
        self.inputCode.delete(0, END)
        self.inputCount.delete(0, END)
        self.inputCount.insert(10, 1)
        self.inputCode.insert(10, 1)
        self.listCompra=[]
        self.detailItems()
        self.inputCode.focus()
        return 'Dell all'
