import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import ttk, messagebox
from pymongo import MongoClient, errors

class RegistroJugador(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Registro de Jugador")
        self.parent = parent
        self.db = db
        self.collection = self.db['jugadores']

        label_nombre = ttk.Label(self, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        label_edad = ttk.Label(self, text="Edad:")
        label_edad.grid(row=1, column=0, padx=5, pady=5)
        self.entry_edad = ttk.Entry(self)
        self.entry_edad.grid(row=1, column=1, padx=5, pady=5)

        label_pais = ttk.Label(self, text="País:")
        label_pais.grid(row=2, column=0, padx=5, pady=5)
        self.entry_pais = ttk.Entry(self)
        self.entry_pais.grid(row=2, column=1, padx=5, pady=5)

        self.button_registrar = ttk.Button(self, text="Registrar Jugador", command=self.registrar_jugador)
        self.button_registrar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def registrar_jugador(self):
        try:
            nombre = self.entry_nombre.get().strip()
            edad = int(self.entry_edad.get())
            pais = self.entry_pais.get().strip()

            if not nombre or not pais:
                messagebox.showerror("Error", "El nombre y el país no pueden estar vacíos.")
                return

            if edad <= 0:
                messagebox.showerror("Error", "La edad debe ser un número positivo.")
                return

            if self.collection.find_one({"Nombre": nombre}):
                messagebox.showerror("Error", "Ya existe un jugador con ese nombre.")
                return

            max_id_jugador = self.collection.find_one(sort=[("ID", -1)])
            max_id = max_id_jugador["ID"] if max_id_jugador else 0
            siguiente_id = max_id + 1

            while self.collection.find_one({"ID": siguiente_id}):
                siguiente_id += 1

            self.collection.insert_one({"ID": siguiente_id, "Nombre": nombre, "Edad": edad, "Pais": pais})
            messagebox.showinfo("Éxito", "Jugador registrado correctamente.")
            self.back_to_parent()  # Añadir esta línea para volver a la ventana principal

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese datos válidos.")
        except errors.PyMongoError as e:
            messagebox.showerror("Error", f"Error al registrar el jugador: {e}")


    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.destroy()

class IniciarCuenta(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Iniciar Cuenta")
        self.parent = parent
        self.db = db
        self.jugador_id = None

        self.collection = self.db['jugadores']

        label_nombre = ttk.Label(self, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        button_iniciar = ttk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        button_iniciar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def iniciar_sesion(self):
        try:
            nombre = self.entry_nombre.get().strip()

            jugador = self.collection.find_one({"Nombre": nombre})

            if jugador:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                self.open_menu(jugador['ID'])
            else:
                messagebox.showerror("Error", "Nombre incorrecto.")
        except errors.PyMongoError as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")

    def open_menu(self, jugador_id):
        self.withdraw()
        MenuDatos(self, self.db, jugador_id)

    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.destroy()

class MenuDatos(tk.Toplevel):
    def __init__(self, parent, db, jugador_id):
        super().__init__(parent)
        self.title("Menú de Datos")
        self.parent = parent
        self.db = db
        self.jugador_id = jugador_id

        self.button_agregar_datos = ttk.Button(self, text="Agregar Datos", command=self.abrir_agregar_datos)
        self.button_agregar_datos.grid(row=0, column=0, padx=10, pady=10)

        self.button_mostrar_datos = ttk.Button(self, text="Mostrar Datos", command=self.mostrar_datos)
        self.button_mostrar_datos.grid(row=1, column=0, padx=10, pady=10)

        self.button_eliminar_videojuego = ttk.Button(self, text="Eliminar Videojuego", command=self.eliminar_videojuego)
        self.button_eliminar_videojuego.grid(row=2, column=0, padx=10, pady=10)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=3, column=0, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def abrir_agregar_datos(self):
        AgregarDatos(self, self.db, self.jugador_id)

    def mostrar_datos(self):
        jugadores = self.db['jugadores'].find()

        if jugadores:
            datos = ""
            for jugador in jugadores:
                datos += f"Nombre: {jugador['Nombre']}, Edad: {jugador['Edad']}, País: {jugador['Pais']}\n"

                videojuegos = self.db['videojuegos'].find({"Jugador_ID": jugador['ID']})
                for vj in videojuegos:
                    datos += f"  Videojuego:\n"
                    datos += f"    - Título: {vj['Titulo']}\n"
                    datos += f"    - Año de Lanzamiento: {vj['Año_Lanzamiento']}\n"
                    datos += f"    - Colecciones:\n"

                    colecciones = self.db['colecciones'].find({"Videojuego_ID": vj['_id']})
                    for col in colecciones:
                        datos += f"      - Fecha de Adquisición: {col['Fecha_Adquisicion']}, Estado: {col['Estado']}\n"

            if datos:
                messagebox.showinfo("Datos de Jugadores", datos)
            else:
                messagebox.showinfo("Datos de Jugadores", "No hay datos disponibles.")
        else:
            messagebox.showerror("Error", "No se encontraron jugadores en la base de datos.")

    # Los otros métodos de la clase permanecen sin cambios


    def eliminar_videojuego(self):
        titulo_videojuego = self.ask_for_videojuego()
        if titulo_videojuego:
            videojuego = self.db['videojuegos'].find_one({"Titulo": titulo_videojuego, "Jugador_ID": self.jugador_id})
            if videojuego:
                videojuego_id = videojuego['_id']
                self.eliminar_datos_videojuego(videojuego_id)
                self.db['videojuegos'].delete_one({"_id": videojuego_id})
                messagebox.showinfo("Éxito", f"Videojuego '{titulo_videojuego}' y sus datos de colección asociados eliminados correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró un videojuego con ese título para este jugador.")

    def ask_for_videojuego(self):
        return simpledialog.askstring("Eliminar Videojuego", "Ingrese el título del videojuego que desea eliminar:")

    def eliminar_datos_videojuego(self, videojuego_id):
        self.db['colecciones'].delete_many({"Videojuego_ID": videojuego_id})

    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.parent.deiconify()
        self.destroy()

class AgregarDatos(tk.Toplevel):
    def __init__(self, parent, db, jugador_id):
        super().__init__(parent)
        self.title("Agregar Datos")
        self.db = db
        self.jugador_id = jugador_id

        self.label_titulo = ttk.Label(self, text="Título del Videojuego:")
        self.label_titulo.grid(row=0, column=0, padx=10, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=5)

        self.label_anio = ttk.Label(self, text="Año de Lanzamiento:")
        self.label_anio.grid(row=1, column=0, padx=10, pady=5)
        self.entry_anio = ttk.Entry(self)
        self.entry_anio.grid(row=1, column=1, padx=10, pady=5)

        self.label_genero = ttk.Label(self, text="Género:")
        self.label_genero.grid(row=2, column=0, padx=10, pady=5)
        self.entry_genero = ttk.Entry(self)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=5)

        self.label_desarrollador = ttk.Label(self, text="Desarrollador:")
        self.label_desarrollador.grid(row=3, column=0, padx=10, pady=5)
        self.entry_desarrollador = ttk.Entry(self)
        self.entry_desarrollador.grid(row=3, column=1, padx=10, pady=5)

        self.label_plataforma = ttk.Label(self, text="Plataforma:")
        self.label_plataforma.grid(row=4, column=0, padx=10, pady=5)
        self.entry_plataforma = ttk.Entry(self)
        self.entry_plataforma.grid(row=4, column=1, padx=10, pady=5)

        self.label_fecha_adquisicion = ttk.Label(self, text="Fecha de Adquisición:")
        self.label_fecha_adquisicion.grid(row=5, column=0, padx=10, pady=5)
        self.entry_fecha_adquisicion = ttk.Entry(self)
        self.entry_fecha_adquisicion.grid(row=5, column=1, padx=10, pady=5)

        self.label_estado = ttk.Label(self, text="Estado:")
        self.label_estado.grid(row=6, column=0, padx=10, pady=5)
        self.entry_estado = ttk.Entry(self)
        self.entry_estado.grid(row=6, column=1, padx=10, pady=5)

        self.button_guardar = ttk.Button(self, text="Guardar", command=self.guardar_datos)
        self.button_guardar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def guardar_datos(self):
        titulo = self.entry_titulo.get()
        anio_lanzamiento = self.entry_anio.get()
        genero = self.entry_genero.get()
        desarrollador = self.entry_desarrollador.get()
        plataforma = self.entry_plataforma.get()
        fecha_adquisicion = self.entry_fecha_adquisicion.get()
        estado = self.entry_estado.get()

        if titulo and anio_lanzamiento and genero and desarrollador and plataforma and fecha_adquisicion and estado:
            videojuego_id = self.db['videojuegos'].insert_one({
                "Jugador_ID": self.jugador_id,
                "Titulo": titulo,
                "Año_Lanzamiento": anio_lanzamiento,
                "Genero": genero,
                "Desarrollador": desarrollador,
                "Plataforma": plataforma
            }).inserted_id

            self.db['colecciones'].insert_one({
                "Videojuego_ID": videojuego_id,
                "Fecha_Adquisicion": fecha_adquisicion,
                "Estado": estado
            })

            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
            self.close_window()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def close_window(self):
        self.destroy()

class MostrarDatos(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Mostrar Datos")
        self.db = db

        text_area = tk.Text(self)
        text_area.pack(expand=True, fill='both')

        jugadores = self.db['jugadores'].find()

        if jugadores:
            for jugador in jugadores:
                text_area.insert(tk.END, f"Nombre: {jugador['Nombre']}, Edad: {jugador['Edad']}, País: {jugador['Pais']}\n")
                videojuegos = self.db['videojuegos'].find({"Jugador_ID": jugador['ID']})
                for vj in videojuegos:
                    text_area.insert(tk.END, f"  Videojuego:\n")
                    text_area.insert(tk.END, f"    - Título: {vj['Titulo']}\n")
                    text_area.insert(tk.END, f"    - Año de Lanzamiento: {vj['Año_Lanzamiento']}\n")
                    text_area.insert(tk.END, f"    - Género: {vj['Genero']}\n")
                    text_area.insert(tk.END, f"    - Desarrollador: {vj['Desarrollador']}\n")
                    text_area.insert(tk.END, f"    - Plataforma: {vj['Plataforma']}\n")
                    text_area.insert(tk.END, f"    - Colecciones:\n")

                    colecciones = self.db['colecciones'].find({"Videojuego_ID": vj['_id']})
                    for col in colecciones:
                        text_area.insert(tk.END, f"      - Fecha de Adquisición: {col['Fecha_Adquisicion']}, Estado: {col['Estado']}\n")

        self.button_volver = ttk.Button(self, text="Volver", command=self.close_window)
        self.button_volver.pack(pady=10)

    def close_window(self):
        self.destroy()

class MenuDatos(tk.Toplevel):
    def __init__(self, parent, db, jugador_id):
        super().__init__(parent)
        self.title("Menú de Datos")
        self.parent = parent
        self.db = db
        self.jugador_id = jugador_id

        self.button_agregar_datos = ttk.Button(self, text="Agregar Datos", command=self.abrir_agregar_datos)
        self.button_agregar_datos.grid(row=0, column=0, padx=10, pady=10)

        self.button_mostrar_datos = ttk.Button(self, text="Mostrar Datos", command=self.mostrar_datos)
        self.button_mostrar_datos.grid(row=1, column=0, padx=10, pady=10)

        self.button_eliminar_videojuego = ttk.Button(self, text="Eliminar Videojuego", command=self.eliminar_videojuego)
        self.button_eliminar_videojuego.grid(row=2, column=0, padx=10, pady=10)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=3, column=0, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def abrir_agregar_datos(self):
        AgregarDatos(self, self.db, self.jugador_id)

    def mostrar_datos(self):
        videojuegos = self.db['videojuegos'].find({"Jugador_ID": self.jugador_id})

        if videojuegos:
            datos = ""
            for vj in videojuegos:
                datos += f"Videojuego:\n"
                datos += f"  - Título: {vj['Titulo']}\n"
                datos += f"  - Año de Lanzamiento: {vj['Año_Lanzamiento']}\n"
                datos += f"  - Género: {vj['Genero']}\n"
                datos += f"  - Desarrollador: {vj['Desarrollador']}\n"
                datos += f"  - Plataforma: {vj['Plataforma']}\n"
                datos += f"  - Colecciones:\n"

                colecciones = self.db['colecciones'].find({"Videojuego_ID": vj['_id']})
                for col in colecciones:
                    datos += f"    - Fecha de Adquisición: {col['Fecha_Adquisicion']}, Estado: {col['Estado']}\n"

            if datos:
                messagebox.showinfo("Datos de Videojuegos", datos)
            else:
                messagebox.showinfo("Datos de Videojuegos", "No hay datos disponibles.")
        else:
            messagebox.showerror("Error", "No se encontraron videojuegos en la base de datos.")

    def eliminar_videojuego(self):
        titulo_videojuego = self.ask_for_videojuego()
        if titulo_videojuego:
            videojuego = self.db['videojuegos'].find_one({"Titulo": titulo_videojuego, "Jugador_ID": self.jugador_id})
            if videojuego:
                videojuego_id = videojuego['_id']
                self.eliminar_datos_videojuego(videojuego_id)
                self.db['videojuegos'].delete_one({"_id": videojuego_id})
                messagebox.showinfo("Éxito", f"Videojuego '{titulo_videojuego}' y sus datos de colección asociados eliminados correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró un videojuego con ese título para este jugador.")

    def ask_for_videojuego(self):
        return simpledialog.askstring("Eliminar Videojuego", "Ingrese el título del videojuego que desea eliminar:")

    def eliminar_datos_videojuego(self, videojuego_id):
        self.db['colecciones'].delete_many({"Videojuego_ID": videojuego_id})

    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.parent.deiconify()
        self.destroy()



class EliminarVideojuego(tk.Toplevel):
    def __init__(self, parent, db, jugador_id):
        super().__init__(parent)
        self.title("Eliminar Videojuego")
        self.parent = parent
        self.db = db
        self.jugador_id = jugador_id

        self.videojuegos = self.db['videojuegos']

        label_titulo = ttk.Label(self, text="Título del Videojuego:")
        label_titulo.grid(row=0, column=0, padx=5, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        button_eliminar = ttk.Button(self, text="Eliminar Videojuego", command=self.eliminar_videojuego)
        button_eliminar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def eliminar_videojuego(self):
        titulo_videojuego = self.ask_for_videojuego()
        if titulo_videojuego:
            videojuego = self.db['videojuegos'].find_one({"Titulo": titulo_videojuego, "Jugador_ID": self.jugador_id})
            if videojuego:
                videojuego_id = videojuego['_id']
                print(f"Eliminando videojuego con ID: {videojuego_id}")
                # Buscar colecciones asociadas al videojuego y eliminarlas
                result = self.db['colecciones'].delete_many({"Videojuego_ID": videojuego_id})
                print(f"Eliminados {result.deleted_count} documentos de colección")
                # Eliminar el videojuego
                result = self.db['videojuegos'].delete_one({"_id": videojuego_id})
                print(f"Eliminados {result.deleted_count} videojuegos")
                messagebox.showinfo("Éxito", f"Videojuego '{titulo_videojuego}' y sus datos de colección asociados eliminados correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró un videojuego con ese título para este jugador.")

    def close_window(self):
        self.parent.deiconify()
        self.destroy()
            
class EliminarJugador(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Eliminar Jugador")
        self.parent = parent
        self.db = db

        self.collection = self.db['jugadores']

        label_nombre = ttk.Label(self, text="Nombre del Jugador:")
        label_nombre.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        button_eliminar = ttk.Button(self, text="Eliminar Jugador", command=self.eliminar_jugador)
        button_eliminar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def eliminar_jugador(self):
        try:
            nombre = self.entry_nombre.get().strip()

            jugador = self.collection.find_one({"Nombre": nombre})

            if jugador:
                self.collection.delete_one({"Nombre": nombre})
                messagebox.showinfo("Éxito", "Jugador eliminado correctamente.")
                self.back_to_parent()  # Añadir esta línea para volver a la ventana principal
            else:
                messagebox.showerror("Error", "No se encontró un jugador con ese nombre.")
        except errors.PyMongoError as e:
            messagebox.showerror("Error", f"Error al eliminar el jugador: {e}")

    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.parent.deiconify()
        self.destroy()


class ListaJugadores(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Lista de Jugadores")
        self.parent = parent
        self.db = db

        self.collection = self.db['jugadores']

        jugadores = self.collection.find()

        text_area = tk.Text(self)
        text_area.pack(expand=True, fill='both')

        for jugador in jugadores:
            text_area.insert(tk.END, f"Nombre: {jugador['Nombre']}, Edad: {jugador['Edad']}, País: {jugador['Pais']}\n")
        
        self.button_volver = ttk.Button(self, text="Volver", command=self.back_to_parent)
        self.button_volver.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def back_to_parent(self):
        self.parent.deiconify()
        self.destroy()

    def close_window(self):
        self.parent.deiconify()
        self.destroy()


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")

        self.db_client = MongoClient("mongodb://192.168.0.22/")
        self.db = self.db_client["videojuegos_db"]

        self.button_registrar_jugador = ttk.Button(self, text="Registrar Jugador", command=self.open_registrar_jugador)
        self.button_registrar_jugador.grid(row=0, column=0, padx=10, pady=10)

        self.button_iniciar_cuenta = ttk.Button(self, text="Iniciar Cuenta", command=self.open_iniciar_cuenta)
        self.button_iniciar_cuenta.grid(row=1, column=0, padx=10, pady=10)

        self.button_eliminar_jugador = ttk.Button(self, text="Eliminar Jugador", command=self.open_eliminar_jugador)
        self.button_eliminar_jugador.grid(row=2, column=0, padx=10, pady=10)

        self.button_lista_jugadores = ttk.Button(self, text="Lista de Jugadores", command=self.open_lista_jugadores)
        self.button_lista_jugadores.grid(row=3, column=0, padx=10, pady=10)

        self.button_salir = ttk.Button(self, text="Salir", command=self.close_app)
        self.button_salir.grid(row=4, column=0, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def open_lista_jugadores(self):
        self.withdraw()
        ListaJugadores(self, self.db)

    def close_app(self):
        self.db_client.close()
        self.destroy()

    def open_registrar_jugador(self):
        self.withdraw()
        RegistroJugador(self, self.db)

    def open_iniciar_cuenta(self):
        self.withdraw()
        IniciarCuenta(self, self.db)

    def open_eliminar_jugador(self):
        self.withdraw()
        EliminarJugador(self, self.db)

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()