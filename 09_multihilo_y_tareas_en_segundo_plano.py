"""
09_multihilo_y_tareas_en_segundo_plano.py
=========================================
Resolución de la congelación de interfaz (UI Freeze) mediante ejecución multihilo:
- El problema: operaciones pesadas (I/O, descargas, cómputo) en el hilo principal bloquean mainloop().
- La solución correcta: threading.Thread (hilos daemon) + cola segura (queue.Queue) + polling con root.after().
- Demostración comparativa en vivo:
  * Prueba A: Tarea pesada en hilo principal (demuestra el congelamiento total).
  * Prueba B: Tarea pesada en hilo secundario (fluidez 60 FPS ininterrumpida).
- Soporte para cancelación de tareas en progreso y reporte de progreso porcentual.
"""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk


class MultihiloApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("09 - Concurrencia y Multihilo sin Congelar la GUI")
        self.root.geometry("860x650")
        self.root.minsize(760, 560)
        self.root.configure(bg="#F1F5F9")

        # Cola para comunicación segura entre hilos secundarios y el hilo principal
        self.cola_mensajes = queue.Queue()

        # Variable de control de cancelación
        self.cancelar_solicitado = False
        self.tarea_en_progreso = False

        # Variable para la animación de fluidez continua
        self.angulo_spinner = 0

        self._crear_interfaz()
        self._iniciar_indicador_fluidez()
        self._escuchar_cola()

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", padx=20, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Concurrencia: threading.Thread + queue.Queue en Tkinter",
            font=("Helvetica", 15, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Evita la congelación de la interfaz mediante hilos secundarios y comunicación no bloqueante.",
            font=("Helvetica", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w", pady=(2, 0))

        # Contenedor principal
        cuerpo = tk.Frame(self.root, bg="#F1F5F9", padx=15, pady=15)
        cuerpo.pack(fill=tk.BOTH, expand=True)

        # 1. Panel del indicador de fluidez (Heartbeat de 60 FPS)
        frame_heartbeat = tk.LabelFrame(
            cuerpo,
            text=" Testigo de Fluidez de la Interfaz (60 FPS) ",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=10
        )
        frame_heartbeat.pack(fill=tk.X, pady=(0, 15))

        self.canvas_spinner = tk.Canvas(frame_heartbeat, width=50, height=50, bg="#FFFFFF", highlightthickness=0)
        self.canvas_spinner.pack(side=tk.LEFT, padx=(0, 15))

        lbl_heartbeat_desc = tk.Label(
            frame_heartbeat,
            text="Si este círculo giratorio se detiene, la interfaz está TOTALMENTE CONGELADA.\n"
                 "Si sigue girando suavemente, la interfaz responde y procesa eventos con normalidad.",
            font=("Helvetica", 9),
            bg="#FFFFFF",
            fg="#475569",
            justify=tk.LEFT
        )
        lbl_heartbeat_desc.pack(side=tk.LEFT)

        # 2. Panel de control de tareas
        frame_controles = tk.LabelFrame(
            cuerpo,
            text=" Ejecución de Tareas Pesadas (Simulación de Procesamiento / Descarga) ",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=15
        )
        frame_controles.pack(fill=tk.X, pady=(0, 15))

        # Botones de prueba
        frame_btns = tk.Frame(frame_controles, bg="#FFFFFF")
        frame_btns.pack(fill=tk.X, pady=(0, 15))

        self.btn_bloqueante = tk.Button(
            frame_btns,
            text="⚠️ Modo Bloqueante (Hilo Principal)",
            bg="#EF4444",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            command=self._ejecutar_modo_bloqueante
        )
        self.btn_bloqueante.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_multihilo = tk.Button(
            frame_btns,
            text="🚀 Modo Multihilo Seguro (threading)",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            command=self._ejecutar_modo_multihilo
        )
        self.btn_multihilo.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_cancelar = tk.Button(
            frame_btns,
            text="⏹ Cancelar Tarea",
            bg="#64748B",
            fg="white",
            font=("Helvetica", 9),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            state="disabled",
            command=self._solicitar_cancelacion
        )
        self.btn_cancelar.pack(side=tk.LEFT)

        # Barra de progreso
        self.progreso_var = tk.DoubleVar(value=0)
        self.barra_progreso = ttk.Progressbar(frame_controles, orient="horizontal", mode="determinate", variable=self.progreso_var, maximum=100)
        self.barra_progreso.pack(fill=tk.X, pady=(0, 5))

        self.lbl_progreso = tk.Label(frame_controles, text="Estado: En espera", font=("Helvetica", 9), bg="#FFFFFF", fg="#64748B")
        self.lbl_progreso.pack(anchor="w")

        # 3. Bitácora de eventos
        frame_log = tk.LabelFrame(
            cuerpo,
            text=" Registro de Actividad y Mensajes del Hilo Secundario ",
            font=("Helvetica", 10, "bold"),
            bg="#1E293B",
            fg="#38BDF8",
            padx=10,
            pady=10
        )
        frame_log.pack(fill=tk.BOTH, expand=True)

        self.txt_log = tk.Text(frame_log, bg="#0F172A", fg="#E2E8F0", font=("Consolas", 9), relief=tk.FLAT, padx=8, pady=8)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def _iniciar_indicador_fluidez(self) -> None:
        """Animación continua a ~60 FPS que verifica si el hilo principal responde."""
        self.canvas_spinner.delete("all")
        cx, cy, r = 25, 25, 18
        self.angulo_spinner = (self.angulo_spinner + 8) % 360

        # Dibujar arco rotatorio
        self.canvas_spinner.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#E2E8F0", width=3)
        self.canvas_spinner.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=self.angulo_spinner,
            extent=90,
            outline="#2563EB",
            width=3,
            style=tk.ARC
        )

        self.root.after(16, self._iniciar_indicador_fluidez)

    def _log(self, mensaje: str) -> None:
        self.txt_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {mensaje}\n")
        self.txt_log.see(tk.END)

    # -------------------------------------------------------------
    # DEMOSTRACIÓN A: HILO PRINCIPAL (INCORRECTO / BLOQUEANTE)
    # -------------------------------------------------------------
    def _ejecutar_modo_bloqueante(self) -> None:
        self._log("⚠️ INICIANDO EN HILO PRINCIPAL: La interfaz se congelará por completo durante 5 segundos...")
        self.lbl_progreso.config(text="Estado: Procesando en hilo principal (GUI CONGELADA)...")
        self.root.update()  # Forzar actualización inicial antes de bloquear

        # Bucle de sueño que bloquea el hilo de la GUI
        for i in range(1, 6):
            time.sleep(1.0)
            self.progreso_var.set(i * 20)
            # Nota: Al estar en el mismo hilo, los eventos de ratón/teclado y animaciones se detienen.

        self._log("✅ Fin de tarea bloqueante. Observa cómo el testigo giratorio se detuvo por completo.")
        self.lbl_progreso.config(text="Estado: Finalizado en hilo principal.")

    # -------------------------------------------------------------
    # DEMOSTRACIÓN B: HILO SECUNDARIO (CORRECTO / NO BLOQUEANTE)
    # -------------------------------------------------------------
    def _ejecutar_modo_multihilo(self) -> None:
        if self.tarea_en_progreso:
            return

        self.tarea_en_progreso = True
        self.cancelar_solicitado = False
        self.btn_multihilo.config(state="disabled")
        self.btn_bloqueante.config(state="disabled")
        self.btn_cancelar.config(state="normal")
        self.progreso_var.set(0)

        self._log("🚀 Lanzando tarea pesada en un hilo secundario (daemon=True)...")

        # Crear e iniciar el hilo trabajador
        hilo = threading.Thread(target=self._trabajo_en_segundo_plano, daemon=True)
        hilo.start()

    def _trabajo_en_segundo_plano(self) -> None:
        """Función que corre exclusivamente en el hilo secundario.
        IMPORTANTE: NUNCA modificar widgets de Tkinter directamente desde este hilo.
        En su lugar, enviar mensajes a la cola_mensajes.
        """
        pasos_totales = 50
        for paso in range(1, pasos_totales + 1):
            if self.cancelar_solicitado:
                self.cola_mensajes.put(("cancelado", "La tarea fue cancelada por el usuario."))
                return

            time.sleep(0.1)  # Simulación de trabajo de 100ms por paso (5 segundos total)
            porcentaje = (paso / pasos_totales) * 100

            # Enviar actualización a la cola
            self.cola_mensajes.put(("progreso", porcentaje, f"Procesando lote {paso}/{pasos_totales}..."))

        self.cola_mensajes.put(("completado", "¡Procesamiento masivo finalizado exitosamente sin congelar la GUI!"))

    def _solicitar_cancelacion(self) -> None:
        if self.tarea_en_progreso:
            self.cancelar_solicitado = True
            self._log("Solicitando cancelación de la tarea...")

    def _escuchar_cola(self) -> None:
        """Método ejecutado periódicamente en el hilo principal para consumir eventos de la cola."""
        try:
            while True:
                mensaje = self.cola_mensajes.get_nowait()
                tipo = mensaje[0]

                if tipo == "progreso":
                    _, pct, desc = mensaje
                    self.progreso_var.set(pct)
                    self.lbl_progreso.config(text=f"Estado: {desc} ({pct:.0f}%)")

                elif tipo == "completado":
                    _, desc = mensaje
                    self.progreso_var.set(100)
                    self.lbl_progreso.config(text=f"Estado: {desc}")
                    self._log(f"✅ {desc}")
                    self._restablecer_botones()

                elif tipo == "cancelado":
                    _, desc = mensaje
                    self.lbl_progreso.config(text=f"Estado: {desc}")
                    self._log(f"⏹ {desc}")
                    self._restablecer_botones()

                self.cola_mensajes.task_done()

        except queue.Empty:
            pass

        # Volver a consultar la cola en 50 milisegundos
        self.root.after(50, self._escuchar_cola)

    def _restablecer_botones(self) -> None:
        self.tarea_en_progreso = False
        self.cancelar_solicitado = False
        self.btn_multihilo.config(state="normal")
        self.btn_bloqueante.config(state="normal")
        self.btn_cancelar.config(state="disabled")


def main():
    root = tk.Tk()
    app = MultihiloApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
