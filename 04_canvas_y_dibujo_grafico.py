"""
04_canvas_y_dibujo_grafico.py
=============================
Dominio del widget Canvas en Tkinter:
- Renderizado de primitivas 2D: líneas, rectángulos, óvalos, polígonos, arcos y texto.
- Manejo de identificadores de objeto (IDs) y etiquetas (tags).
- Mini pizarra de dibujo a mano alzada capturando eventos de ratón (<Button-1>, <B1-Motion>).
- Animación interactiva en tiempo real (pelota rebotando) mediante el método .after().
- Selectores de color, grosor de trazo y borrado de elementos.
"""

import math
import tkinter as tk
from tkinter import ttk


class CanvasDemoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("04 - Canvas: Dibujo Gráfico y Animaciones en 2D")
        self.root.geometry("880x660")
        self.root.minsize(750, 550)
        self.root.configure(bg="#0F172A")

        # Variables de dibujo libre
        self.color_actual = "#3B82F6"
        self.grosor_pincel = 3
        self.ultimo_x = None
        self.ultimo_y = None

        # Variables de la animación de pelota
        self.animando = False
        self.pelota_id = None
        self.ball_x = 50.0
        self.ball_y = 50.0
        self.ball_radius = 16
        self.vel_x = 4.5
        self.vel_y = 3.2

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#1E293B", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Lienzo Gráfico y Animaciones (tk.Canvas)",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Explora dibujo vectorial, primitivas geométricas, pizarra interactiva y física simple con bucle after().",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w", pady=(2, 0))

        # Cuaderno de pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        tab_primitivas = tk.Frame(notebook, bg="#F8FAFC")
        tab_pizarra = tk.Frame(notebook, bg="#F8FAFC")
        tab_animacion = tk.Frame(notebook, bg="#F8FAFC")

        notebook.add(tab_primitivas, text="  1. Primitivas Gráficas  ")
        notebook.add(tab_pizarra, text="  2. Pizarra de Dibujo Libre  ")
        notebook.add(tab_animacion, text="  3. Animación y Física 2D  ")

        self._construir_tab_primitivas(tab_primitivas)
        self._construir_tab_pizarra(tab_pizarra)
        self._construir_tab_animacion(tab_animacion)

    # -------------------------------------------------------------
    # 1. PESTAÑA: Primitivas Gráficas
    # -------------------------------------------------------------
    def _construir_tab_primitivas(self, contenedor: tk.Frame) -> None:
        canvas = tk.Canvas(contenedor, bg="#1E1E2E", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 1. Líneas y flechas
        canvas.create_text(80, 25, text="Líneas y Flechas", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        canvas.create_line(30, 50, 180, 50, fill="#38BDF8", width=3)
        canvas.create_line(30, 80, 180, 80, fill="#34D399", width=2, arrow=tk.LAST)
        canvas.create_line(30, 110, 180, 110, fill="#F472B6", width=2, dash=(6, 4))

        # 2. Rectángulos
        canvas.create_text(290, 25, text="Rectángulos (fill & outline)", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        canvas.create_rectangle(220, 50, 340, 120, fill="#6366F1", outline="#A5B4FC", width=2)
        canvas.create_rectangle(240, 70, 360, 140, fill="", outline="#F59E0B", width=3)

        # 3. Óvalos y círculos
        canvas.create_text(480, 25, text="Círculos y Elipses", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        canvas.create_oval(410, 50, 480, 120, fill="#EC4899", outline="#FDF2F8", width=2)  # Círculo
        canvas.create_oval(500, 60, 610, 110, fill="#10B981", outline="#6EE7B7", width=2)  # Elipse

        # 4. Polígonos (Triángulo / Estrella)
        canvas.create_text(710, 25, text="Polígono Personalizado", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        puntos_triangulo = [650, 130, 710, 50, 770, 130]
        canvas.create_polygon(puntos_triangulo, fill="#8B5CF6", outline="#C4B5FD", width=2)

        # 5. Arcos (Sectores y tartas)
        canvas.create_text(130, 180, text="Arcos y Sectores Circulares", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        canvas.create_arc(40, 210, 160, 330, start=0, extent=120, fill="#EF4444", outline="white", width=2)
        canvas.create_arc(40, 210, 160, 330, start=120, extent=90, fill="#F59E0B", outline="white", width=2)
        canvas.create_arc(40, 210, 160, 330, start=210, extent=150, fill="#10B981", outline="white", width=2)

        # 6. Diagrama de barras generado con primitivas
        canvas.create_text(480, 180, text="Gráfico de Barras Vectorial con Canvas", fill="#94A3B8", font=("Helvetica", 10, "bold"))
        valores = [("Python", 85, "#38BDF8"), ("JavaScript", 70, "#FBBF24"), ("Rust", 55, "#F97316"), ("Go", 60, "#34D399")]
        base_x = 280
        base_y = 350

        # Ejes
        canvas.create_line(base_x, base_y, base_x + 360, base_y, fill="#64748B", width=2)
        canvas.create_line(base_x, base_y, base_x, base_y - 140, fill="#64748B", width=2)

        for i, (lenguaje, porcentaje, color) in enumerate(valores):
            x1 = base_x + 30 + (i * 80)
            x2 = x1 + 50
            alto_barra = (porcentaje / 100) * 120
            y1 = base_y - alto_barra
            y2 = base_y

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            canvas.create_text((x1 + x2) / 2, y1 - 12, text=f"{porcentaje}%", fill="white", font=("Helvetica", 8, "bold"))
            canvas.create_text((x1 + x2) / 2, base_y + 16, text=lenguaje, fill="#CBD5E1", font=("Helvetica", 8))

    # -------------------------------------------------------------
    # 2. PESTAÑA: Pizarra de Dibujo Libre
    # -------------------------------------------------------------
    def _construir_tab_pizarra(self, contenedor: tk.Frame) -> None:
        # Barra de herramientas superior
        toolbar = tk.Frame(contenedor, bg="#E2E8F0", padx=10, pady=8)
        toolbar.pack(fill=tk.X)

        tk.Label(toolbar, text="Colores:", font=("Helvetica", 9, "bold"), bg="#E2E8F0").pack(side=tk.LEFT, padx=(0, 5))

        colores = ["#000000", "#EF4444", "#10B981", "#3B82F6", "#8B5CF6", "#F59E0B", "#FFFFFF"]
        for c in colores:
            btn_c = tk.Button(
                toolbar,
                bg=c,
                width=3,
                height=1,
                relief=tk.RAISED,
                cursor="hand2",
                command=lambda col=c: self._seleccionar_color(col)
            )
            btn_c.pack(side=tk.LEFT, padx=3)

        tk.Label(toolbar, text="Grosor:", font=("Helvetica", 9, "bold"), bg="#E2E8F0").pack(side=tk.LEFT, padx=(15, 5))
        slider_grosor = tk.Scale(
            toolbar,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            bg="#E2E8F0",
            highlightthickness=0,
            command=self._cambiar_grosor
        )
        slider_grosor.set(3)
        slider_grosor.pack(side=tk.LEFT, padx=5)

        btn_borrar = tk.Button(
            toolbar,
            text="🗑️ Limpiar Pizarra",
            bg="#DC2626",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            cursor="hand2",
            command=self._limpiar_pizarra
        )
        btn_borrar.pack(side=tk.RIGHT, padx=5)

        # Lienzo para pintar
        self.canvas_pizarra = tk.Canvas(contenedor, bg="#FFFFFF", cursor="pencil")
        self.canvas_pizarra.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Eventos de ratón
        self.canvas_pizarra.bind("<Button-1>", self._iniciar_dibujo)
        self.canvas_pizarra.bind("<B1-Motion>", self._dibujar_trazo)
        self.canvas_pizarra.bind("<ButtonRelease-1>", self._terminar_dibujo)

    def _seleccionar_color(self, nuevo_color: str) -> None:
        self.color_actual = nuevo_color

    def _cambiar_grosor(self, valor: str) -> None:
        self.grosor_pincel = int(valor)

    def _iniciar_dibujo(self, evento: tk.Event) -> None:
        self.ultimo_x = evento.x
        self.ultimo_y = evento.y

    def _dibujar_trazo(self, evento: tk.Event) -> None:
        if self.ultimo_x is not None and self.ultimo_y is not None:
            self.canvas_pizarra.create_line(
                self.ultimo_x,
                self.ultimo_y,
                evento.x,
                evento.y,
                fill=self.color_actual,
                width=self.grosor_pincel,
                capstyle=tk.ROUND,
                smooth=True
            )
        self.ultimo_x = evento.x
        self.ultimo_y = evento.y

    def _terminar_dibujo(self, _evento: tk.Event) -> None:
        self.ultimo_x = None
        self.ultimo_y = None

    def _limpiar_pizarra(self) -> None:
        self.canvas_pizarra.delete("all")

    # -------------------------------------------------------------
    # 3. PESTAÑA: Animación y Física 2D
    # -------------------------------------------------------------
    def _construir_tab_animacion(self, contenedor: tk.Frame) -> None:
        panel_controles = tk.Frame(contenedor, bg="#E2E8F0", padx=10, pady=8)
        panel_controles.pack(fill=tk.X)

        self.btn_animar = tk.Button(
            panel_controles,
            text="▶ Iniciar Animación",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._alternar_animacion
        )
        self.btn_animar.pack(side=tk.LEFT, padx=5)

        self.lbl_estado_anim = tk.Label(
            panel_controles,
            text="Estado: En pausa | Ciclo: root.after(16ms) ~ 60 FPS",
            font=("Helvetica", 9),
            bg="#E2E8F0",
            fg="#475569"
        )
        self.lbl_estado_anim.pack(side=tk.LEFT, padx=15)

        # Lienzo para animación
        self.canvas_anim = tk.Canvas(contenedor, bg="#0F172A", highlightthickness=0)
        self.canvas_anim.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pelota inicial
        r = self.ball_radius
        self.pelota_id = self.canvas_anim.create_oval(
            self.ball_x - r,
            self.ball_y - r,
            self.ball_x + r,
            self.ball_y + r,
            fill="#38BDF8",
            outline="#E0F2FE",
            width=2
        )

    def _alternar_animacion(self) -> None:
        self.animando = not self.animando
        if self.animando:
            self.btn_animar.config(text="⏸ Pausar Animación", bg="#F59E0B")
            self.lbl_estado_anim.config(text="Estado: En ejecución (60 FPS)")
            self._paso_animacion()
        else:
            self.btn_animar.config(text="▶ Reanudar Animación", bg="#10B981")
            self.lbl_estado_anim.config(text="Estado: En pausa")

    def _paso_animacion(self) -> None:
        if not self.animando:
            return

        ancho_lienzo = self.canvas_anim.winfo_width()
        alto_lienzo = self.canvas_anim.winfo_height()

        # Si aún no se renderizó la geometría completa, usar fallback
        if ancho_lienzo < 50:
            ancho_lienzo, alto_lienzo = 800, 450

        # Mover posición
        self.ball_x += self.vel_x
        self.ball_y += self.vel_y
        r = self.ball_radius

        # Colisión con bordes horizontales
        if self.ball_x + r >= ancho_lienzo:
            self.ball_x = ancho_lienzo - r
            self.vel_x = -abs(self.vel_x)
            self._cambiar_color_pelota("#F43F5E")
        elif self.ball_x - r <= 0:
            self.ball_x = r
            self.vel_x = abs(self.vel_x)
            self._cambiar_color_pelota("#3B82F6")

        # Colisión con bordes verticales
        if self.ball_y + r >= alto_lienzo:
            self.ball_y = alto_lienzo - r
            self.vel_y = -abs(self.vel_y)
            self._cambiar_color_pelota("#10B981")
        elif self.ball_y - r <= 0:
            self.ball_y = r
            self.vel_y = abs(self.vel_y)
            self._cambiar_color_pelota("#A855F7")

        # Actualizar coordenadas en el Canvas
        self.canvas_anim.coords(
            self.pelota_id,
            self.ball_x - r,
            self.ball_y - r,
            self.ball_x + r,
            self.ball_y + r
        )

        # Planificar el siguiente frame (~60 cuadros por segundo = ~16 ms)
        self.root.after(16, self._paso_animacion)

    def _cambiar_color_pelota(self, color: str) -> None:
        self.canvas_anim.itemconfig(self.pelota_id, fill=color)


def main():
    root = tk.Tk()
    app = CanvasDemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
