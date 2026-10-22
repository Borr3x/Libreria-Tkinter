"""
10_proyecto_integrador_gestor_tareas.py
======================================
Proyecto Integrador Final: "TaskFlow - Gestor de Tareas y Productividad"
Combina todas las funcionalidades aprendidas a lo largo del repositorio:
- Arquitectura Orientada a Objetos (POO) limpia y estructurada.
- Persistencia de datos en disco local (formato JSON).
- Visualización de datos tabulares con ttk.Treeview, tags coloreados y ordenamiento.
- Gráficos estadísticos vectoriales interactivos dibujados con tk.Canvas (Donut Chart).
- Ventanas modales para creación y edición de registros con validaciones.
- Filtros por estado, categorías y buscador en tiempo real.
- Barra de menú superior, atajos de teclado globales y menús contextuales.
- Diálogos de confirmación y selección de archivos con filedialog y messagebox.
"""

import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

ARCHIVO_DATOS_DEFECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.json")


class Tarea:
    """Modelo de datos que representa una tarea individual."""
    def __init__(self, id_tarea: int, titulo: str, categoria: str, prioridad: str, fecha_limite: str, estado: str = "Pendiente", descripcion: str = ""):
        self.id = id_tarea
        self.titulo = titulo
        self.categoria = categoria
        self.prioridad = prioridad  # Alta, Media, Baja
        self.fecha_limite = fecha_limite
        self.estado = estado        # Pendiente, En Progreso, Completada
        self.descripcion = descripcion

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "fecha_limite": self.fecha_limite,
            "estado": self.estado,
            "descripcion": self.descripcion
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_tarea=data["id"],
            titulo=data["titulo"],
            categoria=data.get("categoria", "General"),
            prioridad=data.get("prioridad", "Media"),
            fecha_limite=data.get("fecha_limite", ""),
            estado=data.get("estado", "Pendiente"),
            descripcion=data.get("descripcion", "")
        )


class GestorTareasApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TaskFlow Pro - Gestor Integral de Tareas")
        self.root.geometry("1000x720")
        self.root.minsize(880, 620)
        self.root.configure(bg="#F1F5F9")

        self.archivo_datos = ARCHIVO_DATOS_DEFECTO
        self.tareas = []
        self.filtro_estado = "Todas"
        self.var_busqueda = tk.StringVar()

        self._cargar_tareas_disco()
        self._configurar_estilos()
        self._crear_menus()
        self._crear_interfaz()
        self._vincular_atajos()
        self._actualizar_vista()

    # -------------------------------------------------------------
    # GESTIÓN Y PERSISTENCIA DE DATOS
    # -------------------------------------------------------------
    def _cargar_tareas_disco(self) -> None:
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.tareas = [Tarea.from_dict(item) for item in datos]
            except Exception as e:
                messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo de datos: {e}")
                self.tareas = self._generar_datos_semilla()
        else:
            self.tareas = self._generar_datos_semilla()
            self._guardar_tareas_disco()

    def _guardar_tareas_disco(self) -> None:
        try:
            with open(self.archivo_datos, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tareas], f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudieron persistir los datos: {e}")

    def _generar_datos_semilla(self) -> list:
        return [
            Tarea(1, "Configurar entorno de desarrollo", "Desarrollo", "Alta", "2026-10-25", "Completada", "Instalar Python y extensiones."),
            Tarea(2, "Diseñar interfaz de usuario en Tkinter", "Diseño", "Alta", "2026-10-28", "En Progreso", "Crear mockups y componentes."),
            Tarea(3, "Escribir documentación en README.md", "Documentación", "Media", "2026-10-30", "Pendiente", "Detallar funcionalidades y ejemplos."),
            Tarea(4, "Revisar cobertura de pruebas", "Calidad", "Baja", "2026-11-02", "Pendiente", "Ejecutar tests unitarios."),
            Tarea(5, "Publicar repositorio en GitHub", "DevOps", "Media", "2026-11-05", "Pendiente", "Subir commits iniciales y configurar badges.")
        ]

    # -------------------------------------------------------------
    # ESTILOS Y MENÚS
    # -------------------------------------------------------------
    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Helvetica", 9), rowheight=28)
        style.configure("Treeview.Heading", font=("Helvetica", 9, "bold"), background="#E2E8F0")

    def _crear_menus(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nueva Tarea", accelerator="Ctrl+N", command=self._abrir_modal_nueva_tarea)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Exportar a JSON...", command=self._exportar_json)
        menu_archivo.add_command(label="Importar desde JSON...", command=self._importar_json)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", accelerator="Ctrl+Q", command=self.root.quit)

        # Tareas
        menu_tareas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tareas", menu=menu_tareas)
        menu_tareas.add_command(label="Alternar Estado Completada", accelerator="Ctrl+D", command=self._alternar_completada)
        menu_tareas.add_command(label="Editar Seleccionada", command=self._editar_seleccionada)
        menu_tareas.add_command(label="Eliminar Tarea", accelerator="Supr", command=self._eliminar_seleccionada)

        # Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Atajos de Teclado", command=self._mostrar_atajos)
        menu_ayuda.add_command(label="Acerca de TaskFlow", command=self._mostrar_acerca_de)

    def _vincular_atajos(self) -> None:
        self.root.bind("<Control-n>", lambda _: self._abrir_modal_nueva_tarea())
        self.root.bind("<Control-N>", lambda _: self._abrir_modal_nueva_tarea())
        self.root.bind("<Control-d>", lambda _: self._alternar_completada())
        self.root.bind("<Control-D>", lambda _: self._alternar_completada())
        self.root.bind("<Delete>", lambda _: self._eliminar_seleccionada())
        self.root.bind("<Control-q>", lambda _: self.root.quit())

    # -------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------
    def _crear_interfaz(self) -> None:
        # 1. Encabezado principal
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        lbl_tit = tk.Label(header, text="TaskFlow Pro", font=("Helvetica", 16, "bold"), fg="white", bg="#0F172A")
        lbl_tit.pack(side=tk.LEFT)

        lbl_sub = tk.Label(header, text="  |  Gestor de Tareas y Productividad", font=("Helvetica", 10), fg="#94A3B8", bg="#0F172A")
        lbl_sub.pack(side=tk.LEFT, pady=(3, 0))

        btn_nueva = tk.Button(
            header,
            text="+ Nueva Tarea (Ctrl+N)",
            bg="#2563EB",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self._abrir_modal_nueva_tarea
        )
        btn_nueva.pack(side=tk.RIGHT)

        # 2. Panel de métricas y gráfico Canvas
        panel_dashboard = tk.Frame(self.root, bg="#FFFFFF", padx=15, pady=12, relief=tk.SOLID, bd=1)
        panel_dashboard.pack(fill=tk.X, padx=15, pady=10)

        # Tarjetas numéricas
        frame_cards = tk.Frame(panel_dashboard, bg="#FFFFFF")
        frame_cards.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.card_total = self._crear_tarjeta_metrica(frame_cards, "TOTAL TAREAS", "0", "#3B82F6", 0)
        self.card_pendientes = self._crear_tarjeta_metrica(frame_cards, "PENDIENTES", "0", "#F59E0B", 1)
        self.card_en_progreso = self._crear_tarjeta_metrica(frame_cards, "EN PROGRESO", "0", "#8B5CF6", 2)
        self.card_completadas = self._crear_tarjeta_metrica(frame_cards, "COMPLETADAS", "0", "#10B981", 3)

        # Gráfico Canvas circular (Donut chart de progreso)
        self.canvas_progreso = tk.Canvas(panel_dashboard, width=110, height=80, bg="#FFFFFF", highlightthickness=0)
        self.canvas_progreso.pack(side=tk.RIGHT, padx=10)

        # 3. Barra de filtrado y búsqueda
        barra_filtros = tk.Frame(self.root, bg="#F1F5F9", padx=15)
        barra_filtros.pack(fill=tk.X, pady=(0, 8))

        # Pestañas de filtro de estado
        frame_estados = tk.Frame(barra_filtros, bg="#F1F5F9")
        frame_estados.pack(side=tk.LEFT)

        self.btn_filtros = {}
        for est in ["Todas", "Pendiente", "En Progreso", "Completada"]:
            btn = tk.Button(
                frame_estados,
                text=est,
                font=("Helvetica", 9, "bold"),
                relief=tk.FLAT,
                padx=10,
                pady=4,
                bg="#E2E8F0",
                fg="#334155",
                cursor="hand2",
                command=lambda e=est: self._cambiar_filtro_estado(e)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.btn_filtros[est] = btn

        self._actualizar_botones_filtro()

        # Buscador en tiempo real
        frame_busc = tk.Frame(barra_filtros, bg="#F1F5F9")
        frame_busc.pack(side=tk.RIGHT)

        tk.Label(frame_busc, text="🔍", font=("Helvetica", 10), bg="#F1F5F9").pack(side=tk.LEFT, padx=(0, 4))
        self.var_busqueda.trace_add("write", lambda *_: self._actualizar_vista())
        ent_busc = tk.Entry(frame_busc, textvariable=self.var_busqueda, font=("Helvetica", 9), width=24, relief=tk.SOLID, bd=1)
        ent_busc.pack(side=tk.LEFT)

        # 4. Tabla Treeview principal
        frame_tabla = tk.Frame(self.root, padx=15)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        columnas = ("ID", "Titulo", "Categoria", "Prioridad", "FechaLimite", "Estado")

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.tree.yview)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de columnas
        self.tree.heading("ID", text="#")
        self.tree.column("ID", width=45, anchor="center")

        self.tree.heading("Titulo", text="Título de la Tarea")
        self.tree.column("Titulo", width=320, anchor="w")

        self.tree.heading("Categoria", text="Categoría")
        self.tree.column("Categoria", width=120, anchor="center")

        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.column("Prioridad", width=100, anchor="center")

        self.tree.heading("FechaLimite", text="Fecha Límite")
        self.tree.column("FechaLimite", width=110, anchor="center")

        self.tree.heading("Estado", text="Estado")
        self.tree.column("Estado", width=120, anchor="center")

        # Tags de colores por prioridad y estado
        self.tree.tag_configure("alta", foreground="#DC2626")
        self.tree.tag_configure("media", foreground="#D97706")
        self.tree.tag_configure("baja", foreground="#059669")
        self.tree.tag_configure("completada", foreground="#94A3B8")

        # Eventos de tabla
        self.tree.bind("<Double-1>", lambda _: self._editar_seleccionada())

        # Menú contextual de la tabla
        self.menu_tabla = tk.Menu(self.root, tearoff=0)
        self.menu_tabla.add_command(label="Alternar Completada", command=self._alternar_completada)
        self.menu_tabla.add_command(label="Editar Tarea", command=self._editar_seleccionada)
        self.menu_tabla.add_separator()
        self.menu_tabla.add_command(label="Eliminar Tarea", command=self._eliminar_seleccionada)
        self.tree.bind("<Button-3>", self._mostrar_menu_contextual_tabla)
        self.tree.bind("<Button-2>", self._mostrar_menu_contextual_tabla)

        # 5. Barra de estado inferior
        frame_status = tk.Frame(self.root, bg="#CBD5E1", padx=10, pady=5)
        frame_status.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_status = tk.Label(frame_status, text="Listo.", font=("Helvetica", 9), bg="#CBD5E1", fg="#1E293B")
        self.lbl_status.pack(side=tk.LEFT)

        lbl_tips = tk.Label(frame_status, text="Doble clic para editar • Ctrl+D para completar • Supr para borrar", font=("Helvetica", 8), bg="#CBD5E1", fg="#475569")
        lbl_tips.pack(side=tk.RIGHT)

    def _crear_tarjeta_metrica(self, contenedor: tk.Frame, etiqueta: str, valor: str, color_borde: str, col: int) -> dict:
        card = tk.Frame(contenedor, bg="#F8FAFC", relief=tk.SOLID, bd=1, padx=12, pady=6)
        card.grid(row=0, column=col, padx=5, sticky="ew")
        contenedor.columnconfigure(col, weight=1)

        tk.Label(card, text=etiqueta, font=("Helvetica", 7, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w")
        lbl_val = tk.Label(card, text=valor, font=("Helvetica", 16, "bold"), bg="#F8FAFC", fg=color_borde)
        lbl_val.pack(anchor="w")

        return {"label": lbl_val, "frame": card}

    # -------------------------------------------------------------
    # CONTROL DE VISTA Y FILTROS
    # -------------------------------------------------------------
    def _cambiar_filtro_estado(self, estado: str) -> None:
        self.filtro_estado = estado
        self._actualizar_botones_filtro()
        self._actualizar_vista()

    def _actualizar_botones_filtro(self) -> None:
        for est, btn in self.btn_filtros.items():
            if est == self.filtro_estado:
                btn.config(bg="#2563EB", fg="white")
            else:
                btn.config(bg="#E2E8F0", fg="#334155")

    def _actualizar_vista(self) -> None:
        # 1. Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        criterio = self.var_busqueda.get().lower().strip()

        # 2. Filtrar tareas
        tareas_visibles = []
        totales = len(self.tareas)
        pendientes = sum(1 for t in self.tareas if t.estado == "Pendiente")
        en_progreso = sum(1 for t in self.tareas if t.estado == "En Progreso")
        completadas = sum(1 for t in self.tareas if t.estado == "Completada")

        for t in self.tareas:
            # Filtro por pestaña de estado
            if self.filtro_estado != "Todas" and t.estado != self.filtro_estado:
                continue

            # Filtro por texto de búsqueda
            if criterio:
                coincide = (
                    criterio in str(t.id) or
                    criterio in t.titulo.lower() or
                    criterio in t.categoria.lower() or
                    criterio in t.descripcion.lower()
                )
                if not coincide:
                    continue

            tareas_visibles.append(t)

        # 3. Poblar tabla
        for t in tareas_visibles:
            tag = t.prioridad.lower()
            if t.estado == "Completada":
                tag = "completada"

            estado_icono = "✅ " if t.estado == "Completada" else ("⏳ " if t.estado == "En Progreso" else "📌 ")

            self.tree.insert(
                "",
                tk.END,
                iid=str(t.id),
                values=(
                    t.id,
                    t.titulo,
                    t.categoria,
                    t.prioridad,
                    t.fecha_limite or "-",
                    f"{estado_icono}{t.estado}"
                ),
                tags=(tag,)
            )

        # 4. Actualizar métricas numéricas
        self.card_total["label"].config(text=str(totales))
        self.card_pendientes["label"].config(text=str(pendientes))
        self.card_en_progreso["label"].config(text=str(en_progreso))
        self.card_completadas["label"].config(text=str(completadas))

        # 5. Dibujar donut chart en Canvas
        self._dibujar_grafico_progreso(completadas, totales)

        self.lbl_status.config(text=f"Mostrando {len(tareas_visibles)} de {totales} tareas registradas.")

    def _dibujar_grafico_progreso(self, completadas: int, total: int) -> None:
        self.canvas_progreso.delete("all")
        cx, cy, r_ext, r_int = 55, 40, 32, 22

        pct = (completadas / total * 100) if total > 0 else 0
        angulo = (pct / 100) * 359.9

        # Fondo anillo
        self.canvas_progreso.create_oval(cx - r_ext, cy - r_ext, cx + r_ext, cy + r_ext, fill="#E2E8F0", outline="")

        # Sector completado
        if angulo > 0:
            self.canvas_progreso.create_arc(
                cx - r_ext, cy - r_ext, cx + r_ext, cy + r_ext,
                start=90,
                extent=-angulo,
                fill="#10B981",
                outline=""
            )

        # Círculo interior para efecto dona
        self.canvas_progreso.create_oval(cx - r_int, cy - r_int, cx + r_int, cy + r_int, fill="#FFFFFF", outline="")
        self.canvas_progreso.create_text(cx, cy, text=f"{int(pct)}%", font=("Helvetica", 9, "bold"), fill="#1E293B")

    # -------------------------------------------------------------
    # OPERACIONES CRUD Y MODALES
    # -------------------------------------------------------------
    def _abrir_modal_nueva_tarea(self) -> None:
        self._abrir_formulario_tarea(titulo="Nueva Tarea", tarea_existente=None)

    def _editar_seleccionada(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una tarea de la tabla para editar.")
            return

        id_tarea = int(sel[0])
        tarea = next((t for t in self.tareas if t.id == id_tarea), None)
        if tarea:
            self._abrir_formulario_tarea(titulo=f"Editar Tarea #{id_tarea}", tarea_existente=tarea)

    def _abrir_formulario_tarea(self, titulo: str, tarea_existente: Tarea = None) -> None:
        dlg = tk.Toplevel(self.root)
        dlg.title(titulo)
        dlg.geometry("460x440")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        frame = tk.Frame(dlg, padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos
        tk.Label(frame, text="Título de la tarea:*", font=("Helvetica", 9, "bold")).pack(anchor="w")
        ent_titulo = tk.Entry(frame, font=("Helvetica", 10), relief=tk.SOLID, bd=1)
        ent_titulo.pack(fill=tk.X, pady=(2, 10))

        # Categoría y Prioridad
        frame_grid = tk.Frame(frame)
        frame_grid.pack(fill=tk.X, pady=(0, 10))
        frame_grid.columnconfigure(0, weight=1)
        frame_grid.columnconfigure(1, weight=1)

        tk.Label(frame_grid, text="Categoría:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w")
        cbo_cat = ttk.Combobox(frame_grid, values=["Desarrollo", "Diseño", "Documentación", "Calidad", "DevOps", "Personal", "Otro"])
        cbo_cat.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(2, 0))

        tk.Label(frame_grid, text="Prioridad:", font=("Helvetica", 9, "bold")).grid(row=0, column=1, sticky="w")
        cbo_prio = ttk.Combobox(frame_grid, values=["Alta", "Media", "Baja"], state="readonly")
        cbo_prio.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(2, 0))

        # Fecha límite y Estado
        frame_grid2 = tk.Frame(frame)
        frame_grid2.pack(fill=tk.X, pady=(0, 10))
        frame_grid2.columnconfigure(0, weight=1)
        frame_grid2.columnconfigure(1, weight=1)

        tk.Label(frame_grid2, text="Fecha Límite (AAAA-MM-DD):", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w")
        ent_fecha = tk.Entry(frame_grid2, font=("Helvetica", 9), relief=tk.SOLID, bd=1)
        ent_fecha.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(2, 0))

        tk.Label(frame_grid2, text="Estado:", font=("Helvetica", 9, "bold")).grid(row=0, column=1, sticky="w")
        cbo_estado = ttk.Combobox(frame_grid2, values=["Pendiente", "En Progreso", "Completada"], state="readonly")
        cbo_estado.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(2, 0))

        # Descripción
        tk.Label(frame, text="Descripción detallada:", font=("Helvetica", 9, "bold")).pack(anchor="w")
        txt_desc = tk.Text(frame, height=4, font=("Helvetica", 9), relief=tk.SOLID, bd=1)
        txt_desc.pack(fill=tk.BOTH, expand=True, pady=(2, 15))

        # Cargar valores si es edición
        if tarea_existente:
            ent_titulo.insert(0, tarea_existente.titulo)
            cbo_cat.set(tarea_existente.categoria)
            cbo_prio.set(tarea_existente.prioridad)
            ent_fecha.insert(0, tarea_existente.fecha_limite)
            cbo_estado.set(tarea_existente.estado)
            txt_desc.insert(tk.END, tarea_existente.descripcion)
        else:
            cbo_cat.set("Desarrollo")
            cbo_prio.set("Media")
            ent_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
            cbo_estado.set("Pendiente")

        def guardar():
            tit = ent_titulo.get().strip()
            if not tit:
                messagebox.showerror("Error", "El título de la tarea es obligatorio.", parent=dlg)
                return

            cat = cbo_cat.get().strip() or "General"
            prio = cbo_prio.get().strip() or "Media"
            fecha = ent_fecha.get().strip()
            est = cbo_estado.get().strip() or "Pendiente"
            desc = txt_desc.get("1.0", tk.END).strip()

            if tarea_existente:
                tarea_existente.titulo = tit
                tarea_existente.categoria = cat
                tarea_existente.prioridad = prio
                tarea_existente.fecha_limite = fecha
                tarea_existente.estado = est
                tarea_existente.descripcion = desc
            else:
                nuevo_id = max((t.id for t in self.tareas), default=0) + 1
                nueva = Tarea(nuevo_id, tit, cat, prio, fecha, est, desc)
                self.tareas.append(nueva)

            self._guardar_tareas_disco()
            self._actualizar_vista()
            dlg.destroy()

        # Botón Guardar
        btn_g = tk.Button(frame, text="Guardar Tarea", bg="#2563EB", fg="white", font=("Helvetica", 9, "bold"), relief=tk.FLAT, pady=6, command=guardar)
        btn_g.pack(fill=tk.X)

    def _eliminar_seleccionada(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar.")
            return

        id_tarea = int(sel[0])
        tarea = next((t for t in self.tareas if t.id == id_tarea), None)
        if not tarea:
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar la tarea '{tarea.titulo}'?")
        if confirm:
            self.tareas = [t for t in self.tareas if t.id != id_tarea]
            self._guardar_tareas_disco()
            self._actualizar_vista()

    def _alternar_completada(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return

        id_tarea = int(sel[0])
        tarea = next((t for t in self.tareas if t.id == id_tarea), None)
        if tarea:
            tarea.estado = "Pendiente" if tarea.estado == "Completada" else "Completada"
            self._guardar_tareas_disco()
            self._actualizar_vista()

    def _mostrar_menu_contextual_tabla(self, evento: tk.Event) -> None:
        item = self.tree.identify_row(evento.y)
        if item:
            self.tree.selection_set(item)
            self.menu_tabla.tk_popup(evento.x_root, evento.y_root)

    # -------------------------------------------------------------
    # IMPORTAR / EXPORTAR
    # -------------------------------------------------------------
    def _exportar_json(self) -> None:
        ruta = filedialog.asksaveasfilename(
            title="Exportar Tareas a JSON",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if ruta:
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump([t.to_dict() for t in self.tareas], f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Exportación Exitosa", f"Tareas exportadas correctamente a:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al exportar: {e}")

    def _importar_json(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Importar Tareas desde JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    nuevas = [Tarea.from_dict(item) for item in datos]
                    self.tareas = nuevas
                    self._guardar_tareas_disco()
                    self._actualizar_vista()
                messagebox.showinfo("Importación Exitosa", f"Se importaron {len(nuevas)} tareas con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al importar archivo: {e}")

    def _mostrar_atajos(self) -> None:
        mensaje = (
            "Atajos de Teclado Globales:\n\n"
            "• Ctrl + N : Crear una nueva tarea\n"
            "• Ctrl + D : Alternar estado (Pendiente <-> Completada)\n"
            "• Supr     : Eliminar la tarea seleccionada\n"
            "• Ctrl + Q : Salir de la aplicación\n"
            "• Doble Clic : Editar los datos de la fila"
        )
        messagebox.showinfo("Atajos de Teclado", mensaje)

    def _mostrar_acerca_de(self) -> None:
        messagebox.showinfo("Acerca de TaskFlow Pro", "TaskFlow Pro v1.0\nProyecto Integrador de Tkinter\nDesarrollado en Python puro.")


def main():
    root = tk.Tk()
    app = GestorTareasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
