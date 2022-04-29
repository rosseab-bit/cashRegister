# -*- coding: utf-8 -*-
import sqlite3
import time


class dbSqlite:
    def __init__(self):
        self.sqliteConnection=sqlite3.connect('database/db.sql')

    def insertDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            self.sqliteConnection.commit()
            return 'out: Insert success'
        except:
            return 'error: query not found'

    def selectDB(self, query):
        print(query)
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            return cur.fetchall()
        except:
            return 'error: query not found'

    def updateDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            self.sqliteConnection.commit()
            return 'out: Update success'
        except:
            return 'error: query not found'

    def deleteDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            self.sqliteConnection.commit()
            return 'out: Delete success'
        except:
            return 'error: query not found'

    def updateStock(self, productos):
        print('Productos desde Update')
        print(productos)
        cur=self.sqliteConnection.cursor()
        for item in productos:
            updateQuery='update Stock set Stock=Stock-%s where Codigo=%s;'%(item[6], item[1])
            print(updateQuery)
            cur.execute(updateQuery)
            self.sqliteConnection.commit()
        return 'out: Update success'

    def putVentas(self, productos):
        dateVenta=time.strftime("%d%m%Y")
        cur=self.sqliteConnection.cursor()
        for item in productos:
            precioTotal=item[3]*float(item[6])
            query='insert into Ventas (Codigo, Producto, Precio, Fecha, Cantidad) values (%s, %s, %s, %s, %s)'%(item[5], item[1], precioTotal, dateVenta, item[6])
            cur.execute(query)
            self.sqliteConnection.commit()
        return 'Insert Succes'

    def deleteItemStock(self, item):
        cur=self.sqliteConnection.cursor()
        delItem="delete from Stock where Codigo=%s"%(item)
        cur.execute(delItem)
        self.sqliteConnection.commit()
        return 'out: delete success'
