"""
05_dialogos_ventanas_secundarias.py
===================================
Gestión de ventanas secundarias y diálogos nativos del sistema en Tkinter:
- Ventanas hijas con tk.Toplevel (modales y no modales, grab_set(), transient()).
- Alertas y confirmaciones con tkinter.messagebox (showinfo, showwarning, showerror, askyesno, etc.).
- Explorador del sistema de archivos con tkinter.filedialog (abrir, guardar, seleccionar carpeta).
- Selector de paleta de colores con tkinter.colorchooser.askcolor.
- Entradas de diálogo directas con tkinter.simpledialog (askstring, askinteger, askfloat).
- Comunicación bidireccional y retorno de datos entre ventanas.
"""

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk


class VentanaModalPersonalizada(tk.Toplevel):
    """Ventana emergente modal creada con Toplevel."""
    def __init__(self, parent: tk.Tk, titulo: str, mensaje: str, callback_resultado):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("420x240")
        self.resizable(False, False)
        self.configure(bg="#F8FAFC")
        self.callback_resultado = callback_resultado

        # Configuración modal: bloquea interacción con la ventana padre
        self.transient(parent)   # Asocia visualmente la ventana con el padre
        self.grab_set()          # Redirige todos los eventos a esta ventana

        # Contenido
        tk.Label(
            self,
            text="⭐ Ventana Secundaria Modal (Toplevel)",
            font=("Helvetica", 12, "bold"),
            bg="#1E293B",
            fg="white",
            pady=10
        ).pack(fill=tk.X)

        tk.Label(
            self,
            text=mensaje,
            font=("Helvetica", 10),
            bg="#F8FAFC",
            fg="#334155",
            wraplength=380,
            pady=15
        ).pack()

        tk.Label(self, text="Escribe una respuesta para enviar a la ventana padre:", font=("Helvetica", 9, "bold"), bg="#F8FAFC").pack()
        self.entry_resp = tk.Entry(self, font=("Helvetica", 10), width=35, relief=tk.SOLID, bd=1)
        self.entry_resp.pack(pady=5)
        self.entry_resp.focus()

        # Botones
        frame_btns = tk.Frame(self, bg="#F8FAFC")
        frame_btns.pack(pady=10)

        tk.Button(
            frame_btns,
            text="Cancelar",
            bg="#94A3B8",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_btns,
            text="Confirmar y Retornar",
            bg="#2563EB",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._confirmar
        ).pack(side=tk.LEFT, padx=5)

    def _confirmar(self) -> None:
        texto = self.entry_resp.get().strip()
        self.callback_resultado(texto)
        self.destroy()


class DialogosApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("05 - Diálogos, Mensajes y Ventanas Secundarias")
        self.root.geometry("860x650")
        self.root.minsize(760, 550)
        self.root.configure(bg="#F1F5F9")

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Diálogos Nativos y Ventanas Modales",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Aprende a integrar alertas messagebox, diálogos de archivo filedialog, colorchooser y Toplevel personalizadas.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w", pady=(2, 0))

        # Contenedor dividido en dos columnas: Izquierda (Botones de prueba), Derecha (Log de resultados)
        cuerpo = tk.Frame(self.root, bg="#F1F5F9", padx=15, pady=15)
        cuerpo.pack(fill=tk.BOTH, expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        # Columna Izquierda: Acciones
        col_acciones = tk.Frame(cuerpo, bg="#F1F5F9")
        col_acciones.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 1. Grupo Messagebox
        grp_msg = tk.LabelFrame(col_acciones, text=" 1. tkinter.messagebox ", font=("Helvetica", 10, "bold"), bg="white", padx=10, pady=10)
        grp_msg.pack(fill=tk.X, pady=(0, 10))

        frame_msg_btns = tk.Frame(grp_msg, bg="white")
        frame_msg_btns.pack(fill=tk.X)

        tk.Button(frame_msg_btns, text="ℹ️ showinfo", bg="#3B82F6", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_showinfo).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_msg_btns, text="⚠️ showwarning", bg="#F59E0B", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_showwarning).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_msg_btns, text="❌ showerror", bg="#EF4444", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_showerror).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_msg_btns, text="❓ askyesno", bg="#8B5CF6", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_askyesno).pack(side=tk.LEFT, padx=3)

        # 2. Grupo FileDialog
        grp_file = tk.LabelFrame(col_acciones, text=" 2. tkinter.filedialog ", font=("Helvetica", 10, "bold"), bg="white", padx=10, pady=10)
        grp_file.pack(fill=tk.X, pady=(0, 10))

        frame_file_btns = tk.Frame(grp_file, bg="white")
        frame_file_btns.pack(fill=tk.X)

        tk.Button(frame_file_btns, text="📂 Abrir Archivo", bg="#0284C7", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_abrir_archivo).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_file_btns, text="💾 Guardar Como...", bg="#059669", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_guardar_archivo).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_file_btns, text="📁 Seleccionar Carpeta", bg="#D97706", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_abrir_carpeta).pack(side=tk.LEFT, padx=3)

        # 3. Grupo ColorChooser y SimpleDialog
        grp_inputs = tk.LabelFrame(col_acciones, text=" 3. colorchooser & simpledialog ", font=("Helvetica", 10, "bold"), bg="white", padx=10, pady=10)
        grp_inputs.pack(fill=tk.X, pady=(0, 10))

        frame_input_btns = tk.Frame(grp_inputs, bg="white")
        frame_input_btns.pack(fill=tk.X)

        tk.Button(frame_input_btns, text="🎨 Elegir Color", bg="#EC4899", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_color).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_input_btns, text="✏️ askstring", bg="#475569", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_askstring).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_input_btns, text="🔢 askinteger", bg="#475569", fg="white", relief=tk.FLAT, padx=8, pady=4, command=self._demo_askinteger).pack(side=tk.LEFT, padx=3)

        # 4. Grupo Ventana Toplevel Personalizada
        grp_toplevel = tk.LabelFrame(col_acciones, text=" 4. Ventana Modal Personalizada (tk.Toplevel) ", font=("Helvetica", 10, "bold"), bg="white", padx=10, pady=10)
        grp_toplevel.pack(fill=tk.X)

        tk.Button(
            grp_toplevel,
            text="🚀 Abrir Ventana Modal Interactiva",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=8,
            command=self._demo_toplevel_modal
        ).pack(fill=tk.X)

        # Columna Derecha: Bitácora de Resultados en vivo
        col_log = tk.LabelFrame(cuerpo, text=" Registro de Eventos y Respuestas ", font=("Helvetica", 10, "bold"), bg="#1E293B", fg="#38BDF8", padx=10, pady=10)
        col_log.grid(row=0, column=1, sticky="nsew")

        self.txt_log = tk.Text(col_log, bg="#0F172A", fg="#E2E8F0", font=("Consolas", 9), relief=tk.FLAT, padx=8, pady=8)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        btn_limpiar_log = tk.Button(col_log, text="Limpiar Registro", bg="#334155", fg="white", relief=tk.FLAT, pady=4, command=self._limpiar_log)
        btn_limpiar_log.pack(fill=tk.X, pady=(6, 0))

        self._agregar_log("Sistema inicializado. Haz clic en cualquier botón de la izquierda para probar diálogos.")

    def _agregar_log(self, mensaje: str) -> None:
        self.txt_log.insert(tk.END, f"• {mensaje}\n")
        self.txt_log.see(tk.END)

    def _limpiar_log(self) -> None:
        self.txt_log.delete("1.0", tk.END)

    # Handlers
    def _demo_showinfo(self) -> None:
        messagebox.showinfo("Operación Exitosa", "Tu archivo ha sido procesado de forma correcta.")
        self._agregar_log("messagebox.showinfo ejecutado con éxito.")

    def _demo_showwarning(self) -> None:
        messagebox.showwarning("Advertencia de Sistema", "El disco duro tiene poco espacio disponible.")
        self._agregar_log("messagebox.showwarning mostrado al usuario.")

    def _demo_showerror(self) -> None:
        messagebox.showerror("Fallo Crítico", "No se pudo conectar a la base de datos remota.")
        self._agregar_log("messagebox.showerror notificado.")

    def _demo_askyesno(self) -> None:
        resp = messagebox.askyesno("Confirmación Requerida", "¿Deseas formatear la unidad temporal?")
        self._agregar_log(f"messagebox.askyesno respuesta: {resp} ({'Sí' if resp else 'No'})")

    def _demo_abrir_archivo(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo para abrir",
            filetypes=[("Archivos de texto", "*.txt"), ("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self._agregar_log(f"Archivo seleccionado: {ruta}")
        else:
            self._agregar_log("Diálogo de apertura cancelado por el usuario.")

    def _demo_guardar_archivo(self) -> None:
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Archivo JSON", "*.json")]
        )
        if ruta:
            self._agregar_log(f"Ruta de guardado especificada: {ruta}")
        else:
            self._agregar_log("Guardado cancelado.")

    def _demo_abrir_carpeta(self) -> None:
        carpeta = filedialog.askdirectory(title="Seleccionar directorio de trabajo")
        if carpeta:
            self._agregar_log(f"Directorio seleccionado: {carpeta}")
        else:
            self._agregar_log("Selección de directorio cancelada.")

    def _demo_color(self) -> None:
        color = colorchooser.askcolor(title="Seleccionar color de fondo", initialcolor="#3B82F6")
        if color and color[1]:
            hex_color = color[1]
            self._agregar_log(f"Color elegido: {hex_color} (RGB: {color[0]})")
        else:
            self._agregar_log("Selección de color cancelada.")

    def _demo_askstring(self) -> None:
        texto = simpledialog.askstring("Nombre de Proyecto", "¿Cuál es el nombre de tu proyecto?")
        self._agregar_log(f"simpledialog.askstring ingresado: {texto}")

    def _demo_askinteger(self) -> None:
        numero = simpledialog.askinteger("Configurar Puerto", "Ingresa el número de puerto (1-65535):", minvalue=1, maxvalue=65535)
        self._agregar_log(f"simpledialog.askinteger ingresado: {numero}")

    def _demo_toplevel_modal(self) -> None:
        def recibir_datos(resultado: str):
            self._agregar_log(f"Datos recibidos desde Toplevel modal: '{resultado}'")

        VentanaModalPersonalizada(
            parent=self.root,
            titulo="Diálogo Personalizado",
            mensaje="Esta ventana modal bloquea la ventana principal hasta cerrarse (grab_set).",
            callback_resultado=recibir_datos
        )


def main():
    root = tk.Tk()
    app = DialogosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
