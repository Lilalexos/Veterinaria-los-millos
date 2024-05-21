import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('el_refugio_animal.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS mascotas (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    especie TEXT,
                    raza TEXT,
                    edad INTEGER,
                    historial TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS citas (
                    id INTEGER PRIMARY KEY,
                    mascota_id INTEGER,
                    tipo TEXT,
                    fecha TEXT,
                    FOREIGN KEY(mascota_id) REFERENCES mascotas(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    cantidad INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS facturacion (
                    id INTEGER PRIMARY KEY,
                    mascota_id INTEGER,
                    servicio TEXT,
                    costo REAL,
                    fecha TEXT,
                    FOREIGN KEY(mascota_id) REFERENCES mascotas(id))''')

conn.commit()

# GUI setup
class VetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clínica Veterinaria El Refugio Animal")
        self.create_widgets()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self.root)

        self.tab_mascotas = ttk.Frame(self.tabControl)
        self.tab_citas = ttk.Frame(self.tabControl)
        self.tab_inventario = ttk.Frame(self.tabControl)
        self.tab_facturacion = ttk.Frame(self.tabControl)
        self.tab_informes = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_mascotas, text='Mascotas')
        self.tabControl.add(self.tab_citas, text='Citas')
        self.tabControl.add(self.tab_inventario, text='Inventario')
        self.tabControl.add(self.tab_facturacion, text='Facturación')
        self.tabControl.add(self.tab_informes, text='Informes')
        
        self.tabControl.pack(expand=1, fill="both")

        self.create_mascotas_tab()
        self.create_citas_tab()
        self.create_inventario_tab()
        self.create_facturacion_tab()
        self.create_informes_tab()

    def create_mascotas_tab(self):
        self.lbl_nombre = tk.Label(self.tab_mascotas, text="Nombre:")
        self.lbl_nombre.grid(column=0, row=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self.tab_mascotas)
        self.entry_nombre.grid(column=1, row=0, padx=10, pady=10)

        self.lbl_especie = tk.Label(self.tab_mascotas, text="Especie:")
        self.lbl_especie.grid(column=0, row=1, padx=10, pady=10)
        self.entry_especie = tk.Entry(self.tab_mascotas)
        self.entry_especie.grid(column=1, row=1, padx=10, pady=10)

        self.lbl_raza = tk.Label(self.tab_mascotas, text="Raza:")
        self.lbl_raza.grid(column=0, row=2, padx=10, pady=10)
        self.entry_raza = tk.Entry(self.tab_mascotas)
        self.entry_raza.grid(column=1, row=2, padx=10, pady=10)

        self.lbl_edad = tk.Label(self.tab_mascotas, text="Edad:")
        self.lbl_edad.grid(column=0, row=3, padx=10, pady=10)
        self.entry_edad = tk.Entry(self.tab_mascotas)
        self.entry_edad.grid(column=1, row=3, padx=10, pady=10)

        self.lbl_historial = tk.Label(self.tab_mascotas, text="Historial:")
        self.lbl_historial.grid(column=0, row=4, padx=10, pady=10)
        self.entry_historial = tk.Entry(self.tab_mascotas)
        self.entry_historial.grid(column=1, row=4, padx=10, pady=10)

        self.btn_add_mascota = tk.Button(self.tab_mascotas, text="Agregar Mascota", command=self.add_mascota)
        self.btn_add_mascota.grid(column=0, row=5, padx=10, pady=10, columnspan=2)

        self.tree_mascotas = ttk.Treeview(self.tab_mascotas, columns=("id", "nombre", "especie", "raza", "edad", "historial"), show='headings')
        self.tree_mascotas.heading("id", text="ID")
        self.tree_mascotas.heading("nombre", text="Nombre")
        self.tree_mascotas.heading("especie", text="Especie")
        self.tree_mascotas.heading("raza", text="Raza")
        self.tree_mascotas.heading("edad", text="Edad")
        self.tree_mascotas.heading("historial", text="Historial")
        self.tree_mascotas.grid(column=0, row=6, padx=10, pady=10, columnspan=2)

        self.load_mascotas()

    def create_citas_tab(self):
        self.lbl_mascota_id = tk.Label(self.tab_citas, text="ID Mascota:")
        self.lbl_mascota_id.grid(column=0, row=0, padx=10, pady=10)
        self.entry_mascota_id = tk.Entry(self.tab_citas)
        self.entry_mascota_id.grid(column=1, row=0, padx=10, pady=10)

        self.lbl_tipo_cita = tk.Label(self.tab_citas, text="Tipo de Cita:")
        self.lbl_tipo_cita.grid(column=0, row=1, padx=10, pady=10)
        self.entry_tipo_cita = tk.Entry(self.tab_citas)
        self.entry_tipo_cita.grid(column=1, row=1, padx=10, pady=10)

        self.lbl_fecha_cita = tk.Label(self.tab_citas, text="Fecha de Cita:")
        self.lbl_fecha_cita.grid(column=0, row=2, padx=10, pady=10)
        self.entry_fecha_cita = tk.Entry(self.tab_citas)
        self.entry_fecha_cita.grid(column=1, row=2, padx=10, pady=10)

        self.btn_add_cita = tk.Button(self.tab_citas, text="Agregar Cita", command=self.add_cita)
        self.btn_add_cita.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        self.tree_citas = ttk.Treeview(self.tab_citas, columns=("id", "mascota_id", "tipo", "fecha"), show='headings')
        self.tree_citas.heading("id", text="ID")
        self.tree_citas.heading("mascota_id", text="ID Mascota")
        self.tree_citas.heading("tipo", text="Tipo")
        self.tree_citas.heading("fecha", text="Fecha")
        self.tree_citas.grid(column=0, row=4, padx=10, pady=10, columnspan=2)

        self.load_citas()

    def create_inventario_tab(self):
        self.lbl_nombre_producto = tk.Label(self.tab_inventario, text="Nombre del Producto:")
        self.lbl_nombre_producto.grid(column=0, row=0, padx=10, pady=10)
        self.entry_nombre_producto = tk.Entry(self.tab_inventario)
        self.entry_nombre_producto.grid(column=1, row=0, padx=10, pady=10)

        self.lbl_cantidad_producto = tk.Label(self.tab_inventario, text="Cantidad:")
        self.lbl_cantidad_producto.grid(column=0, row=1, padx=10, pady=10)
        self.entry_cantidad_producto = tk.Entry(self.tab_inventario)
        self.entry_cantidad_producto.grid(column=1, row=1, padx=10, pady=10)

        self.btn_add_producto = tk.Button(self.tab_inventario, text="Agregar Producto", command=self.add_producto)
        self.btn_add_producto.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

        self.tree_inventario = ttk.Treeview(self.tab_inventario, columns=("id", "nombre", "cantidad"), show='headings')
        self.tree_inventario.heading("id", text="ID")
        self.tree_inventario.heading("nombre", text="Nombre")
        self.tree_inventario.heading("cantidad", text="Cantidad")
        self.tree_inventario.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        self.load_inventario()

    def create_facturacion_tab(self):
        self.lbl_mascota_id_factura = tk.Label(self.tab_facturacion, text="ID Mascota:")
        self.lbl_mascota_id_factura.grid(column=0, row=0, padx=10, pady=10)
        self.entry_mascota_id_factura = tk.Entry(self.tab_facturacion)
        self.entry_mascota_id_factura.grid(column=1, row=0, padx=10, pady=10)

        self.lbl_servicio_factura = tk.Label(self.tab_facturacion, text="Servicio:")
        self.lbl_servicio_factura.grid(column=0, row=1, padx=10, pady=10)
        self.entry_servicio_factura = tk.Entry(self.tab_facturacion)
        self.entry_servicio_factura.grid(column=1, row=1, padx=10, pady=10)

        self.lbl_costo_factura = tk.Label(self.tab_facturacion, text="Costo:")
        self.lbl_costo_factura.grid(column=0, row=2, padx=10, pady=10)
        self.entry_costo_factura = tk.Entry(self.tab_facturacion)
        self.entry_costo_factura.grid(column=1, row=2, padx=10, pady=10)

        self.btn_add_factura = tk.Button(self.tab_facturacion, text="Agregar Factura", command=self.add_factura)
        self.btn_add_factura.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        self.tree_facturacion = ttk.Treeview(self.tab_facturacion, columns=("id", "mascota_id", "servicio", "costo", "fecha"), show='headings')
        self.tree_facturacion.heading("id", text="ID")
        self.tree_facturacion.heading("mascota_id", text="ID Mascota")
        self.tree_facturacion.heading("servicio", text="Servicio")
        self.tree_facturacion.heading("costo", text="Costo")
        self.tree_facturacion.heading("fecha", text="Fecha")
        self.tree_facturacion.grid(column=0, row=4, padx=10, pady=10, columnspan=2)

        self.load_facturacion()

    def create_informes_tab(self):
        self.lbl_informes = tk.Label(self.tab_informes, text="Generar Informes:")
        self.lbl_informes.grid(column=0, row=0, padx=10, pady=10)

        self.btn_generate_informes = tk.Button(self.tab_informes, text="Generar", command=self.generate_informes)
        self.btn_generate_informes.grid(column=1, row=0, padx=10, pady=10)

        self.txt_informes = tk.Text(self.tab_informes)
        self.txt_informes.grid(column=0, row=1, padx=10, pady=10, columnspan=2)

    def add_mascota(self):
        nombre = self.entry_nombre.get()
        especie = self.entry_especie.get()
        raza = self.entry_raza.get()
        edad = self.entry_edad.get()
        historial = self.entry_historial.get()

        cursor.execute("INSERT INTO mascotas (nombre, especie, raza, edad, historial) VALUES (?, ?, ?, ?, ?)",
                       (nombre, especie, raza, edad, historial))
        conn.commit()
        self.load_mascotas()

    def load_mascotas(self):
        for row in self.tree_mascotas.get_children():
            self.tree_mascotas.delete(row)
        cursor.execute("SELECT * FROM mascotas")
        for row in cursor.fetchall():
            self.tree_mascotas.insert("", tk.END, values=row)

    def add_cita(self):
        mascota_id = self.entry_mascota_id.get()
        tipo = self.entry_tipo_cita.get()
        fecha = self.entry_fecha_cita.get()

        cursor.execute("INSERT INTO citas (mascota_id, tipo, fecha) VALUES (?, ?, ?)",
                       (mascota_id, tipo, fecha))
        conn.commit()
        self.load_citas()

    def load_citas(self):
        for row in self.tree_citas.get_children():
            self.tree_citas.delete(row)
        cursor.execute("SELECT * FROM citas")
        for row in cursor.fetchall():
            self.tree_citas.insert("", tk.END, values=row)

    def add_producto(self):
        nombre = self.entry_nombre_producto.get()
        cantidad = self.entry_cantidad_producto.get()

        cursor.execute("INSERT INTO inventario (nombre, cantidad) VALUES (?, ?)", (nombre, cantidad))
        conn.commit()
        self.load_inventario()

    def load_inventario(self):
        for row in self.tree_inventario.get_children():
            self.tree_inventario.delete(row)
        cursor.execute("SELECT * FROM inventario")
        for row in cursor.fetchall():
            self.tree_inventario.insert("", tk.END, values=row)

    def add_factura(self):
        mascota_id = self.entry_mascota_id_factura.get()
        servicio = self.entry_servicio_factura.get()
        costo = self.entry_costo_factura.get()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO facturacion (mascota_id, servicio, costo, fecha) VALUES (?, ?, ?, ?)",
                       (mascota_id, servicio, costo, fecha))
        conn.commit()
        self.load_facturacion()

    def load_facturacion(self):
        for row in self.tree_facturacion.get_children():
            self.tree_facturacion.delete(row)
        cursor.execute("SELECT * FROM facturacion")
        for row in cursor.fetchall():
            self.tree_facturacion.insert("", tk.END, values=row)

    def generate_informes(self):
        cursor.execute("SELECT COUNT(*) FROM mascotas")
        total_mascotas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM citas")
        total_citas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM inventario")
        total_productos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM facturacion")
        total_facturas = cursor.fetchone()[0]

        informe = f"Total de Mascotas: {total_mascotas}\nTotal de Citas: {total_citas}\nTotal de Productos: {total_productos}\nTotal de Facturas: {total_facturas}\n"
        self.txt_informes.delete(1.0, tk.END)
        self.txt_informes.insert(tk.END, informe)

if __name__ == "__main__":
    root = tk.Tk()
    app = VetApp(root)
    root.mainloop()
    conn.close()
