"""
02_gestores_de_posicionamiento.py
================================
Demostración visual y comparativa de los tres gestores de geometría de Tkinter:
1. pack()  - Empaquetamiento lineal (top, bottom, left, right, fill, expand).
2. grid()  - Cuadrícula matricial (filas, columnas, sticky, rowspan, columnspan, weights).
3. place() - Coordenadas absolutas (x, y) y relativas (relx, rely, relwidth, relheight).

Regla de oro de Tkinter demostrada: NUNCA mezcles pack() y grid() dentro del MISMO
contenedor o Frame padre, ya que provocará un bloqueo o bucle infinito de renderizado.
"""

import tkinter as tk
from tkinter import ttk


class GestoresGeometriaApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("02 - Gestores de Posicionamiento (pack, grid, place)")
        self.root.geometry("820x620")
        self.root.minsize(700, 500)
        self.root.configure(bg="#0F172A")

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        # Encabezado informativo
        header = tk.Frame(self.root, bg="#1E293B", padx=20, pady=15)
        header.pack(fill=tk.X)

        lbl_tit = tk.Label(
            header,
            text="Sistemas de Geometría en Tkinter",
            font=("Helvetica", 16, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        )
        lbl_tit.pack(anchor="w")

        lbl_desc = tk.Label(
            header,
            text="Explora las 3 formas de estructurar y distribuir interfaces: pack(), grid() y place().",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#1E293B"
        )
        lbl_desc.pack(anchor="w", pady=(3, 0))

        # Cuaderno de pestañas (Notebook de ttk)
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TNotebook", background="#0F172A", borderwidth=0)
        estilo.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[16, 8])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Crear frames para cada pestaña
        tab_pack = tk.Frame(notebook, bg="#F8FAFC")
        tab_grid = tk.Frame(notebook, bg="#F8FAFC")
        tab_place = tk.Frame(notebook, bg="#F8FAFC")

        notebook.add(tab_pack, text="  1. pack()  ")
        notebook.add(tab_grid, text="  2. grid()  ")
        notebook.add(tab_place, text="  3. place()  ")

        # Construir cada pestaña
        self._construir_tab_pack(tab_pack)
        self._construir_tab_grid(tab_grid)
        self._construir_tab_place(tab_place)

    # -------------------------------------------------------------
    # 1. PESTAÑA: pack()
    # -------------------------------------------------------------
    def _construir_tab_pack(self, contenedor: tk.Frame) -> None:
        # Explicación superior
        info = tk.Label(
            contenedor,
            text="El gestor pack() organiza elementos apilándolos linealmente contra los bordes\n"
                 "(TOP, BOTTOM, LEFT, RIGHT). Soporta 'fill' (X, Y, BOTH) y 'expand' (True/False).",
            font=("Helvetica", 9),
            bg="#E2E8F0",
            fg="#1E293B",
            justify=tk.LEFT,
            padx=12,
            pady=8
        )
        info.pack(fill=tk.X, padx=15, pady=(15, 10))

        # Panel de demostración visual
        demo_frame = tk.Frame(contenedor, bg="#FFFFFF", relief=tk.GROOVE, bd=2)
        demo_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Bloque TOP
        lbl_top = tk.Label(
            demo_frame,
            text="side=TOP, fill=X\nOcupa todo el ancho superior",
            bg="#3B82F6",
            fg="white",
            font=("Helvetica", 9, "bold"),
            pady=10
        )
        lbl_top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=4)

        # Bloque BOTTOM
        lbl_bottom = tk.Label(
            demo_frame,
            text="side=BOTTOM, fill=X\nFijado en la parte inferior",
            bg="#64748B",
            fg="white",
            font=("Helvetica", 9, "bold"),
            pady=10
        )
        lbl_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=4)

        # Bloque LEFT
        lbl_left = tk.Label(
            demo_frame,
            text="side=LEFT\nfill=Y\nBarra lateral",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=15
        )
        lbl_left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=4)

        # Bloque RIGHT
        lbl_right = tk.Label(
            demo_frame,
            text="side=RIGHT\nfill=Y\nPanel derecho",
            bg="#F59E0B",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=15
        )
        lbl_right.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=4)

        # Bloque CENTER (expand=True, fill=BOTH)
        lbl_center = tk.Label(
            demo_frame,
            text="side=TOP, expand=True, fill=BOTH\n\nEste elemento se expande dinámicamente\n"
                 "para reclamar todo el espacio restante disponible.",
            bg="#8B5CF6",
            fg="white",
            font=("Helvetica", 10, "bold")
        )
        lbl_center.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=8, pady=4)

    # -------------------------------------------------------------
    # 2. PESTAÑA: grid()
    # -------------------------------------------------------------
    def _construir_tab_grid(self, contenedor: tk.Frame) -> None:
        info = tk.Label(
            contenedor,
            text="El gestor grid() distribuye elementos en filas (row) y columnas (column) como una hoja de cálculo.\n"
                 "Soporta 'columnspan', 'rowspan', anclaje con 'sticky' (N, S, E, W) y distribución con weight.",
            font=("Helvetica", 9),
            bg="#E2E8F0",
            fg="#1E293B",
            justify=tk.LEFT,
            padx=12,
            pady=8
        )
        info.pack(fill=tk.X, padx=15, pady=(15, 10))

        # Formulario de ejemplo usando grid
        formulario = tk.Frame(contenedor, bg="#FFFFFF", relief=tk.GROOVE, bd=2, padx=20, pady=20)
        formulario.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Configurar pesos de columnas para responsividad
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(2, weight=1)

        # Fila 0: Título que abarca 3 columnas (columnspan=3)
        lbl_header = tk.Label(
            formulario,
            text="Formulario Responsivo con Cuadrícula (grid)",
            font=("Helvetica", 12, "bold"),
            bg="#0284C7",
            fg="white",
            pady=6
        )
        lbl_header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))

        # Fila 1: Nombre
        tk.Label(formulario, text="Nombre Completo:", font=("Helvetica", 10, "bold"), bg="white").grid(
            row=1, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        tk.Entry(formulario, font=("Helvetica", 10), relief=tk.SOLID, bd=1).grid(
            row=1, column=1, columnspan=2, sticky="ew", pady=8
        )

        # Fila 2: Correo
        tk.Label(formulario, text="Correo Electrónico:", font=("Helvetica", 10, "bold"), bg="white").grid(
            row=2, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        tk.Entry(formulario, font=("Helvetica", 10), relief=tk.SOLID, bd=1).grid(
            row=2, column=1, columnspan=2, sticky="ew", pady=8
        )

        # Fila 3: Teléfono y Ciudad en la misma fila
        tk.Label(formulario, text="Teléfono:", font=("Helvetica", 10, "bold"), bg="white").grid(
            row=3, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        tk.Entry(formulario, font=("Helvetica", 10), relief=tk.SOLID, bd=1).grid(
            row=3, column=1, sticky="ew", pady=8, padx=(0, 5)
        )
        tk.Entry(formulario, font=("Helvetica", 10), relief=tk.SOLID, bd=1).grid(
            row=3, column=2, sticky="ew", pady=8, padx=(5, 0)
        )

        # Fila 4: Comentarios (rowspan=2 para etiqueta o caja)
        tk.Label(formulario, text="Notas:", font=("Helvetica", 10, "bold"), bg="white").grid(
            row=4, column=0, sticky="nw", pady=8, padx=(0, 10)
        )
        txt_notas = tk.Text(formulario, height=4, font=("Helvetica", 9), relief=tk.SOLID, bd=1)
        txt_notas.grid(row=4, column=1, columnspan=2, sticky="nsew", pady=8)
        txt_notas.insert(tk.END, "El gestor grid permite alinear campos complejos de forma limpia y ordenada.")

        # Fila 5: Botones alineados a la derecha
        btn_frame = tk.Frame(formulario, bg="white")
        btn_frame.grid(row=5, column=0, columnspan=3, sticky="e", pady=(15, 0))

        tk.Button(btn_frame, text="Cancelar", bg="#94A3B8", fg="white", font=("Helvetica", 9), relief=tk.FLAT, padx=12, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar Información", bg="#059669", fg="white", font=("Helvetica", 9, "bold"), relief=tk.FLAT, padx=15, pady=5).pack(side=tk.LEFT)

    # -------------------------------------------------------------
    # 3. PESTAÑA: place()
    # -------------------------------------------------------------
    def _construir_tab_place(self, contenedor: tk.Frame) -> None:
        info = tk.Label(
            contenedor,
            text="El gestor place() sitúa elementos por coordenadas fijas (x, y) o porcentuales/relativas\n"
                 "(relx, rely, relwidth, relheight). Es ideal para interfaces fijas, capas flotantes o juegos.",
            font=("Helvetica", 9),
            bg="#E2E8F0",
            fg="#1E293B",
            justify=tk.LEFT,
            padx=12,
            pady=8
        )
        info.pack(fill=tk.X, padx=15, pady=(15, 10))

        canvas_area = tk.Frame(contenedor, bg="#1E1E2E", relief=tk.SUNKEN, bd=2)
        canvas_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Tarjeta 1: Coordenadas absolutas
        card1 = tk.Frame(canvas_area, bg="#EC4899", padx=10, pady=10)
        card1.place(x=30, y=30, width=220, height=120)
        tk.Label(card1, text="Posición Absoluta:", font=("Helvetica", 9, "bold"), fg="white", bg="#EC4899").pack(anchor="w")
        tk.Label(card1, text="x = 30px, y = 30px\nwidth = 220px\nheight = 120px", font=("Helvetica", 9), fg="#FDF2F8", bg="#EC4899").pack(anchor="w", pady=4)

        # Tarjeta 2: Coordenadas relativas porcentuales al tamaño del contenedor
        card2 = tk.Frame(canvas_area, bg="#6366F1", padx=10, pady=10)
        card2.place(relx=0.55, rely=0.08, relwidth=0.40, relheight=0.42)
        tk.Label(card2, text="Posición Relativa:", font=("Helvetica", 9, "bold"), fg="white", bg="#6366F1").pack(anchor="w")
        tk.Label(card2, text="relx = 55%\nrely = 8%\nrelwidth = 40%\nrelheight = 42%\n(Se escala automáticamente)", font=("Helvetica", 9), fg="#EEF2FF", bg="#6366F1").pack(anchor="w", pady=4)

        # Botón flotante central centrado usando anchor="center"
        btn_flotante = tk.Button(
            canvas_area,
            text="★ Botón Flotante en el Centro Exacto (relx=0.5, rely=0.75) ★",
            font=("Helvetica", 10, "bold"),
            bg="#FBBF24",
            fg="#1E293B",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=10
        )
        btn_flotante.place(relx=0.5, rely=0.75, anchor="center")


def main():
    root = tk.Tk()
    app = GestoresGeometriaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
