"""
07_estilos_modernos_ttk.py
==========================
Personalización visual y uso avanzado del subsistema ttk (Themed Tkinter):
- Comparación visual entre widgets clásicos (tk) y widgets temáticos modernos (ttk).
- Explorador y selector de temas nativos e integrados ('clam', 'alt', 'default', 'classic').
- Creación de estilos personalizados con ttk.Style() (.configure(), .map()).
- Componentes ttk específicos:
  * ttk.Notebook (Pestañas).
  * ttk.Progressbar (Modo determinado e indeterminado).
  * ttk.Separator (Divisores visuales).
  * ttk.Sizegrip (Control de cambio de tamaño).
"""

import tkinter as tk
from tkinter import ttk


class EstilosModernosApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("07 - Estilos Modernos y Temas ttk (ttk.Style)")
        self.root.geometry("860x650")
        self.root.minsize(750, 550)
        self.root.configure(bg="#F1F5F9")

        self.style = ttk.Style()
        self.temas_disponibles = sorted(self.style.theme_names())
        self.tema_actual = tk.StringVar(value=self.style.theme_use())

        # Configuración de variables de progreso
        self.var_progreso = tk.DoubleVar(value=35.0)
        self.indeterminado_activo = False

        self._configurar_estilos_personalizados()
        self._crear_interfaz()

    def _configurar_estilos_personalizados(self) -> None:
        """Crea clases de estilo personalizadas con colores, padding y estados dinámicos."""
        # Botón primario azul
        self.style.configure(
            "Primary.TButton",
            font=("Helvetica", 10, "bold"),
            padding=8,
            relief="flat"
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("!disabled", "#2563EB")],
            foreground=[("!disabled", "white")]
        )

        # Botón de éxito verde
        self.style.configure(
            "Success.TButton",
            font=("Helvetica", 10, "bold"),
            padding=8,
            relief="flat"
        )
        self.style.map(
            "Success.TButton",
            background=[("active", "#059669"), ("!disabled", "#10B981")],
            foreground=[("!disabled", "white")]
        )

        # Botón de peligro rojo
        self.style.configure(
            "Danger.TButton",
            font=("Helvetica", 10, "bold"),
            padding=8,
            relief="flat"
        )
        self.style.map(
            "Danger.TButton",
            background=[("active", "#DC2626"), ("!disabled", "#EF4444")],
            foreground=[("!disabled", "white")]
        )

        # Tarjetas de etiqueta ttk
        self.style.configure(
            "Card.TLabelframe",
            background="#FFFFFF",
            relief="groove",
            borderwidth=1
        )
        self.style.configure(
            "Card.TLabelframe.Label",
            font=("Helvetica", 10, "bold"),
            foreground="#1E293B",
            background="#FFFFFF"
        )

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Subsistema ttk y Motor de Estilos",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Compara temas globales del sistema y diseña estilos con ttk.Style().configure() y .map().",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w", pady=(2, 0))

        # Barra de selección de temas
        barra_tema = tk.Frame(self.root, bg="#E2E8F0", padx=15, pady=10)
        barra_tema.pack(fill=tk.X)

        tk.Label(barra_tema, text="Tema ttk Activo:", font=("Helvetica", 10, "bold"), bg="#E2E8F0").pack(side=tk.LEFT, padx=(0, 10))

        cbo_temas = ttk.Combobox(
            barra_tema,
            textvariable=self.tema_actual,
            values=self.temas_disponibles,
            state="readonly",
            font=("Helvetica", 9)
        )
        cbo_temas.pack(side=tk.LEFT, padx=(0, 10))
        cbo_temas.bind("<<ComboboxSelected>>", self._cambiar_tema)

        self.lbl_info_tema = tk.Label(
            barra_tema,
            text=f"Temas detectados en tu sistema: {', '.join(self.temas_disponibles)}",
            font=("Helvetica", 8, "italic"),
            bg="#E2E8F0",
            fg="#475569"
        )
        self.lbl_info_tema.pack(side=tk.LEFT, padx=10)

        # Contenedor central con Notebook
        cuaderno = ttk.Notebook(self.root)
        cuaderno.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tab_estilos = ttk.Frame(cuaderno, padding=15)
        tab_barras = ttk.Frame(cuaderno, padding=15)
        tab_comparativa = ttk.Frame(cuaderno, padding=15)

        cuaderno.add(tab_estilos, text="  Estilos Personalizados  ")
        cuaderno.add(tab_barras, text="  Barras de Progreso  ")
        cuaderno.add(tab_comparativa, text="  Clásicos vs ttk  ")

        self._construir_tab_estilos(tab_estilos)
        self._construir_tab_barras(tab_barras)
        self._construir_tab_comparativa(tab_comparativa)

        # Control de agarre de tamaño en la esquina inferior
        ttk.Sizegrip(self.root).pack(side=tk.RIGHT, anchor=tk.SE)

    def _construir_tab_estilos(self, contenedor: ttk.Frame) -> None:
        lbl_info = ttk.Label(
            contenedor,
            text="Los botones a continuación usan clases de estilo personalizadas (Primary.TButton, Success.TButton, Danger.TButton)\n"
                 "con estados pseudo-clases dinámicos ('active', '!disabled') aplicados mediante style.map().",
            wraplength=700
        )
        lbl_info.pack(fill=tk.X, pady=(0, 15))

        # Panel de botones estilizados
        frame_btns = ttk.LabelFrame(contenedor, text=" Botones con Estilos Custom ", padding=15)
        frame_btns.pack(fill=tk.X, pady=(0, 15))

        btn_pri = ttk.Button(frame_btns, text="Botón Primario", style="Primary.TButton")
        btn_pri.pack(side=tk.LEFT, padx=10)

        btn_suc = ttk.Button(frame_btns, text="Botón Éxito", style="Success.TButton")
        btn_suc.pack(side=tk.LEFT, padx=10)

        btn_dan = ttk.Button(frame_btns, text="Botón Peligro", style="Danger.TButton")
        btn_dan.pack(side=tk.LEFT, padx=10)

        btn_dis = ttk.Button(frame_btns, text="Botón Deshabilitado", style="Primary.TButton", state="disabled")
        btn_dis.pack(side=tk.LEFT, padx=10)

        # Divisor ttk.Separator
        ttk.Separator(contenedor, orient="horizontal").pack(fill=tk.X, pady=15)

        # Tarjetas de información
        frame_card = ttk.LabelFrame(contenedor, text=" Componente ttk.LabelFrame Estilizado ", padding=15)
        frame_card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame_card,
            text="Ventajas clave de ttk:\n\n"
                 "1. Integración con el aspecto nativo del sistema operativo (Windows, macOS o Linux).\n"
                 "2. Separación limpia entre el código funcional y el aspecto estético (equivalente a CSS para Tkinter).\n"
                 "3. Soporte para estados avanzados como hover (active), focus, disabled y pressed mediante .map().\n"
                 "4. Nuevos widgets inexistentes en el tk clásico (Notebook, Treeview, Combobox, Progressbar).",
            font=("Helvetica", 9),
            justify=tk.LEFT
        ).pack(anchor="w")

    def _construir_tab_barras(self, contenedor: ttk.Frame) -> None:
        # Barra Determinada
        frame_det = ttk.LabelFrame(contenedor, text=" 1. Barra de Progreso Determinada ", padding=15)
        frame_det.pack(fill=tk.X, pady=(0, 15))

        self.prog_det = ttk.Progressbar(
            frame_det,
            orient="horizontal",
            mode="determinate",
            variable=self.var_progreso,
            maximum=100
        )
        self.prog_det.pack(fill=tk.X, pady=(0, 10))

        frame_ctrl_det = ttk.Frame(frame_det)
        frame_ctrl_det.pack(fill=tk.X)

        ttk.Button(frame_ctrl_det, text="- 10%", command=lambda: self._ajustar_progreso(-10)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ctrl_det, text="+ 10%", command=lambda: self._ajustar_progreso(10)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ctrl_det, text="Reiniciar a 0%", command=lambda: self.var_progreso.set(0)).pack(side=tk.LEFT, padx=5)

        self.lbl_pct = ttk.Label(frame_ctrl_det, text="Progreso: 35.0%")
        self.lbl_pct.pack(side=tk.RIGHT, padx=10)

        # Barra Indeterminada (Carga infinita / Spinner)
        frame_indet = ttk.LabelFrame(contenedor, text=" 2. Barra de Progreso Indeterminada (Carga o Espera) ", padding=15)
        frame_indet.pack(fill=tk.X)

        self.prog_indet = ttk.Progressbar(frame_indet, orient="horizontal", mode="indeterminate", length=300)
        self.prog_indet.pack(fill=tk.X, pady=(0, 10))

        self.btn_indet = ttk.Button(frame_indet, text="▶ Iniciar Movimiento Indeterminado", command=self._alternar_indeterminado)
        self.btn_indet.pack(side=tk.LEFT)

    def _construir_tab_comparativa(self, contenedor: ttk.Frame) -> None:
        lbl_desc = ttk.Label(
            contenedor,
            text="Observa la diferencia entre los widgets clásicos del módulo 'tk' original (izquierda)\n"
                 "y los widgets temáticos del módulo 'ttk' (derecha) bajo el tema actual.",
            justify=tk.LEFT
        )
        lbl_desc.pack(fill=tk.X, pady=(0, 15))

        frame_comp = ttk.Frame(contenedor)
        frame_comp.pack(fill=tk.BOTH, expand=True)
        frame_comp.columnconfigure(0, weight=1)
        frame_comp.columnconfigure(1, weight=1)

        # Clásico
        panel_clasico = tk.LabelFrame(frame_comp, text=" tk Clásico (tkinter.*) ", padx=15, pady=15, bg="#F3F4F6")
        panel_clasico.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(panel_clasico, text="tk.Button clásico:", bg="#F3F4F6").pack(anchor="w")
        tk.Button(panel_clasico, text="Botón Clásico").pack(fill=tk.X, pady=(2, 10))

        tk.Label(panel_clasico, text="tk.Entry clásico:", bg="#F3F4F6").pack(anchor="w")
        tk.Entry(panel_clasico).pack(fill=tk.X, pady=(2, 10))

        tk.Label(panel_clasico, text="tk.Checkbutton clásico:", bg="#F3F4F6").pack(anchor="w")
        tk.Checkbutton(panel_clasico, text="Opción clásica", bg="#F3F4F6").pack(anchor="w")

        # Moderno ttk
        panel_ttk = ttk.LabelFrame(frame_comp, text=" Moderno ttk (tkinter.ttk.*) ", padding=15)
        panel_ttk.grid(row=0, column=1, sticky="nsew")

        ttk.Label(panel_ttk, text="ttk.Button moderno:").pack(anchor="w")
        ttk.Button(panel_ttk, text="Botón ttk").pack(fill=tk.X, pady=(2, 10))

        ttk.Label(panel_ttk, text="ttk.Entry moderno:").pack(anchor="w")
        ttk.Entry(panel_ttk).pack(fill=tk.X, pady=(2, 10))

        ttk.Label(panel_ttk, text="ttk.Checkbutton moderno:").pack(anchor="w")
        ttk.Checkbutton(panel_ttk, text="Opción ttk").pack(anchor="w")

    def _cambiar_tema(self, _evento=None) -> None:
        nuevo_tema = self.tema_actual.get()
        self.style.theme_use(nuevo_tema)
        # Re-aplicar configuraciones personalizadas para el nuevo tema
        self._configurar_estilos_personalizados()

    def _ajustar_progreso(self, delta: float) -> None:
        actual = self.var_progreso.get()
        nuevo = max(0.0, min(100.0, actual + delta))
        self.var_progreso.set(nuevo)
        self.lbl_pct.config(text=f"Progreso: {nuevo:.1f}%")

    def _alternar_indeterminado(self) -> None:
        self.indeterminado_activo = not self.indeterminado_activo
        if self.indeterminado_activo:
            self.prog_indet.start(15)  # Avanza cada 15ms
            self.btn_indet.config(text="⏹ Detener Movimiento")
        else:
            self.prog_indet.stop()
            self.btn_indet.config(text="▶ Iniciar Movimiento Indeterminado")


def main():
    root = tk.Tk()
    app = EstilosModernosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
