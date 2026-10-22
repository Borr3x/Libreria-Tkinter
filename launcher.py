"""
launcher.py
===========
Lanzador Interactivo y Panel de Control del Repositorio Tkinter Showcase.
Permite explorar, filtrar y ejecutar con un solo clic cualquiera de los 10 módulos
de demostración incluidos en el repositorio, además de inspeccionar sus objetivos.
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))

MODULOS = [
    {
        "id": "01",
        "archivo": "01_fundamentos_y_conceptos_basicos.py",
        "titulo": "01. Fundamentos y Conceptos Básicos",
        "nivel": "Principiante",
        "color_nivel": "#10B981",
        "descripcion": "Ciclo mainloop(), centrado de ventanas, widgets básicos (Label, Button, Entry), variables reactivas StringVar e IntVar y modificación de propiedades."
    },
    {
        "id": "02",
        "archivo": "02_gestores_de_posicionamiento.py",
        "titulo": "02. Gestores de Posicionamiento",
        "nivel": "Principiante",
        "color_nivel": "#10B981",
        "descripcion": "Comparación visual y práctica de los tres gestores de geometría de Tkinter: pack() lineal, grid() en cuadrícula matricial y place() por coordenadas."
    },
    {
        "id": "03",
        "archivo": "03_widgets_interactivos_formulario.py",
        "titulo": "03. Widgets Interactivos y Formulario",
        "nivel": "Intermedio",
        "color_nivel": "#3B82F6",
        "descripcion": "Catálogo completo de entrada: Checkbutton, Radiobutton, Entry con contraseña, Combobox, Spinbox, Scale y panel reactivo de datos en formato JSON."
    },
    {
        "id": "04",
        "archivo": "04_canvas_y_dibujo_grafico.py",
        "titulo": "04. Canvas: Dibujo Gráfico y Animaciones",
        "nivel": "Intermedio",
        "color_nivel": "#3B82F6",
        "descripcion": "Primitivas vectoriales (líneas, rectángulos, óvalos, polígonos), pizarra de dibujo libre a mano alzada y física de rebote animada a 60 FPS con after()."
    },
    {
        "id": "05",
        "archivo": "05_dialogos_ventanas_secundarias.py",
        "titulo": "05. Diálogos Nativos y Ventanas Modales",
        "nivel": "Intermedio",
        "color_nivel": "#3B82F6",
        "descripcion": "Alertas nativas con messagebox, selección de archivos con filedialog, selector de color con colorchooser y ventanas emergentes modales con Toplevel."
    },
    {
        "id": "06",
        "archivo": "06_menus_eventos_y_atajos.py",
        "titulo": "06. Menús, Eventos y Atajos de Teclado",
        "nivel": "Intermedio",
        "color_nivel": "#3B82F6",
        "descripcion": "Barra de menú superior en cascada, menús contextuales emergentes (clic derecho), vinculación de eventos de ratón/teclado y barra de estado."
    },
    {
        "id": "07",
        "archivo": "07_estilos_modernos_ttk.py",
        "titulo": "07. Estilos Modernos y Temas ttk",
        "nivel": "Avanzado",
        "color_nivel": "#8B5CF6",
        "descripcion": "El motor ttk.Style, explorador de temas globales nativos ('clam', 'alt', 'default'), botones estilizados, progressbars y comparativa clásica vs moderna."
    },
    {
        "id": "08",
        "archivo": "08_tablas_y_jerarquias_treeview.py",
        "titulo": "08. Tablas y Jerarquías con ttk.Treeview",
        "nivel": "Avanzado",
        "color_nivel": "#8B5CF6",
        "descripcion": "Modo tabla tabular con operaciones CRUD completas, ordenamiento dinámico por columnas al hacer clic, buscador en vivo y modo árbol de carpetas."
    },
    {
        "id": "09",
        "archivo": "09_multihilo_y_tareas_en_segundo_plano.py",
        "titulo": "09. Multihilo y Tareas en Segundo Plano",
        "nivel": "Avanzado",
        "color_nivel": "#8B5CF6",
        "descripcion": "Solución a la congelación de la interfaz mediante threading.Thread, cola de mensajes queue.Queue y polling no bloqueante con after()."
    },
    {
        "id": "10",
        "archivo": "10_proyecto_integrador_gestor_tareas.py",
        "titulo": "10. Proyecto Integrador: TaskFlow Pro",
        "nivel": "Proyecto Completo",
        "color_nivel": "#EC4899",
        "descripcion": "Aplicación de gestión de tareas completa: POO, almacenamiento JSON, dashboard estadístico en Canvas (Donut chart), filtros, modales y atajos."
    }
]


class LauncherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tkinter Python Showcase - Panel de Control y Lanzador")
        self.root.geometry("960x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#0F172A")

        self.filtro_nivel = "Todos"
        self.var_buscar = tk.StringVar()

        self._crear_interfaz()
        self._renderizar_tarjetas()

    def _crear_interfaz(self) -> None:
        # Encabezado principal
        header = tk.Frame(self.root, bg="#1E293B", padx=25, pady=18)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🐍 Tkinter Python Mastery Showcase",
            font=("Helvetica", 18, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Repositorio didáctico con 10 módulos progresivos listos para ejecutar y estudiar.",
            font=("Helvetica", 10),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w", pady=(3, 0))

        # Barra de filtros y búsqueda
        barra_herramientas = tk.Frame(self.root, bg="#0F172A", padx=25, pady=12)
        barra_herramientas.pack(fill=tk.X)

        # Filtros por nivel
        frame_filtros = tk.Frame(barra_herramientas, bg="#0F172A")
        frame_filtros.pack(side=tk.LEFT)

        tk.Label(frame_filtros, text="Nivel:", font=("Helvetica", 9, "bold"), fg="#CBD5E1", bg="#0F172A").pack(side=tk.LEFT, padx=(0, 6))

        self.btns_nivel = {}
        for nivel in ["Todos", "Principiante", "Intermedio", "Avanzado", "Proyecto Completo"]:
            btn = tk.Button(
                frame_filtros,
                text=nivel,
                font=("Helvetica", 8, "bold"),
                relief=tk.FLAT,
                padx=8,
                pady=3,
                bg="#1E293B",
                fg="#94A3B8",
                cursor="hand2",
                command=lambda n=nivel: self._cambiar_filtro_nivel(n)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.btns_nivel[nivel] = btn

        self._actualizar_botones_nivel()

        # Buscador
        frame_busc = tk.Frame(barra_herramientas, bg="#0F172A")
        frame_busc.pack(side=tk.RIGHT)

        tk.Label(frame_busc, text="🔍", font=("Helvetica", 10), fg="#94A3B8", bg="#0F172A").pack(side=tk.LEFT, padx=(0, 4))
        self.var_buscar.trace_add("write", lambda *_: self._renderizar_tarjetas())
        txt_busc = tk.Entry(frame_busc, textvariable=self.var_buscar, font=("Helvetica", 9), width=22, relief=tk.SOLID, bd=1)
        txt_busc.pack(side=tk.LEFT)

        # Contenedor con Scrollbar para las tarjetas de módulos
        contenedor_scroll = tk.Frame(self.root, bg="#0F172A")
        contenedor_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.canvas_scroll = tk.Canvas(contenedor_scroll, bg="#0F172A", highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor_scroll, orient="vertical", command=self.canvas_scroll.yview)

        self.frame_tarjetas = tk.Frame(self.canvas_scroll, bg="#0F172A")
        self.frame_tarjetas.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )

        self.canvas_window = self.canvas_scroll.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)

        self.canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Ajustar ancho del frame interno al redimensionar la ventana
        self.canvas_scroll.bind("<Configure>", self._ajustar_ancho_canvas)

        # Barra de estado inferior
        frame_status = tk.Frame(self.root, bg="#1E293B", padx=15, pady=8)
        frame_status.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_status = tk.Label(frame_status, text="Listo.", font=("Helvetica", 9), fg="#94A3B8", bg="#1E293B")
        self.lbl_status.pack(side=tk.LEFT)

        tk.Label(
            frame_status,
            text=f"Directorio: {DIRECTORIO_ACTUAL}",
            font=("Consolas", 8),
            fg="#64748B",
            bg="#1E293B"
        ).pack(side=tk.RIGHT)

    def _ajustar_ancho_canvas(self, evento: tk.Event) -> None:
        self.canvas_scroll.itemconfig(self.canvas_window, width=evento.width)

    def _cambiar_filtro_nivel(self, nivel: str) -> None:
        self.filtro_nivel = nivel
        self._actualizar_botones_nivel()
        self._renderizar_tarjetas()

    def _actualizar_botones_nivel(self) -> None:
        for n, btn in self.btns_nivel.items():
            if n == self.filtro_nivel:
                btn.config(bg="#2563EB", fg="white")
            else:
                btn.config(bg="#1E293B", fg="#94A3B8")

    def _renderizar_tarjetas(self) -> None:
        # Limpiar tarjetas actuales
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        criterio = self.var_buscar.get().lower().strip()
        modulos_filtrados = []

        for m in MODULOS:
            if self.filtro_nivel != "Todos" and m["nivel"] != self.filtro_nivel:
                continue
            if criterio and (criterio not in m["titulo"].lower() and criterio not in m["descripcion"].lower()):
                continue
            modulos_filtrados.append(m)

        for mod in modulos_filtrados:
            card = tk.Frame(self.frame_tarjetas, bg="#1E293B", relief=tk.FLAT, padx=16, pady=12)
            card.pack(fill=tk.X, pady=6, padx=5)

            # Fila superior de la tarjeta: Título + Badge de nivel + Botón de ejecución
            fila_sup = tk.Frame(card, bg="#1E293B")
            fila_sup.pack(fill=tk.X)

            lbl_tit = tk.Label(fila_sup, text=mod["titulo"], font=("Helvetica", 11, "bold"), fg="#F8FAFC", bg="#1E293B")
            lbl_tit.pack(side=tk.LEFT)

            # Badge de nivel
            badge = tk.Label(
                fila_sup,
                text=f" {mod['nivel']} ",
                font=("Helvetica", 7, "bold"),
                bg=mod["color_nivel"],
                fg="white",
                padx=4,
                pady=1
            )
            badge.pack(side=tk.LEFT, padx=10)

            # Botón ejecutar
            btn_ejecutar = tk.Button(
                fila_sup,
                text="▶ Ejecutar Módulo",
                font=("Helvetica", 9, "bold"),
                bg="#2563EB",
                fg="white",
                activebackground="#1D4ED8",
                activeforeground="white",
                relief=tk.FLAT,
                padx=12,
                pady=4,
                cursor="hand2",
                command=lambda arch=mod["archivo"]: self._ejecutar_archivo(arch)
            )
            btn_ejecutar.pack(side=tk.RIGHT)

            # Descripción del módulo
            lbl_desc = tk.Label(
                card,
                text=mod["descripcion"],
                font=("Helvetica", 9),
                fg="#94A3B8",
                bg="#1E293B",
                justify=tk.LEFT,
                wraplength=760
            )
            lbl_desc.pack(anchor="w", pady=(6, 0))

        self.lbl_status.config(text=f"Mostrando {len(modulos_filtrados)} de {len(MODULOS)} módulos disponibles.")

    def _ejecutar_archivo(self, nombre_archivo: str) -> None:
        ruta_completa = os.path.join(DIRECTORIO_ACTUAL, nombre_archivo)
        if not os.path.exists(ruta_completa):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_completa}")
            return

        try:
            # Lanzar el proceso de Python en paralelo
            subprocess.Popen([sys.executable, ruta_completa])
            self.lbl_status.config(text=f"Lanzado con éxito: {nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error de Ejecución", f"Fallo al ejecutar el script:\n{e}")


def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
