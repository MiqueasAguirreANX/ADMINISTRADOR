from tkinter import *
import tkinter.ttk as ttk
import sqlite3 as sql
import os
import os.path as op
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter.messagebox as msj

# clases -------------------------------------------------------------------

class producto():
    def __init__(self, categoria, marca, modelo, precio, unidades):
        self.categoria = categoria
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.unidades = unidades

class producto_id():
    def __init__(self, id, categoria, marca, modelo, precio, unidades):
        self.id = id
        self.categoria = categoria
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.unidades = unidades


path_inventario = "inventario.db"
path_ventas = "ventas.db"

# funciones ----------------------------------------------------------------

# funciones de inventario

def get_lista():
    conn = sql.connect(path_inventario)
    c = conn.cursor()
    c.execute("SELECT * FROM INVENTARIO")
    base_lista = c.fetchall()
    conn.commit()
    conn.close()
    return base_lista
    
def borrar_elemento(id_del):
    if id_del != "" and int(id_del) > 0:
        conn = sql.connect(path_inventario)
        c = conn.cursor()
        c.execute(f"DELETE FROM INVENTARIO WHERE ID={id_del}")
        conn.commit()
        conn.close()

def crear_tabla():
    if op.exists(path_inventario):
        pass
    else:
        conn = sql.connect(path_inventario)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE
            INVENTARIO ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria VARCHAR(50),
                marca VARCHAR(50),
                modelo VARCHAR(50),
                precio REAL,
                unidades INTEGER,
                anio INTEGER,
                mes INTEGER,
                dia INTEGER)
            ''')
        conn.commit()
        conn.close()

def reinicio():
    if op.exists(path_inventario):
        os.remove(path_inventario)

    crear_tabla()
    for i in treeview.get_children():
        treeview.delete(i)

    resetear()

def actualizar():


    base_lista = get_lista()

    if len(base_lista)>0:
        num = 0
        for item in base_lista:
            treeview.insert('', str(num), str(item[0]), text=str(item[0]))
            treeview.set(str(item[0]), 'categoria', item[1])
            treeview.set(str(item[0]), 'marca', item[2])
            treeview.set(str(item[0]), 'modelo', item[3])
            treeview.set(str(item[0]), 'precio', item[4])
            treeview.set(str(item[0]), 'unidades', item[5])
            num += 1


    resetear()

def count_lista():
    base_lista = get_lista()
    return len(base_lista)

def resetear():
    base_lista = get_lista()
    cat.delete(0, END)
    mar.delete(0, END)
    model.delete(0, END)
    pre.delete(0, END)
    uni.delete(0, END)

    try:
        lbl_cant["text"] = str(count_lista())
        n = 0.0;
        for i in base_lista:
            n = n + (i[4]*i[5])

        lbl_total["text"] = str(n)

    except:
        pass

    cat.focus()

def f_borrar(id_del):
    base_lista = get_lista()
    if count_lista()>0:
        flag = False
        for i in base_lista:
            if i[0] == int(id_del):
                flag = True

        if flag == True:
            borrar_elemento(id_del)
            treeview.delete(id_del)

    resetear()

def agregar_producto(prd):
    conn = sql.connect(path_inventario)
    c = conn.cursor()
    fecha = datetime.date.today()
    base = [prd.categoria, prd.marca, prd.modelo, prd.precio, prd.unidades, fecha.year, fecha.month, fecha.day]
    c.execute('''
        INSERT INTO 
        INVENTARIO
        VALUES
        ( NULL , ?, ?, ?, ?, ? , ?, ?, ?)
        ''', base)
    conn.commit()
    conn.close()

def f_guardar():
    categoria = cat.get()
    marca = mar.get()
    modelo = model.get()
    precio = pre.get()
    unidades = uni.get()

    if categoria != "" and marca != "" and precio != "" and unidades != "":
        if float(precio)>0 and int(unidades)>0: 
            agregar_producto(producto(categoria, marca, modelo, precio, unidades))
            lista = get_lista()

            treeview.insert('', str(len(lista)-1), str(lista[-1][0]), text=str(lista[-1][0]))
            treeview.set(str(lista[-1][0]), 'categoria', lista[-1][1])
            treeview.set(str(lista[-1][0]), 'marca', lista[-1][2])
            treeview.set(str(lista[-1][0]), 'modelo', lista[-1][3])
            treeview.set(str(lista[-1][0]), 'precio', lista[-1][4])
            treeview.set(str(lista[-1][0]), 'unidades', lista[-1][5])
        else:
            msj.showerror("PRECIO O UNIDAD INVALIDOS", "Porfavor introduzca precios y/o unidades positivos")
    else:
        msj.showerror("ERROR EN LOS DATOS", "Porfavor introduzca datos validos")

    resetear()

# funciones de ventas

def vf_cancelar():
    if len(carrito)>0:
        carrito.pop()
        treeview.delete(treeview_c.get_children()[-1])

def vvender():
    if len(carrito)>0:
        for i in carrito:
            vagregar_producto(i)
        
        for i in treeview_c.get_children():
            treeview_c.delete(i)

        carrito.clear()
        base_lista = get_lista()

        for i in treeview.get_children():
            treeview.delete(i)

        if len(base_lista)>0:
            num = 0
            for item in base_lista:
                treeview.insert('', str(num), str(item[0]), text=str(item[0]))
                treeview.set(str(item[0]), 'categoria', item[1])
                treeview.set(str(item[0]), 'marca', item[2])
                treeview.set(str(item[0]), 'modelo', item[3])
                treeview.set(str(item[0]), 'precio', item[4])
                treeview.set(str(item[0]), 'unidades', item[5])
                num += 1


        resetear()

    vresetear()

def vget_lista():
    conn = sql.connect(path_ventas)
    c = conn.cursor()
    c.execute("SELECT * FROM VENTAS")
    base_l = c.fetchall()
    conn.commit()
    conn.close()
    return base_l

def vborrar_elemento(id_del):
    if id_del != "" and int(id_del) > 0:
        conn = sql.connect(path_ventas)
        c = conn.cursor()
        c.execute(f"DELETE FROM VENTAS WHERE ID={id_del}")
        conn.commit()
        conn.close()

def vcrear_tabla():
    if op.exists(path_ventas):
        pass
    else:
        conn = sql.connect(path_ventas)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE
            VENTAS ( ID INTEGER,
                categoria VARCHAR(50),
                marca VARCHAR(50),
                modelo VARCHAR(50),
                precio REAL,
                unidades INTEGER,
                anio INTEGER,
                mes INTEGER,
                dia INTEGER)
            ''')
        conn.commit()
        conn.close()

def vreinicio():
    if op.exists("C:/Users/Miqueas/Python/ADMINISTRADOR/ventas.db"):
        os.remove("C:/Users/Miqueas/Python/ADMINISTRADOR/ventas.db")

    vcrear_tabla()
    for i in treeview_v.get_children():
        treeview_v.delete(i)
    for i in treeview_c.get_children():
        treeview_c.delete(i)

    vresetear()

def vactualizar():
    vbase_lista = vget_lista()

    if len(vbase_lista)>0:
        num = 0
        for item in vbase_lista:
            treeview_v.insert('', str(num), str(item[0]), text=str(item[0]))
            treeview_v.set(str(item[0]), 'categoria', item[1])
            treeview_v.set(str(item[0]), 'marca', item[2])
            treeview_v.set(str(item[0]), 'modelo', item[3])
            treeview_v.set(str(item[0]), 'precio', item[4])
            treeview_v.set(str(item[0]), 'unidades', item[5])
            num += 1


    vresetear()

def vcount_lista():
    ba = vget_lista()
    return len(ba)

def vresetear():
    vbase_lista = vget_lista()
    vid.delete(0, END)
    vpre.delete(0, END)
    vuni.delete(0, END)

    try:
        vlbl_cant["text"] = str(vcount_lista())
        n = 0.0;
        m = 0.0;
        for i in vbase_lista:
            n = n + (i[4]*i[5])
        for i in carrito:
            m = m + (i.precio*i.unidades)

        vlbl_total["text"] = str(n)
        vlbl_venta["text"] = str(m)

    except:
        pass

    vid.focus()

def vf_borrar(id_del):
    base_lista = vget_lista()
    if vcount_lista()>0:
        flag = False
        for i in base_lista:
            if i[0] == int(id_del):
                flag = True

        if flag == True:
            vborrar_elemento(id_del)
            treeview_v.delete(id_del)

    resetear()

def vagregar_producto(prd):
    conn = sql.connect(path_ventas)
    c = conn.cursor()
    fecha = datetime.date.today()
    base = (prd.id, prd.categoria, prd.marca, prd.modelo, prd.precio, prd.unidades, fecha.year, fecha.month, fecha.day)
    c.execute('''
                INSERT INTO 
                VENTAS
                VALUES
                ( ? , ?, ?, ?, ?, ? , ?, ?, ?)
            ''', base)
    item = obtener_producto(prd.id)
    conn.commit()
    conn.close()

    conn = sql.connect(path_inventario)
    c = conn.cursor()
    c.execute(f'''
                UPDATE INVENTARIO
                SET unidades={item.unidades-int(prd.unidades)}
                WHERE ID={prd.id}
            ''')
    conn.commit()
    conn.close()

    treeview_v.insert('', str(vcount_lista()-1), prd.id, text=prd.id)
    treeview_v.set(prd.id, 'categoria', prd.categoria)
    treeview_v.set(prd.id, 'marca', prd.marca)
    treeview_v.set(prd.id, 'modelo', prd.modelo)
    treeview_v.set(prd.id, 'precio', str(prd.precio))
    treeview_v.set(prd.id, 'unidades', str(prd.unidades))

def obtener_producto(id):
    if id == "":
        return False

    if int(id) <= 0 :
        return False

    conn = sql.connect(path_inventario)
    c = conn.cursor()
    c.execute(f"SELECT * FROM INVENTARIO WHERE ID={id}")
    item = c.fetchone()
    if type(item) == type(None):
        conn.commit()
        conn.close()
        return False
    
    conn.commit()
    conn.close()
    prd = producto_id(item[0], item[1], item[2], item[3], item[4], item[5])
    return prd

def agregar_carrito():
    id = vid.get()
    precio = vpre.get()
    unidades = vuni.get()
    prd = obtener_producto(id)

    if prd != False or prd.unidades >= int(unidades):
        carrito.append(producto_id(prd.id, prd.categoria, prd.marca, prd.modelo, precio, unidades))
        treeview_c.insert('', str(len(carrito)-1), prd.id, text=prd.id)
        treeview_c.set(prd.id, 'categoria', prd.categoria)
        treeview_c.set(prd.id, 'marca', prd.marca)
        treeview_c.set(prd.id, 'modelo', prd.modelo)
        treeview_c.set(prd.id, 'precio', str(precio))
        treeview_c.set(prd.id, 'unidades', str(unidades))
    else:
        msj.showinfo("Mensaje de aviso", message="Este item no se encuentra en el inventario o no hay suficiente cantidad")
    vresetear()

# funciones de datos

def seleccion(event):
    if count_lista()>0 or vcount_lista()>0:

        ventas = vget_lista()
        inventario = get_lista()
        
        global dfr_der
        global dfr_izq
        global datos_fr

        if event.widget.get() == "Enero":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 1:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 1:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Febrero":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 2:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 2:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Marzo":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 3:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 3:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Abril":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 4:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 4:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Mayo":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 5:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 5:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Junio":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 6:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 6:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Julio":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 7:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 7:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Agosto":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1, sticky='ns')

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 8:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 8:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Septiembre":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 9:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 9:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Octubre":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 10:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 10:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Noviembre":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 11:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 11:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

        if event.widget.get() == "Diciembre":
            dfr_der.destroy()
            dfr_der = Frame(display_fechas)
            dfr_der.grid(row=1, column=1)

            sum_dias = np.zeros(31)
            rest_dias = np.zeros(31)

            for item in ventas:
                if item[7] == 12:
                    for i in range(31):
                        if item[8] == (i+1):
                            sum_dias[i] = sum_dias[i] + (item[4]*item[5])

            for item in inventario:
                if item[7] == 12:
                    for i in range(31):
                        if item[8] == (i+1):
                            rest_dias[i] = rest_dias[i] + (item[4]*item[5])


            width=0.3
            x = np.arange(31)
            x2 = [ i + width for i in x ]
            x3 = [ i + 2*width for i in x ]
            neto = [ ]
            dias = [ ]
            for i in range(31):
                dias.append(str(i+1))
                neto.append(sum_dias[i]-rest_dias[i])

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(7, 4.3), dpi=100, facecolor="#B9DDE7")
            
            plt.bar( x, sum_dias, width, color="green", label="Ganancia")
            plt.bar( x2, rest_dias, width, color="red", label="Perdida")
            plt.bar( x3, neto, width, color="blue", label="Neto")
            plt.xlabel("Dias del mes")
            plt.xticks([r + width for r in range(31)], dias)
            plt.ylabel("Ganancia / Perdida / Neto")

            plt.grid(True)
            plt.legend()
            plt.title("Estadisticas: "+ event.widget.get())
            chart = FigureCanvasTkAgg(fig, dfr_der)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            datos_fr.destroy()
            datos_fr = Frame(display_fechas, bg="black")
            datos_fr.grid(row=1, column=0, sticky='ns')

            Label(datos_fr, text="Total Ganancia:  {0:.2f}" .format(sum(sum_dias)), bg="black", fg="green", font=('times', 14)).grid(row=0, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Perdida:   {0:.2f}" .format(sum(rest_dias)), bg="black", fg="red", font=('times', 14)).grid(row=1, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Total Neto:      {0:.2f}" .format(sum(neto)), bg="black", fg="blue", font=('times', 14)).grid(row=2, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Promedio neto:   {0:.2f}" .format(np.mean(neto)), bg="black", fg="white", font=('times', 14)).grid(row=3, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Varianza neto:   {0:.2f}" .format(np.var(neto)), bg="black", fg="white", font=('times', 14)).grid(row=6, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Desvio std neto: {0:.2f}" .format(np.std(neto)), bg="black", fg="white", font=('times', 14)).grid(row=7, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Maximo neto:     {0:.2f}" .format(np.max(neto)), bg="black", fg="white", font=('times', 14)).grid(row=8, column=0, ipadx=10, ipady=4)
            Label(datos_fr, text="Minimo neto:     {0:.2f}" .format(np.min(neto)), bg="black", fg="white", font=('times', 14)).grid(row=9, column=0, ipadx=10, ipady=4)

def df_get_datos(eleccion):
    if eleccion=="inventario":
        lista = get_lista()
        val = []
        try:
            if len(lista)>0:
                for item in lista:
                    if item[4] != "" and item[5] != "":
                        val.append(item[4]*item[5])


        except:
            pass
        finally:
            return val

    if eleccion=="ventas":
        lista = vget_lista()
        val = []
        try:
            if len(lista)>0:
                for item in lista:
                    if item[4] != "" and item[5] != "":
                        val.append(item[4]*item[5])

        except:
            pass
        finally:
            return val

def actualizar_trev(trev, eleccion):
    n = 0
    ventas = vget_lista()
    inventario = get_lista()
    if eleccion == "ventas":
        for item in ventas:
            trev.insert('', str(n), str(item[0]), text=str(item[0]))
            trev.set(str(item[0]), "precio", str(item[4]))
            trev.set(str(item[0]), "unidades", str(item[5]))
            trev.set(str(item[0]), "total", str(item[4]*item[5]))
            n += 1

    if eleccion == "perdida":
        for item in inventario:
            trev.insert('', str(n), str(item[0]), text=str(item[0]))
            trev.set(str(item[0]), "precio", str(item[4]))
            trev.set(str(item[0]), "unidades", str(item[5]))
            trev.set(str(item[0]), "total", str(item[4]*item[5]))
            n += 1

def f_notebook(event):
    if event.widget.select() == ".!frame.!notebook.!frame3":
        global fr_datos
        fr_datos.destroy()
        fr_datos = Frame(fr_std, bg="lightblue")

        flag_neto = False

        # implementar todos los widgets -------------------------------------------------

        # ganancia ************************************************

        fr_datos_ganancia = Frame(fr_datos, bg="lightblue")
        fr_datos_ganancia.grid(row=0, column=0, sticky="we")
        x = []
        y = df_get_datos("ventas")

        fr_datos_perdida = Frame(fr_datos, bg="lightblue")
        fr_datos_perdida.grid(row=1, column=0, sticky=E + W)
        xp = []
        yp = df_get_datos("inventario")

        if len(y) > 0 :
            for item in range(len(y)):
                x.append(item+1)

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            fig = plt.figure(figsize=(5, 2), dpi=100, facecolor="gray")
            fig.add_subplot(111).bar(x, y, 0.3, color="green", edgecolor="black")

            chart = FigureCanvasTkAgg(fig, master=fr_datos_ganancia)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            fr1 = Frame(fr_datos_ganancia, bg="black")
            fr1.grid(row=0, column=1, rowspan=2)
            g_scrollbar = Scrollbar(fr1, orient='vertical')

            trev = ttk.Treeview(fr1, columns=('precio', 'unidades', 'total'))
            trev.config(yscrollcommand=g_scrollbar.set, height=10, selectmode="browse")
            trev.heading('#0', text="ID")
            trev.heading('precio', text="PRECIO")
            trev.heading('unidades', text="UNIDADES")
            trev.heading('total', text="TOTAL")
            trev.column('#0', width=50, anchor='center')
            trev.column('precio', width=95, anchor='center')
            trev.column('unidades', width=78, anchor='center')
            trev.column('total', width=110, anchor='center')
            trev.pack(side=LEFT)

            # scrollbar vertical para la lista de productos
            g_scrollbar.config(command=trev.yview)
            g_scrollbar.pack(side=RIGHT, fill=Y)
            actualizar_trev(trev, "ventas")

            Label(fr_datos_ganancia, text="El total es {0:.2f} y el promedio {1:.2f}" \
                  .format((sum(y)), (np.mean(y))), bg="light green", font=('times', 14)).grid(row=1, column=0, sticky='we')

        # **********************************************************

        # perdida **************************************************

        if len(yp)>0:
            for item in range(len(yp)):
                xp.append(item+1)

            plt.style.use('ggplot')
            plt.rcParams.update({'figure.autolayout': True})

            figp = plt.figure(figsize=(5, 2), dpi=100, facecolor="gray")
            figp.add_subplot(111).bar(xp, yp, 0.3, color="red", edgecolor="black")

            chart = FigureCanvasTkAgg(figp, master=fr_datos_perdida)
            chart.draw()
            chart.get_tk_widget().grid(row=0, column=0)

            fr2 = Frame(fr_datos_perdida, bg="black")
            fr2.grid(row=0, column=1, rowspan=2)
            p_scrollbar = Scrollbar(fr2, orient='vertical')

            trep = ttk.Treeview(fr2, columns=('precio', 'unidades', 'total'))
            trep.config(yscrollcommand=p_scrollbar.set, height=10, selectmode="browse")
            trep.heading('#0', text="ID")
            trep.heading('precio', text="PRECIO")
            trep.heading('unidades', text="UNIDADES")
            trep.heading('total', text="TOTAL")
            trep.column('#0', width=50, anchor='center')
            trep.column('precio', width=95, anchor='center')
            trep.column('unidades', width=78, anchor='center')
            trep.column('total', width=110, anchor='center')
            trep.pack(side=LEFT)

            # scrollbar vertical para la lista de productos
            p_scrollbar.config(command=trep.yview)
            p_scrollbar.pack(side=RIGHT, fill=Y)
            actualizar_trev(trep, "perdida")

            Label(fr_datos_perdida, text="El total es {0:.2f} y el promedio es {1:.2f}" \
                .format((sum(yp)), (np.mean(yp))), bg="red", font=('times', 14)).grid(row=1, column=0, sticky='we')

            flag_neto=True
        # **********************************************************

        if flag_neto:
            Label(fr_datos, bg="lightblue", text="  ").grid(row=0, column=1, sticky="ns", rowspan=4, ipadx=12)


        # datos generales ******************************************
        if lbl_total['text'] != "" and vlbl_total['text'] != "" and flag_neto:
            Label(fr_datos, text="El neto es %.2f" %((float(vlbl_total['text']))-(float(lbl_total['text']))),\
                  justify=CENTER, font=('times', 18) , bg="lightblue").grid(row=3, column=0, sticky='we', ipady=8)


        # -------------------------------------------------------------------------------

        fr_datos.pack(fill="both", expand=1)

    if event.widget.select() == ".!frame.!notebook.!frame4":
        global display_fechas, dfr_izq, dfr_der, datos_fr
        display_fechas.destroy()
        display_fechas = Frame(fr_fechas)
        display_fechas.pack(fill="both", expand=1)
        

        # Implementar todos los widgets *************************************************

        dfr_izq = Frame(display_fechas, bg="gray")
        dfr_izq.grid(row=0, column=0)
        dfr_der = Frame(display_fechas, bg="yellow")
        dfr_der.grid(row=0, column=1)

        l_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        meses = ttk.Combobox(dfr_izq, justify=CENTER, values=l_meses, state='readonly')
        meses.set('Enero')
        meses.bind("<<ComboboxSelected>>", seleccion)
        meses.grid(row=0, column=0)

        datos_fr = Frame(dfr_izq)
        datos_fr.grid(row=1, column=0)

    if event.widget.select() == ".!frame.!notebook.!frame5":
        contacto_fr = Frame(contacto)
        contacto_fr.pack(side='top')

        # widgets
        
        Label(contacto_fr, text="¡Hola usuario promedio!", font=('times', 20, 'bold')).grid(row=0, column=0, pady=10)
        Label(contacto_fr, text="Bienvenido a esta aplicacion para comercios", font=('times', 16, 'bold')).grid(row=1, column=0, pady=10)
        Label(contacto_fr, text="Si tienes algun problema o duda contactame aqui:", font=('times', 16, 'bold')).grid(row=2, column=0, pady=10)
        Label(contacto_fr, text="Desarrollador: Miqueas Absalóm Aguirre (Est. de Ingeniería)", font=('times', 16)).grid(row=3, column=0, pady=10)
        Label(contacto_fr, text="Email: miqueasburzum@gmail.com", font=('times', 16)).grid(row=4, column=0, pady=10)
        Label(contacto_fr, text="Si quieres darme soporte para seguir desarrollando aplicaciones gratuitas", font=('times', 16)).grid(row=5, column=0, pady=10)
        Label(contacto_fr, text="O simplemente te gusto la aplicacion y quieres dar algo a cambio", font=('times', 16)).grid(row=6, column=0, pady=10)
        Label(contacto_fr, text="Pasate por mi patreon: 'MiqueasAguirreANX' ", font=('times', 16)).grid(row=7, column=0, pady=10)

        # *******************************************************************************

#-----------------------------------------------------------------------------
raiz = Tk()
raiz.title("ADMINISTRADOR")
raiz.resizable(height=False, width=False)

fr_principal = Frame(raiz)
fr_principal.config(bg="black")
fr_principal.pack()

notebook = ttk.Notebook(fr_principal)

# paginas -----------------------------------------------------------------
fr_inventario = Frame(notebook, bg="#96ACB8")
fr_inventario.pack(fill="both", expand=1)
fr_ventas = Frame(notebook, bg="#A0BEBB")
fr_ventas.pack(fill="both", expand=1)
fr_std = Frame(notebook, bg="#8177C0")
fr_std.pack(fill="both", expand=1)
fr_datos = Frame(fr_std, bg="#8177C0")
fr_datos.pack(fill="both", expand=1)
fr_fechas = Frame(notebook)
fr_fechas.pack(fill="both", expand=1)
display_fechas = Frame(fr_fechas)
display_fechas.pack(fill="both", expand=1)
contacto= Frame(notebook)
contacto.pack(fill='both', expand=1)

# widgets de las paginas --------------------------------------------------

# inventario

vcrear_tabla()
crear_tabla()

# frame principal
fr_ent = Frame(fr_inventario)
fr_ent.config(padx=10, pady=10, bg="#96ACB8", bd=8)
fr_ent.grid(row=0, column=0, sticky=N+S)
fr_secundario = Frame(fr_inventario)
fr_secundario.config(padx=10, pady=10, bg="#96ACB8", bd=8)
fr_secundario.grid(row=0, column=1, sticky=N+S)
fr_botones = Frame(fr_inventario)
fr_botones.config(padx=10, pady=10, bg="#96ACB8", bd=8)
fr_botones.grid(row=0, column=2, sticky=N+S)


# las etiquetas
Label(fr_ent, text="Categoria:", bg="#96ACB8", font=('arial', 11)).grid(row=0, column=0, pady=5, padx=5)
Label(fr_ent, text="Marca:", bg="#96ACB8", font=('arial', 11)).grid(row=1, column=0, pady=5, padx=5)
Label(fr_ent, text="Modelo:", bg="#96ACB8", font=('arial', 11)).grid(row=2, column=0, pady=5, padx=5)
Label(fr_ent, text="Precio:", bg="#96ACB8", font=('arial', 11)).grid(row=3, column=0, pady=5, padx=5)
Label(fr_ent, text="Unidades:", bg="#96ACB8", font=('arial', 11)).grid(row=4, column=0, pady=5, padx=5)

# las entradas
cat = Entry(fr_ent)
cat.grid(row=0, column=1)
cat.focus()
mar = Entry(fr_ent)
mar.grid(row=1, column=1)
model = Entry(fr_ent)
model.grid(row=2, column=1)
pre = Entry(fr_ent)
pre.grid(row=3, column=1)
uni = Spinbox(fr_ent, from_=1, to=100, increment=1)
uni.grid(row=4, column=1)

# botones para guardar o cancelar productos individuales
botones = Frame(fr_ent, bg="#96ACB8")
botones.grid(row=6, column=0, columnspan=2)
btn_guardar = Button(botones, text="Guardar", bg="#96FF7C", bd=5, command= f_guardar )
btn_guardar.config(font=("arial", 12))
btn_guardar.grid(row=0, column=0, padx=5, pady=5, ipadx=30, columnspan=2)

ttk.Separator(botones, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=E+W, pady=15)
Label(botones, text="    ID:        ", bg="#96ACB8", font=('arial', 11)).grid(row=2, column=0, pady=5, padx=5)
id_borrar = Entry(botones)
id_borrar.grid(row=2, column=1)

btn_borrar = Button(botones, text="Borrar", bg="#FF887C", bd=5, command=lambda : f_borrar(id_borrar.get()))
btn_borrar.config(font=("arial", 12))
btn_borrar.grid(row=3, column=0, padx=5, pady=5, ipadx=30)
btn_reiniciar = Button(botones, text="Reiniciar", bg="#FF007C", bd=5, command=reinicio)
btn_reiniciar.config(font=("arial", 12))
btn_reiniciar.grid(row=3, column=1, padx=5, pady=5, ipadx=30)

ttk.Separator(botones, orient=HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=E+W, pady=15)



resetear()
Label(botones, text="Total gastado:   ", bg="#96ACB8",font=('times', 14)).grid(row=5, column=0)
lbl_total = Label(botones, text="", bg="#96ACB8",font=('times', 14))
lbl_total.grid(row=5, column=1)
Label(botones, text="Nro de registros:", bg="#96ACB8",font=('times', 14)).grid(row=6, column=0)
lbl_cant = Label(botones, text="", bg="#96ACB8",font=('times', 14))
lbl_cant.grid(row=6, column=1)


# Lista de productos
scrollbar = Scrollbar(fr_secundario, orient='vertical')

treeview = ttk.Treeview(fr_secundario, columns=( 'categoria', 'marca', 'modelo' , 'precio', 'unidades'))
treeview.config(yscrollcommand=scrollbar.set, height=22, selectmode="browse")
treeview.heading('#0', text="ID")
treeview.heading('categoria', text="CATEGORIA")
treeview.heading('marca', text="MARCA")
treeview.heading('modelo', text="MODELO")
treeview.heading('precio', text="PRECIO")
treeview.heading('unidades', text="UNIDADES")
treeview.column('#0', width=50, anchor='center')
treeview.column('categoria', width=100, anchor='center')
treeview.column('modelo', width=100, anchor='center')
treeview.column('marca', width=100, anchor='center')
treeview.column('precio', width=80, anchor='center')
treeview.column('unidades', width=80, anchor='center')
treeview.pack(side=LEFT)
# scrollbar vertical para la lista de productos
scrollbar.config(command=treeview.yview)
scrollbar.pack(side=RIGHT, fill=Y)
actualizar()
resetear()

# ventas

global carrito
carrito = []

# frame principal
vfr_ent = Frame(fr_ventas)
vfr_ent.config(padx=10, pady=10, bg="#A0BEBB", bd=8)
vfr_ent.grid(row=0, column=0, sticky=N+S)
vfr_secundario = Frame(fr_ventas)
vfr_secundario.config(padx=10, pady=10, bg="#A0BEBB", bd=8)
vfr_secundario.grid(row=0, column=1, sticky=N+S)
vfr_botones = Frame(fr_ventas)
vfr_botones.config(padx=10, pady=10, bg="#A0BEBB", bd=8)
vfr_botones.grid(row=0, column=2, sticky=N+S)


# las etiquetas
Label(vfr_ent, text="ID:      ", bg="#A0BEBB", font=('times', 12)).grid(row=0, column=0, pady=5, padx=5)
Label(vfr_ent, text="Precio:  ", bg="#A0BEBB", font=('times', 12)).grid(row=1, column=0, pady=5, padx=5)
Label(vfr_ent, text="Unidades:", bg="#A0BEBB", font=('times', 12)).grid(row=2, column=0, pady=5, padx=5)

# las entradas
vid = Entry(vfr_ent)
vid.grid(row=0, column=1)
vpre = Entry(vfr_ent)
vpre.grid(row=1, column=1)
vuni = Spinbox(vfr_ent, from_=1, to=100, increment=1)
vuni.grid(row=2, column=1)

# botones para guardar o cancelar productos individuales
vbotones = Frame(vfr_ent, bg="#A0BEBB")
vbotones.grid(row=3, column=0, columnspan=2)
vbtn_guardar = Button(vbotones, text="Agregar", bg="#96FF7C", bd=5, command= agregar_carrito )
vbtn_guardar.config(font=("arial", 12))
vbtn_guardar.grid(row=0, column=0, padx=5, pady=5, ipadx=15)
vbtn_cancelar = Button(vbotones, text="Cancelar", bg="#FFFA51", bd=5, command= vf_cancelar )
vbtn_cancelar.config(font=("arial", 12))
vbtn_cancelar.grid(row=0, column=1, padx=5, pady=5, ipadx=15)

ttk.Separator(vbotones, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=E+W, pady=15)
Label(vbotones, text="    ID:        ", bg="#A0BEBB", font=('arial', 11)).grid(row=2, column=0, pady=5, padx=5)
vid_borrar = Entry(vbotones)
vid_borrar.grid(row=2, column=1)

vbtn_borrar = Button(vbotones, text="Borrar", bg="#FF887C", bd=5, command=lambda : vf_borrar(vid_borrar.get()))
vbtn_borrar.config(font=("arial", 12))
vbtn_borrar.grid(row=3, column=0, padx=5, pady=5, ipadx=25)
vbtn_reiniciar = Button(vbotones, text="Reiniciar", bg="#FF887C", bd=5, command=vreinicio)
vbtn_reiniciar.config(font=("arial", 12))
vbtn_reiniciar.grid(row=3, column=1, padx=5, pady=5, ipadx=20)
vbtn_vender = Button(vbotones, text="Vender", bg="#DDDDFF", bd=5, command=vvender)
vbtn_vender.config(font=("arial", 12))
vbtn_vender.grid(row=4, column=0, padx=5, pady=10, ipadx=45, columnspan=2)

ttk.Separator(vbotones, orient=HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=E+W, pady=15)

resetear()
Label(vbotones, text="Total venta:     ", bg="#A0BEBB", font=('times', 14)).grid(row=6, column=0)
vlbl_venta = Label(vbotones, text="", bg="#A0BEBB", font=('times', 14))
vlbl_venta.grid(row=6, column=1)
Label(vbotones, text="Total ganado:    ", bg="#A0BEBB", font=('times', 14)).grid(row=7, column=0)
vlbl_total = Label(vbotones, text="", bg="#A0BEBB", font=('times', 14))
vlbl_total.grid(row=7, column=1)
Label(vbotones, text="Nro de registros:", bg="#A0BEBB", font=('times', 14)).grid(row=8, column=0)
vlbl_cant = Label(vbotones, text="", bg="#A0BEBB", font=('times', 14))
vlbl_cant.grid(row=8, column=1)

# Lista de productos
vscrollbar = Scrollbar(vfr_secundario, orient='vertical')

treeview_v = ttk.Treeview(vfr_secundario, columns=( 'categoria', 'marca', 'modelo' , 'precio', 'unidades'))
treeview_v.config(yscrollcommand=vscrollbar.set, height=10, selectmode="browse")
treeview_v.heading('#0', text="ID")
treeview_v.heading('categoria', text="CATEGORIA")
treeview_v.heading('marca', text="MARCA")
treeview_v.heading('modelo', text="MODELO")
treeview_v.heading('precio', text="PRECIO")
treeview_v.heading('unidades', text="UNIDADES")
treeview_v.column('#0', width=60, anchor='center')
treeview_v.column('categoria', width=100, anchor='center')
treeview_v.column('modelo', width=100, anchor='center')
treeview_v.column('marca', width=100, anchor='center')
treeview_v.column('precio', width=90, anchor='center')
treeview_v.column('unidades', width=80, anchor='center')
treeview_v.grid(row=1, column=0)
# scrollbar vertical para la lista de productos

vscrollbar.config(command=treeview_v.yview)
vscrollbar.grid(row=1, column=1, sticky='ns')

vscroll_carrito = Scrollbar(vfr_secundario, orient='vertical')

treeview_c = ttk.Treeview(vfr_secundario, columns=( 'categoria', 'marca', 'modelo' , 'precio', 'unidades'))
treeview_c.config(yscrollcommand=vscroll_carrito.set, height=10, selectmode="browse")
treeview_c.heading('#0', text="ID")
treeview_c.heading('categoria', text="CATEGORIA")
treeview_c.heading('marca', text="MARCA")
treeview_c.heading('modelo', text="MODELO")
treeview_c.heading('precio', text="PRECIO")
treeview_c.heading('unidades', text="UNIDADES")
treeview_c.column('#0', width=60, anchor='center')
treeview_c.column('categoria', width=100, anchor='center')
treeview_c.column('modelo', width=100, anchor='center')
treeview_c.column('marca', width=100, anchor='center')
treeview_c.column('precio', width=90, anchor='center')
treeview_c.column('unidades', width=80, anchor='center')
treeview_c.grid(row=0, column=0, pady=10)
# scrollbar vertical para la lista de productos

vscroll_carrito.config(command=treeview_c.yview)
vscroll_carrito.grid(row=0, column=1, sticky='ns', pady=10)

vresetear()
vactualizar()

# ------------------------------------------------------------------------

# agregar los tabs
notebook.add(child=fr_inventario, text="Inventario")
notebook.add(child=fr_ventas, text="Ventas")
notebook.add(child=fr_std, text="Datos generales")
notebook.add(child=fr_fechas , text="Estadistica")
notebook.add(child=contacto, text="Contacto")
notebook.bind("<<NotebookTabChanged>>", f_notebook)
notebook.pack()

raiz.mainloop()