"""
01_fundamentos_y_conceptos_basicos.py
====================================
Demostración de los conceptos esenciales y ciclo de vida básico en Tkinter:
- Inicialización de la ventana principal (tk.Tk).
- Configuración de propiedades: título, dimensiones, tamaño mínimo/máximo, redimensionabilidad y centrado.
- Creación y colocación de widgets básicos: Label, Button y Entry.
- Variables de control reactivas: StringVar, IntVar.
- Modificación dinámica de propiedades de widgets (método .config()).
- Manejo de eventos de clic y el ciclo principal de eventos (mainloop).
"""

import tkinter as tk
from tkinter import ttk


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    """Calcula y aplica la posición requerida para centrar la ventana en la pantalla."""
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho - ancho) // 2
    pos_y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


class VentanaFundamentos:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("01 - Fundamentos y Conceptos Básicos de Tkinter")
        
        # Dimensiones y límites de la ventana
        ancho, alto = 550, 480
        centrar_ventana(self.root, ancho, alto)
        self.root.minsize(450, 400)
        self.root.resizable(True, True)
        self.root.configure(bg="#F3F4F6")

        # Variables de control reactivas
        self.var_nombre = tk.StringVar(value="")
        self.var_contador = tk.IntVar(value=0)
        self.var_mensaje = tk.StringVar(
            value="¡Bienvenido a Tkinter! Escribe tu nombre o pulsa los botones."
        )

        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        """Construye todos los elementos gráficos en la ventana."""
        # 1. Encabezado principal
        frame_header = tk.Frame(self.root, bg="#1E293B", padx=20, pady=15)
        frame_header.pack(fill=tk.X)

        lbl_titulo = tk.Label(
            frame_header,
            text="Explorador de Fundamentos Tkinter",
            font=("Helvetica", 16, "bold"),
            fg="#FFFFFF",
            bg="#1E293B"
        )
        lbl_titulo.pack(anchor="w")

        lbl_subtitulo = tk.Label(
            frame_header,
            text="Ventana principal, ciclo mainloop(), widgets esenciales y variables de control.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#1E293B"
        )
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))

        # Contenedor central
        contenedor = tk.Frame(self.root, bg="#F3F4F6", padx=25, pady=20)
        contenedor.pack(fill=tk.BOTH, expand=True)

        # 2. Sección: Entrada de texto reactiva
        lbl_seccion_input = tk.Label(
            contenedor,
            text="1. ENTRADA Y VARIABLE DE CONTROL (StringVar):",
            font=("Helvetica", 10, "bold"),
            fg="#334155",
            bg="#F3F4F6"
        )
        lbl_seccion_input.pack(anchor="w", pady=(0, 5))

        frame_input = tk.Frame(contenedor, bg="#F3F4F6")
        frame_input.pack(fill=tk.X, pady=(0, 15))

        lbl_campo = tk.Label(frame_input, text="Nombre:", font=("Helvetica", 10), bg="#F3F4F6")
        lbl_campo.pack(side=tk.LEFT, padx=(0, 10))

        self.txt_nombre = tk.Entry(
            frame_input,
            textvariable=self.var_nombre,
            font=("Helvetica", 11),
            relief=tk.SOLID,
            bd=1
        )
        self.txt_nombre.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.txt_nombre.focus()  # Poner foco al iniciar

        btn_saludar = tk.Button(
            frame_input,
            text="Saludar",
            font=("Helvetica", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.accion_saludar
        )
        btn_saludar.pack(side=tk.LEFT)

        # 3. Sección: Contador interactivo (IntVar)
        lbl_seccion_contador = tk.Label(
            contenedor,
            text="2. CONTADOR REACTIVO (IntVar):",
            font=("Helvetica", 10, "bold"),
            fg="#334155",
            bg="#F3F4F6"
        )
        lbl_seccion_contador.pack(anchor="w", pady=(0, 5))

        frame_contador = tk.Frame(contenedor, bg="#FFFFFF", relief=tk.SOLID, bd=1, padx=15, pady=10)
        frame_contador.pack(fill=tk.X, pady=(0, 15))

        lbl_valor_contador = tk.Label(
            frame_contador,
            textvariable=self.var_contador,
            font=("Helvetica", 20, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
            width=5
        )
        lbl_valor_contador.pack(side=tk.LEFT, padx=(0, 15))

        btn_incrementar = tk.Button(
            frame_contador,
            text="+ Incrementar",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self.modificar_contador(1)
        )
        btn_incrementar.pack(side=tk.LEFT, padx=5)

        btn_decrementar = tk.Button(
            frame_contador,
            text="- Decrementar",
            bg="#EF4444",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self.modificar_contador(-1)
        )
        btn_decrementar.pack(side=tk.LEFT, padx=5)

        btn_reiniciar = tk.Button(
            frame_contador,
            text="↺ Reiniciar",
            bg="#64748B",
            fg="white",
            font=("Helvetica", 9),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.reiniciar_contador
        )
        btn_reiniciar.pack(side=tk.LEFT, padx=5)

        # 4. Sección: Tarjeta de estado / salida dinámica
        lbl_seccion_salida = tk.Label(
            contenedor,
            text="3. MENSAJE DINÁMICO EN TIEMPO REAL:",
            font=("Helvetica", 10, "bold"),
            fg="#334155",
            bg="#F3F4F6"
        )
        lbl_seccion_salida.pack(anchor="w", pady=(0, 5))

        self.lbl_mensaje = tk.Label(
            contenedor,
            textvariable=self.var_mensaje,
            font=("Helvetica", 10, "italic"),
            fg="#1E293B",
            bg="#E2E8F0",
            relief=tk.FLAT,
            wraplength=480,
            justify=tk.LEFT,
            padx=12,
            pady=12
        )
        self.lbl_mensaje.pack(fill=tk.X, pady=(0, 10))

        # 5. Barra inferior con información del sistema Tkinter
        frame_status = tk.Frame(self.root, bg="#CBD5E1", padx=10, pady=5)
        frame_status.pack(side=tk.BOTTOM, fill=tk.X)

        tk_version = self.root.tk.call("info", "patchlevel")
        lbl_info = tk.Label(
            frame_status,
            text=f"Tkinter activo • Versión de Tcl/Tk: {tk_version}",
            font=("Helvetica", 8),
            bg="#CBD5E1",
            fg="#475569"
        )
        lbl_info.pack(side=tk.LEFT)

    def accion_saludar(self) -> None:
        """Lee el texto del Entry y actualiza el mensaje dinámicamente."""
        nombre = self.var_nombre.get().strip()
        if nombre:
            self.var_mensaje.set(f"¡Hola, {nombre}! Has activado tu primer evento en Tkinter con éxito 🎉")
            self.lbl_mensaje.config(bg="#DBEAFE", fg="#1E40AF")
        else:
            self.var_mensaje.set("⚠️ Por favor escribe tu nombre en el campo de texto antes de pulsar el botón.")
            self.lbl_mensaje.config(bg="#FEE2E2", fg="#991B1B")

    def modificar_contador(self, cambio: int) -> None:
        """Modifica el valor del contador y actualiza el mensaje descriptivo."""
        nuevo_valor = self.var_contador.get() + cambio
        self.var_contador.set(nuevo_valor)
        self.var_mensaje.set(f"El contador ha cambiado a {nuevo_valor} (usando IntVar).")
        self.lbl_mensaje.config(bg="#E0F2FE", fg="#0369A1")

    def reiniciar_contador(self) -> None:
        """Reinicia el contador a cero."""
        self.var_contador.set(0)
        self.var_mensaje.set("Contador reiniciado a 0.")
        self.lbl_mensaje.config(bg="#F1F5F9", fg="#334155")


def main():
    # Inicialización de la raíz de la aplicación Tkinter
    root = tk.Tk()
    app = VentanaFundamentos(root)
    # Inicio del bucle infinito de escucha de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
