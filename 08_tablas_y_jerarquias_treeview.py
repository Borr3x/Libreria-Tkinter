"""
08_tablas_y_jerarquias_treeview.py
==================================
Dominio del widget ttk.Treeview para visualización de datos y jerarquías:
- Modo Tabla Tabular (Columnas, encabezados, alineaciones y anchos personalizados).
- Ordenamiento interactivo al hacer clic en los encabezados (ascendente / descendente).
- Modo Árbol Jerárquico (Nodos padre, subnodos, carpetas y archivos).
- Operaciones CRUD completas: Agregar registro, Editar seleccionado y Eliminar.
- Barra de búsqueda y filtrado en tiempo real.
- Integración de barras de desplazamiento (Scrollbars vertical y horizontal).
"""

import tkinter as tk
from tkinter import messagebox, ttk


class TreeviewApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("08 - Tablas y Árboles con ttk.Treeview")
        self.root.geometry("920x680")
        self.root.minsize(800, 580)
        self.root.configure(bg="#F1F5F9")

        # Datos de ejemplo iniciales (ID, Nombre, Rol, Departamento, Salario)
        self.datos_empleados = [
            (101, "Ana Morales", "Frontend Lead", "Tecnología", 48000),
            (102, "Carlos Rivas", "Data Engineer", "Datos", 52000),
            (103, "Lucía Méndez", "Product Manager", "Producto", 61000),
            (104, "David Ortiz", "DevOps Engineer", "Infraestructura", 55000),
            (105, "Elena Cruz", "UX Designer", "Diseño", 43000),
            (106, "Fernando Gil", "Backend Senior", "Tecnología", 54000),
            (107, "Gabriela Paz", "QA Specialist", "Calidad", 41000),
            (108, "Hugo Salazar", "Security Analyst", "Seguridad", 59000),
        ]

        self.orden_ascendente = {col: True for col in ("ID", "Nombre", "Rol", "Depto", "Salario")}

        self._crear_interfaz()
        self._cargar_datos_tabla()
        self._cargar_datos_arbol()

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Visualización de Datos y Jerarquías (ttk.Treeview)",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Explora el Treeview en modo tabla con CRUD, ordenamiento dinámico y filtrado, y en modo árbol de carpetas.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w", pady=(2, 0))

        # Cuaderno de pestañas
        cuaderno = ttk.Notebook(self.root)
        cuaderno.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tab_tabla = ttk.Frame(cuaderno, padding=12)
        tab_arbol = ttk.Frame(cuaderno, padding=12)

        cuaderno.add(tab_tabla, text="  1. Modo Tabla Tabular (CRUD y Filtros)  ")
        cuaderno.add(tab_arbol, text="  2. Modo Árbol Jerárquico  ")

        self._construir_tab_tabla(tab_tabla)
        self._construir_tab_arbol(tab_arbol)

    # -------------------------------------------------------------
    # 1. MODO TABLA TABULAR (CRUD)
    # -------------------------------------------------------------
    def _construir_tab_tabla(self, contenedor: ttk.Frame) -> None:
        # Barra superior: Búsqueda y botones de acción
        barra_herramientas = tk.Frame(contenedor, bg="#F1F5F9")
        barra_herramientas.pack(fill=tk.X, pady=(0, 10))

        tk.Label(barra_herramientas, text="🔍 Buscar:", font=("Helvetica", 9, "bold"), bg="#F1F5F9").pack(side=tk.LEFT, padx=(0, 5))
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *_: self._filtrar_tabla())
        txt_buscar = tk.Entry(barra_herramientas, textvariable=self.var_buscar, font=("Helvetica", 9), width=24, relief=tk.SOLID, bd=1)
        txt_buscar.pack(side=tk.LEFT, padx=(0, 15))

        btn_agregar = tk.Button(barra_herramientas, text="➕ Nuevo Registro", bg="#10B981", fg="white", font=("Helvetica", 9, "bold"), relief=tk.FLAT, padx=10, pady=4, command=self._dialogo_agregar)
        btn_agregar.pack(side=tk.LEFT, padx=3)

        btn_eliminar = tk.Button(barra_herramientas, text="🗑️ Eliminar Fila", bg="#EF4444", fg="white", font=("Helvetica", 9), relief=tk.FLAT, padx=10, pady=4, command=self._eliminar_seleccionado)
        btn_eliminar.pack(side=tk.LEFT, padx=3)

        # Contenedor del Treeview con Scrollbars
        frame_tree = tk.Frame(contenedor)
        frame_tree.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(frame_tree, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal")

        columnas = ("ID", "Nombre", "Rol", "Depto", "Salario")
        self.tree_tabla = ttk.Treeview(
            frame_tree,
            columns=columnas,
            show="headings",
            selectmode="browse",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree_tabla.yview)
        scroll_x.config(command=self.tree_tabla.xview)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de columnas y encabezados interactivos
        anchos = {"ID": 60, "Nombre": 180, "Rol": 160, "Depto": 140, "Salario": 120}
        alineaciones = {"ID": "center", "Nombre": "w", "Rol": "w", "Depto": "center", "Salario": "e"}

        for col in columnas:
            self.tree_tabla.heading(col, text=col, command=lambda c=col: self._ordenar_por_columna(c))
            self.tree_tabla.column(col, width=anchos[col], anchor=alineaciones[col])

        # Estilo de filas alternadas (striped rows)
        self.tree_tabla.tag_configure("par", background="#F8FAFC")
        self.tree_tabla.tag_configure("impar", background="#FFFFFF")

        # Doble clic para editar
        self.tree_tabla.bind("<Double-1>", lambda _: self._dialogo_editar())

        # Nota al pie
        tk.Label(
            contenedor,
            text="💡 Tip: Haz clic en cualquier encabezado para ordenar ascendentemente/descendentemente. Haz doble clic en una fila para editar.",
            font=("Helvetica", 8, "italic"),
            fg="#64748B",
            bg="#F1F5F9"
        ).pack(anchor="w", pady=(8, 0))

    def _cargar_datos_tabla(self, datos=None) -> None:
        """Limpia y rellena las filas de la tabla."""
        for fila in self.tree_tabla.get_children():
            self.tree_tabla.delete(fila)

        filas = datos if datos is not None else self.datos_empleados
        for i, emp in enumerate(filas):
            tag = "par" if i % 2 == 0 else "impar"
            salario_formateado = f"${emp[4]:,}"
            self.tree_tabla.insert("", tk.END, iid=str(emp[0]), values=(emp[0], emp[1], emp[2], emp[3], salario_formateado), tags=(tag,))

    def _filtrar_tabla(self) -> None:
        criterio = self.var_buscar.get().lower().strip()
        if not criterio:
            self._cargar_datos_tabla()
            return

        filtrados = [
            emp for emp in self.datos_empleados
            if criterio in str(emp[0]).lower()
            or criterio in emp[1].lower()
            or criterio in emp[2].lower()
            or criterio in emp[3].lower()
        ]
        self._cargar_datos_tabla(filtrados)

    def _ordenar_por_columna(self, columna: str) -> None:
        """Ordena los elementos de la tabla según la columna pulsada."""
        idx_map = {"ID": 0, "Nombre": 1, "Rol": 2, "Depto": 3, "Salario": 4}
        col_idx = idx_map[columna]
        asc = self.orden_ascendente[columna]

        self.datos_empleados.sort(
            key=lambda x: x[col_idx],
            reverse=not asc
        )
        self.orden_ascendente[columna] = not asc

        # Actualizar flecha en encabezados
        for col in self.orden_ascendente:
            simbolo = " ▲" if not self.orden_ascendente[col] else " ▼"
            texto_base = col
            self.tree_tabla.heading(col, text=f"{texto_base}{simbolo if col == columna else ''}")

        self._filtrar_tabla()

    def _dialogo_agregar(self) -> None:
        self._abrir_formulario_edicion(titulo="Agregar Nuevo Empleado", emp_existente=None)

    def _dialogo_editar(self) -> None:
        seleccion = self.tree_tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un registro para editar.")
            return

        item_id = int(seleccion[0])
        empleado = next((e for e in self.datos_empleados if e[0] == item_id), None)
        if empleado:
            self._abrir_formulario_edicion(titulo=f"Editar Registro #{item_id}", emp_existente=empleado)

    def _abrir_formulario_edicion(self, titulo: str, emp_existente=None) -> None:
        dlg = tk.Toplevel(self.root)
        dlg.title(titulo)
        dlg.geometry("380x320")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        frame = tk.Frame(dlg, padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        campos = ["ID", "Nombre", "Rol", "Departamento", "Salario ($)"]
        entries = {}

        for i, campo in enumerate(campos):
            tk.Label(frame, text=f"{campo}:", font=("Helvetica", 9, "bold")).grid(row=i, column=0, sticky="w", pady=4)
            ent = tk.Entry(frame, font=("Helvetica", 9), relief=tk.SOLID, bd=1)
            ent.grid(row=i, column=1, sticky="ew", pady=4, padx=(10, 0))
            entries[campo] = ent

        frame.columnconfigure(1, weight=1)

        # Si estamos editando, cargar valores previos
        if emp_existente:
            entries["ID"].insert(0, str(emp_existente[0]))
            entries["ID"].config(state="disabled")
            entries["Nombre"].insert(0, emp_existente[1])
            entries["Rol"].insert(0, emp_existente[2])
            entries["Departamento"].insert(0, emp_existente[3])
            entries["Salario ($)"].insert(0, str(emp_existente[4]))
        else:
            siguiente_id = max((e[0] for e in self.datos_empleados), default=100) + 1
            entries["ID"].insert(0, str(siguiente_id))

        def guardar():
            try:
                emp_id = int(entries["ID"].get().strip())
                nombre = entries["Nombre"].get().strip()
                rol = entries["Rol"].get().strip()
                depto = entries["Departamento"].get().strip()
                salario = int(entries["Salario ($)"].get().replace("$", "").replace(",", "").strip())

                if not nombre or not rol:
                    messagebox.showerror("Error", "Nombre y Rol son obligatorios.", parent=dlg)
                    return

                if emp_existente:
                    # Modificar en la lista
                    idx = next(i for i, e in enumerate(self.datos_empleados) if e[0] == emp_id)
                    self.datos_empleados[idx] = (emp_id, nombre, rol, depto, salario)
                else:
                    self.datos_empleados.append((emp_id, nombre, rol, depto, salario))

                self._filtrar_tabla()
                dlg.destroy()
            except ValueError:
                messagebox.showerror("Error", "El salario debe ser un número entero válido.", parent=dlg)

        btn_guardar = tk.Button(frame, text="Guardar Registro", bg="#2563EB", fg="white", font=("Helvetica", 9, "bold"), relief=tk.FLAT, pady=6, command=guardar)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, sticky="ew", pady=(15, 0))

    def _eliminar_seleccionado(self) -> None:
        seleccion = self.tree_tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una fila para eliminar.")
            return

        item_id = int(seleccion[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el registro #{item_id}?")
        if confirm:
            self.datos_empleados = [e for e in self.datos_empleados if e[0] != item_id]
            self._filtrar_tabla()

    # -------------------------------------------------------------
    # 2. MODO ÁRBOL JERÁRQUICO
    # -------------------------------------------------------------
    def _construir_tab_arbol(self, contenedor: ttk.Frame) -> None:
        lbl_info = tk.Label(
            contenedor,
            text="Treeview en modo árbol (#0 como columna jerárquica):\n"
                 "Muestra estructuras jerárquicas como carpetas, categorías y archivos con iconos/símbolos expansibles.",
            font=("Helvetica", 9),
            justify=tk.LEFT
        )
        lbl_info.pack(anchor="w", pady=(0, 10))

        frame_arbol = tk.Frame(contenedor)
        frame_arbol.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(frame_arbol, orient="vertical")
        self.tree_jerarquia = ttk.Treeview(frame_arbol, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree_jerarquia.yview)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_jerarquia.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_jerarquia.heading("#0", text="Estructura del Proyecto (Explorador de Archivos)", anchor="w")

    def _cargar_datos_arbol(self) -> None:
        # Raíz
        raiz = self.tree_jerarquia.insert("", tk.END, text="📁 mi_proyecto_python", open=True)

        # Carpetas de nivel 1
        src = self.tree_jerarquia.insert(raiz, tk.END, text="📁 src", open=True)
        tests = self.tree_jerarquia.insert(raiz, tk.END, text="📁 tests", open=True)
        docs = self.tree_jerarquia.insert(raiz, tk.END, text="📁 docs", open=False)

        # Archivos dentro de src
        self.tree_jerarquia.insert(src, tk.END, text="🐍 main.py")
        self.tree_jerarquia.insert(src, tk.END, text="🐍 app.py")
        self.tree_jerarquia.insert(src, tk.END, text="🐍 utils.py")

        # Subcarpeta dentro de src
        assets = self.tree_jerarquia.insert(src, tk.END, text="📁 assets", open=False)
        self.tree_jerarquia.insert(assets, tk.END, text="🖼️ icon.ico")
        self.tree_jerarquia.insert(assets, tk.END, text="🎨 theme.tcl")

        # Archivos de tests y docs
        self.tree_jerarquia.insert(tests, tk.END, text="🐍 test_core.py")
        self.tree_jerarquia.insert(tests, tk.END, text="🐍 test_gui.py")
        self.tree_jerarquia.insert(docs, tk.END, text="📄 README.md")
        self.tree_jerarquia.insert(docs, tk.END, text="📄 architecture.pdf")

        # Archivos raíz
        self.tree_jerarquia.insert(raiz, tk.END, text="⚙️ pyproject.toml")
        self.tree_jerarquia.insert(raiz, tk.END, text="📄 LICENSE")


def main():
    root = tk.Tk()
    app = TreeviewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
