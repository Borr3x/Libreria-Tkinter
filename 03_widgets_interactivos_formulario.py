"""
03_widgets_interactivos_formulario.py
=====================================
Demostración completa de captura de datos de usuario con widgets interactivos:
- Campos de texto: Entry (normal, contraseña con máscara show='*'), Text multilínea con Scrollbar.
- Opciones binarias: Checkbutton (BooleanVar).
- Selección excluyente: Radiobutton agrupados (StringVar).
- Desplegables y selectores numéricos: Combobox y Spinbox (ttk).
- Control deslizante continuo: Scale con evento de cambio en vivo.
- Panel de inspección reactiva en tiempo real que serializa el estado de las variables.
"""

import json
import tkinter as tk
from tkinter import ttk


class FormularioWidgetsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("03 - Widgets Interactivos y Formularios de Entrada")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#F1F5F9")

        # Variables reactivas para almacenar el estado del formulario
        self.var_usuario = tk.StringVar(value="")
        self.var_password = tk.StringVar(value="")
        self.var_nivel = tk.StringVar(value="Intermedio")
        self.var_notificaciones = tk.BooleanVar(value=True)
        self.var_terminos = tk.BooleanVar(value=False)
        self.var_pais = tk.StringVar(value="México")
        self.var_edad = tk.IntVar(value=25)
        self.var_satisfaccion = tk.IntVar(value=80)

        self._crear_interfaz()
        self._actualizar_resumen()

        # Rastrear cambios automáticos en las variables clave para actualizar el panel
        for var in (
            self.var_usuario,
            self.var_password,
            self.var_nivel,
            self.var_notificaciones,
            self.var_terminos,
            self.var_pais,
            self.var_edad,
            self.var_satisfaccion
        ):
            var.trace_add("write", lambda *_: self._actualizar_resumen())

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Catálogo de Widgets de Entrada de Datos",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Interactúa con cada control y observa cómo se reflejan los valores en el panel en tiempo real.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w", pady=(2, 0))

        # Panel principal dividido en dos columnas: Izquierda (Formulario), Derecha (Inspección)
        cuerpo = tk.Frame(self.root, bg="#F1F5F9", padx=15, pady=15)
        cuerpo.pack(fill=tk.BOTH, expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        # Columna Izquierda: Formulario
        col_form = tk.LabelFrame(
            cuerpo,
            text=" Controles del Formulario ",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=15
        )
        col_form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 1. Campos de texto
        tk.Label(col_form, text="Nombre de Usuario (Entry):", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
        entry_user = tk.Entry(col_form, textvariable=self.var_usuario, font=("Helvetica", 10), relief=tk.SOLID, bd=1)
        entry_user.pack(fill=tk.X, pady=(2, 8))
        self.var_usuario.set("alex_dev")

        tk.Label(col_form, text="Contraseña (Entry con show='•'):", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
        entry_pass = tk.Entry(col_form, textvariable=self.var_password, show="•", font=("Helvetica", 10), relief=tk.SOLID, bd=1)
        entry_pass.pack(fill=tk.X, pady=(2, 12))
        self.var_password.set("SuperSecreto123")

        # 2. Radiobuttons (Nivel de experiencia)
        tk.Label(col_form, text="Nivel de Experiencia (Radiobutton):", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
        frame_radios = tk.Frame(col_form, bg="white")
        frame_radios.pack(fill=tk.X, pady=(2, 10))

        for opcion in ["Principiante", "Intermedio", "Avanzado"]:
            rb = tk.Radiobutton(
                frame_radios,
                text=opcion,
                value=opcion,
                variable=self.var_nivel,
                bg="white",
                activebackground="white",
                font=("Helvetica", 9)
            )
            rb.pack(side=tk.LEFT, padx=(0, 15))

        # 3. Combobox y Spinbox
        frame_selectores = tk.Frame(col_form, bg="white")
        frame_selectores.pack(fill=tk.X, pady=(0, 10))
        frame_selectores.columnconfigure(0, weight=1)
        frame_selectores.columnconfigure(1, weight=1)

        # País (Combobox)
        tk.Label(frame_selectores, text="País (ttk.Combobox):", font=("Helvetica", 9, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        paises = ["Argentina", "Chile", "Colombia", "España", "México", "Perú", "Uruguay"]
        cbo_pais = ttk.Combobox(frame_selectores, textvariable=self.var_pais, values=paises, state="readonly", font=("Helvetica", 9))
        cbo_pais.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(2, 0))

        # Edad (Spinbox)
        tk.Label(frame_selectores, text="Edad (ttk.Spinbox):", font=("Helvetica", 9, "bold"), bg="white").grid(row=0, column=1, sticky="w")
        spn_edad = ttk.Spinbox(frame_selectores, from_=16, to=99, textvariable=self.var_edad, width=5, font=("Helvetica", 9))
        spn_edad.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(2, 0))

        # 4. Deslizador Scale
        tk.Label(col_form, text="Nivel de Satisfacción (Scale: 0 a 100%):", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w", pady=(8, 0))
        scale_sat = tk.Scale(
            col_form,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.var_satisfaccion,
            bg="white",
            troughcolor="#E2E8F0",
            activebackground="#2563EB",
            highlightthickness=0
        )
        scale_sat.pack(fill=tk.X, pady=(0, 10))

        # 5. Checkbuttons
        chk_notif = tk.Checkbutton(
            col_form,
            text="Deseo recibir notificaciones periódicas (BooleanVar)",
            variable=self.var_notificaciones,
            bg="white",
            activebackground="white",
            font=("Helvetica", 9)
        )
        chk_notif.pack(anchor="w")

        chk_term = tk.Checkbutton(
            col_form,
            text="Acepto los términos y condiciones del servicio",
            variable=self.var_terminos,
            bg="white",
            activebackground="white",
            font=("Helvetica", 9, "bold"),
            fg="#2563EB"
        )
        chk_term.pack(anchor="w", pady=(2, 10))

        # 6. Área de texto multilínea con Scrollbar (Text)
        tk.Label(col_form, text="Biografía / Observaciones (Text con Scrollbar):", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
        frame_text = tk.Frame(col_form, bg="white")
        frame_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        scroll_text = tk.Scrollbar(frame_text)
        scroll_text.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_bio = tk.Text(
            frame_text,
            height=4,
            font=("Helvetica", 9),
            yscrollcommand=scroll_text.set,
            relief=tk.SOLID,
            bd=1
        )
        self.txt_bio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_text.config(command=self.txt_bio.yview)
        self.txt_bio.insert(tk.END, "Desarrollador apasionado por las interfaces de usuario limpias y funcionales en Python.")
        self.txt_bio.bind("<KeyRelease>", lambda _: self._actualizar_resumen())

        # Columna Derecha: Panel de Inspección Reactivo
        col_resumen = tk.LabelFrame(
            cuerpo,
            text=" Estado Reactivo de Variables (JSON) ",
            font=("Helvetica", 10, "bold"),
            bg="#1E293B",
            fg="#38BDF8",
            padx=12,
            pady=12
        )
        col_resumen.grid(row=0, column=1, sticky="nsew")

        self.txt_json = tk.Text(
            col_resumen,
            bg="#0F172A",
            fg="#A7F3D0",
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.txt_json.pack(fill=tk.BOTH, expand=True)

        btn_limpiar = tk.Button(
            col_resumen,
            text="Limpiar Formulario",
            bg="#EF4444",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            pady=6,
            command=self._limpiar_formulario
        )
        btn_limpiar.pack(fill=tk.X, pady=(10, 0))

    def _actualizar_resumen(self) -> None:
        """Serializa el estado actual de las variables y lo muestra en formato JSON formateado."""
        try:
            bio_texto = self.txt_bio.get("1.0", tk.END).strip()
        except Exception:
            bio_texto = ""

        datos = {
            "usuario": self.var_usuario.get(),
            "password_longitud": len(self.var_password.get()),
            "nivel_experiencia": self.var_nivel.get(),
            "pais_seleccionado": self.var_pais.get(),
            "edad": self.var_edad.get(),
            "satisfaccion_pct": self.var_satisfaccion.get(),
            "notificaciones_activas": self.var_notificaciones.get(),
            "acepto_terminos": self.var_terminos.get(),
            "biografia": bio_texto
        }

        self.txt_json.delete("1.0", tk.END)
        self.txt_json.insert(tk.END, json.dumps(datos, indent=2, ensure_ascii=False))

    def _limpiar_formulario(self) -> None:
        self.var_usuario.set("")
        self.var_password.set("")
        self.var_nivel.set("Principiante")
        self.var_pais.set("México")
        self.var_edad.set(18)
        self.var_satisfaccion.set(50)
        self.var_notificaciones.set(False)
        self.var_terminos.set(False)
        self.txt_bio.delete("1.0", tk.END)
        self._actualizar_resumen()


def main():
    root = tk.Tk()
    app = FormularioWidgetsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
