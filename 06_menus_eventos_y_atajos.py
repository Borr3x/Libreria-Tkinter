"""
06_menus_eventos_y_atajos.py
============================
Sistemas de menús, bindings de eventos y atajos de teclado en Tkinter:
- Barra de menú superior (tk.Menu) con cascadas (Archivo, Edición, Opciones, Ayuda).
- Separadores, aceleradores visuales y elementos de tipo Checkbutton / Radiobutton en menús.
- Menú contextual emergente (clic derecho / popup menu).
- Vinculación de eventos con .bind():
  * Atajos de teclado: <Control-n>, <Control-s>, <Control-q>, <Escape>.
  * Eventos de ratón: <Button-3>, <Enter>, <Leave>, <Motion>.
- Barra de estado (status bar) interactiva con feedback en tiempo real.
"""

import tkinter as tk
from tkinter import messagebox, ttk


class MenusYEventosApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("06 - Menús, Context Menu, Atajos y Eventos")
        self.root.geometry("820x580")
        self.root.minsize(700, 480)
        self.root.configure(bg="#F8FAFC")

        # Variables para elementos de menú
        self.var_modo_oscuro = tk.BooleanVar(value=False)
        self.var_nivel_zoom = tk.StringVar(value="100%")
        self.var_estado = tk.StringVar(value="Listo. Presiona atajos como Ctrl+S o haz clic derecho.")

        self._crear_barra_menus()
        self._crear_interfaz()
        self._crear_menu_contextual()
        self._vincular_atajos()

    def _crear_barra_menus(self) -> None:
        """Crea la barra de menú superior con cascadas y aceleradores."""
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        # 1. Menú Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_archivo.add_command(label="Nuevo", accelerator="Ctrl+N", command=self._accion_nuevo)
        menu_archivo.add_command(label="Abrir...", accelerator="Ctrl+O", command=self._accion_abrir)
        menu_archivo.add_command(label="Guardar", accelerator="Ctrl+S", command=self._accion_guardar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", accelerator="Ctrl+Q", command=self.root.quit)

        # 2. Menú Edición
        menu_edicion = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Edición", menu=menu_edicion)

        menu_edicion.add_command(label="Deshacer", accelerator="Ctrl+Z", command=lambda: self._set_estado("Acción: Deshacer"))
        menu_edicion.add_command(label="Rehacer", accelerator="Ctrl+Y", command=lambda: self._set_estado("Acción: Rehacer"))
        menu_edicion.add_separator()
        menu_edicion.add_command(label="Cortar", accelerator="Ctrl+X", command=lambda: self.txt_area.event_generate("<<Cut>>"))
        menu_edicion.add_command(label="Copiar", accelerator="Ctrl+C", command=lambda: self.txt_area.event_generate("<<Copy>>"))
        menu_edicion.add_command(label="Pegar", accelerator="Ctrl+V", command=lambda: self.txt_area.event_generate("<<Paste>>"))

        # 3. Menú Ver con Checkbuttons y Radiobuttons
        menu_ver = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ver", menu=menu_ver)

        menu_ver.add_checkbutton(
            label="Modo Oscuro en Editor",
            variable=self.var_modo_oscuro,
            command=self._alternar_modo_oscuro
        )
        menu_ver.add_separator()

        # Opciones exclusivas de Zoom
        menu_ver.add_command(label="Nivel de Zoom:", state="disabled")
        for zoom in ["75%", "100%", "125%", "150%"]:
            menu_ver.add_radiobutton(
                label=f"  {zoom}",
                value=zoom,
                variable=self.var_nivel_zoom,
                command=self._cambiar_zoom
            )

        # 4. Menú Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Atajos de Teclado", command=self._mostrar_atajos)
        menu_ayuda.add_command(label="Acerca de...", command=self._mostrar_acerca_de)

    def _crear_menu_contextual(self) -> None:
        """Crea el menú emergente (popup) que se abre con clic derecho."""
        self.menu_contextual = tk.Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(label="📋 Copiar Selección", command=lambda: self.txt_area.event_generate("<<Copy>>"))
        self.menu_contextual.add_command(label="📌 Pegar Contenido", command=lambda: self.txt_area.event_generate("<<Paste>>"))
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="✨ Limpiar Editor", command=self._limpiar_editor)
        self.menu_contextual.add_command(label="💾 Guardar Cambios (Ctrl+S)", command=self._accion_guardar)

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#1E293B", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Barra de Menús, Menú Contextual y Eventos",
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Usa los menús de arriba, los atajos Ctrl+N/Ctrl+S/Ctrl+Q o haz clic derecho en el editor.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w", pady=(2, 0))

        # Panel central
        contenedor = tk.Frame(self.root, bg="#F8FAFC", padx=15, pady=15)
        contenedor.pack(fill=tk.BOTH, expand=True)

        # Zona de captura de ratón (hover box)
        self.box_hover = tk.Label(
            contenedor,
            text="Área de Detección de Ratón (<Enter>, <Leave>, <Motion>)\nPasa el cursor por aquí para ver las coordenadas en tiempo real.",
            font=("Helvetica", 9, "bold"),
            bg="#E2E8F0",
            fg="#334155",
            relief=tk.DASHED,
            bd=2,
            pady=15
        )
        self.box_hover.pack(fill=tk.X, pady=(0, 10))

        # Eventos del cursor en la caja
        self.box_hover.bind("<Enter>", lambda _: self.box_hover.config(bg="#DBEAFE", fg="#1D4ED8"))
        self.box_hover.bind("<Leave>", lambda _: self.box_hover.config(bg="#E2E8F0", fg="#334155"))
        self.box_hover.bind("<Motion>", self._rastrear_coordenadas)

        # Editor de texto interactivo
        lbl_ed = tk.Label(contenedor, text="Área de Texto con Menú Contextual (Clic Derecho):", font=("Helvetica", 10, "bold"), bg="#F8FAFC", fg="#1E293B")
        lbl_ed.pack(anchor="w", pady=(5, 3))

        self.txt_area = tk.Text(contenedor, font=("Helvetica", 11), relief=tk.SOLID, bd=1, padx=10, pady=10)
        self.txt_area.pack(fill=tk.BOTH, expand=True)
        self.txt_area.insert(
            tk.END,
            "¡Haz clic derecho sobre este texto para desplegar el menú contextual!\n\n"
            "Atajos soportados en esta ventana:\n"
            "  • Ctrl + N : Crear nuevo archivo simulado.\n"
            "  • Ctrl + S : Guardar contenido del editor.\n"
            "  • Ctrl + O : Simular apertura de archivo.\n"
            "  • Ctrl + Q : Cerrar la ventana.\n"
        )

        # Vincular clic derecho en el editor (Button-3 en Windows/Linux, Button-2 en macOS)
        self.txt_area.bind("<Button-3>", self._mostrar_menu_contextual)
        self.txt_area.bind("<Button-2>", self._mostrar_menu_contextual)

        # Barra de estado inferior
        frame_status = tk.Frame(self.root, bg="#CBD5E1", padx=10, pady=6)
        frame_status.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_status = tk.Label(frame_status, textvariable=self.var_estado, font=("Helvetica", 9), bg="#CBD5E1", fg="#1E293B")
        self.lbl_status.pack(side=tk.LEFT)

        self.lbl_coords = tk.Label(frame_status, text="X: 0 | Y: 0", font=("Consolas", 9), bg="#CBD5E1", fg="#475569")
        self.lbl_coords.pack(side=tk.RIGHT)

    def _vincular_atajos(self) -> None:
        """Asocia combinaciones de teclado a métodos específicos."""
        self.root.bind("<Control-n>", lambda _: self._accion_nuevo())
        self.root.bind("<Control-N>", lambda _: self._accion_nuevo())
        self.root.bind("<Control-s>", lambda _: self._accion_guardar())
        self.root.bind("<Control-S>", lambda _: self._accion_guardar())
        self.root.bind("<Control-o>", lambda _: self._accion_abrir())
        self.root.bind("<Control-O>", lambda _: self._accion_abrir())
        self.root.bind("<Control-q>", lambda _: self.root.quit())
        self.root.bind("<Control-Q>", lambda _: self.root.quit())

    def _mostrar_menu_contextual(self, evento: tk.Event) -> None:
        self.menu_contextual.tk_popup(evento.x_root, evento.y_root)

    def _rastrear_coordenadas(self, evento: tk.Event) -> None:
        self.lbl_coords.config(text=f"Cursor: X={evento.x:03d} | Y={evento.y:03d}")

    def _set_estado(self, texto: str) -> None:
        self.var_estado.set(texto)

    def _accion_nuevo(self) -> None:
        self.txt_area.delete("1.0", tk.END)
        self._set_estado("Nuevo documento creado (Ctrl+N)")

    def _accion_abrir(self) -> None:
        self._set_estado("Comando Abrir ejecutado (Ctrl+O)")
        messagebox.showinfo("Abrir", "Simulación: Seleccionando archivo...")

    def _accion_guardar(self) -> None:
        contenido = self.txt_area.get("1.0", tk.END).strip()
        self._set_estado(f"Documento guardado con éxito ({len(contenido)} caracteres)")
        messagebox.showinfo("Guardar", "¡El contenido ha sido guardado exitosamente!")

    def _limpiar_editor(self) -> None:
        self.txt_area.delete("1.0", tk.END)
        self._set_estado("Editor vaciado.")

    def _alternar_modo_oscuro(self) -> None:
        if self.var_modo_oscuro.get():
            self.txt_area.config(bg="#1E293B", fg="#F8FAFC", insertbackground="white")
            self._set_estado("Modo Oscuro activado.")
        else:
            self.txt_area.config(bg="#FFFFFF", fg="#000000", insertbackground="black")
            self._set_estado("Modo Claro activado.")

    def _cambiar_zoom(self) -> None:
        zoom_str = self.var_nivel_zoom.get().replace("%", "")
        tamano_base = int(11 * (int(zoom_str) / 100))
        self.txt_area.config(font=("Helvetica", tamano_base))
        self._set_estado(f"Nivel de zoom ajustado al {self.var_nivel_zoom.get()}")

    def _mostrar_atajos(self) -> None:
        mensaje = (
            "Atajos disponibles:\n\n"
            "• Ctrl + N : Nuevo documento\n"
            "• Ctrl + O : Abrir documento\n"
            "• Ctrl + S : Guardar documento\n"
            "• Ctrl + Q : Salir\n"
            "• Clic Derecho : Menú contextual"
        )
        messagebox.showinfo("Atajos de Teclado", mensaje)

    def _mostrar_acerca_de(self) -> None:
        messagebox.showinfo("Acerca de", "Demostración de Menús y Eventos en Tkinter\nVersión 1.0")


def main():
    root = tk.Tk()
    app = MenusYEventosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
