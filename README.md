# 🐍 Tkinter Mastery Showcase - Guía Práctica de Python GUI

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-brightgreen.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)](#requisitos-e-instalación)

Bienvenido a **Tkinter Mastery Showcase**, un repositorio educativo y profesional diseñado para aprender, dominar y consultar las capacidades de **Tkinter** y **ttk (Themed Tkinter)** en Python.

Todos los ejemplos han sido desarrollados utilizando **únicamente la biblioteca estándar de Python**, con código limpio, tipado estático opcional (`type hints`), estructuración orientada a objetos (POO) y buenas prácticas de diseño de interfaces.

---

## 📑 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Panel de Control Interactivo (`launcher.py`)](#-panel-de-control-interactivo-launcherpy)
- [Guía Detallada Archivo por Archivo](#-guía-detallada-archivo-por-archivo)
  - [01. Fundamentos y Conceptos Básicos](#01_fundamentos_y_conceptos_basicospy)
  - [02. Gestores de Posicionamiento](#02_gestores_de_posicionamientopy)
  - [03. Widgets Interactivos y Formularios](#03_widgets_interactivos_formulariopy)
  - [04. Canvas: Dibujo Gráfico y Animaciones](#04_canvas_y_dibujo_graficopy)
  - [05. Diálogos Nativos y Ventanas Modales](#05_dialogos_ventanas_secundariaspy)
  - [06. Menús, Eventos y Atajos](#06_menus_eventos_y_atajospy)
  - [07. Estilos Modernos y Temas ttk](#07_estilos_modernos_ttkpy)
  - [08. Tablas y Jerarquías con Treeview](#08_tablas_y_jerarquias_treeviewpy)
  - [09. Multihilo y Concurrencia](#09_multihilo_y_tareas_en_segundo_planopy)
  - [10. Proyecto Integrador: TaskFlow Pro](#10_proyecto_integrador_gestor_tareaspy)
- [Requisitos e Instalación](#-requisitos-e-instalación)
- [Cómo Publicar este Repositorio en GitHub](#-cómo-publicar-este-repositorio-en-github)
- [Buenas Prácticas en Tkinter](#-buenas-prácticas-en-tkinter)
- [Licencia](#-licencia)

---

## 🌟 Características Principales

- **Progresión de Aprendizaje Gradual:** Desde un *"Hola Mundo"* con centrado de pantalla hasta un Gestor de Tareas completo con almacenamiento JSON.
- **Sin Dependencias de Terceros:** No requiere `pip install`. Funciona directamente con el intérprete de Python estándar.
- **Lanzador Visual Integrado (`launcher.py`):** Un panel tipo dashboard para explorar y ejecutar cualquier ejemplo con un solo clic.
- **Solución a Problemas Reales:** Incluye ejemplos claros de sincronización multihilo (`threading` + `queue.Queue`) para evitar que la interfaz se congele.
- **Diseño Moderno:** Uso exhaustivo de `ttk.Style`, paletas de colores armónicas, iconos Unicode y fuentes limpias.

---

## 📂 Estructura del Proyecto

```text
tkinter-showcase/
├── launcher.py                                # Dashboard interactivo para lanzar cualquier módulo
├── 01_fundamentos_y_conceptos_basicos.py       # Ciclo de vida, ventana, Labels, Buttons, Entry, variables
├── 02_gestores_de_posicionamiento.py          # Comparativa visual de pack(), grid() y place()
├── 03_widgets_interactivos_formulario.py      # Entry, Checkbutton, Radiobutton, Combobox, Spinbox, Scale
├── 04_canvas_y_dibujo_grafico.py              # Primitivas 2D, pizarra de dibujo y animación a 60 FPS
├── 05_dialogos_ventanas_secundarias.py        # messagebox, filedialog, colorchooser, Toplevel modal
├── 06_menus_eventos_y_atajos.py               # Menús en cascada, clic derecho, bindings y atajos
├── 07_estilos_modernos_ttk.py                 # ttk.Style, explorador de temas y barras de progreso
├── 08_tablas_y_jerarquias_treeview.py         # Tablas CRUD, ordenación interactiva, buscador y árbol
├── 09_multihilo_y_tareas_en_segundo_plano.py  # Concurrencia segura: threading + queue + after()
├── 10_proyecto_integrador_gestor_tareas.py    # Aplicación integral TaskFlow Pro con estadísticas Canvas
├── requirements.txt                           # Información de entorno y compatibilidad de Python
├── .gitignore                                 # Filtros de exclusión para Git y Python
├── LICENSE                                    # Licencia de código abierto MIT
└── README.md                                  # Documentación completa del proyecto
```

---

## 🚀 Panel de Control Interactivo (`launcher.py`)

Para que no tengas que ejecutar cada archivo manualmente desde la consola, el repositorio incluye un **Dashboard Central**:

```bash
python launcher.py
```

### Funcionalidades del Lanzador:
1. **Listado Visual de Módulos:** Muestra cada archivo con su número, título didáctico, nivel de dificultad e insignias de color.
2. **Botón de Ejecución Directa:** Ejecuta el archivo en un subproceso independiente sin bloquear el lanzador.
3. **Filtros por Nivel:** Filtra al instante por *Principiante*, *Intermedio*, *Avanzado* o *Proyecto Completo*.
4. **Buscador en Tiempo Real:** Localiza cualquier funcionalidad tecleando palabras clave como `"canvas"`, `"treeview"` o `"estilos"`.

---

## 📖 Guía Detallada Archivo por Archivo

A continuación se detalla exhaustivamente el propósito, los widgets utilizados y los conceptos técnicos explicados en cada uno de los archivos de código:

---

### `01_fundamentos_y_conceptos_basicos.py`

* **Propósito:** Introducir los fundamentos del desarrollo de interfaces con Tkinter y comprender el ciclo de vida de una aplicación de escritorio.
* **Nivel:** Principiante.
* **Widgets Utilizados:** `tk.Tk`, `tk.Frame`, `tk.Label`, `tk.Button`, `tk.Entry`.
* **Conceptos Clave Explicados:**
  - **Inicialización y ciclo principal:** Uso de `root = tk.Tk()` y el bucle de escucha de eventos `root.mainloop()`.
  - **Propiedades de ventana:** Configuración de título (`title`), dimensiones (`geometry`), tamaño mínimo (`minsize`), restricciones de redimensionamiento (`resizable`) y color de fondo (`bg`).
  - **Centrado dinámico en pantalla:** Cálculo algorítmico de coordenadas `x` e `y` consultando la resolución de pantalla del monitor mediante `winfo_screenwidth()` y `winfo_screenheight()`.
  - **Variables reactivas de Tkinter:** Implementación de `StringVar` e `IntVar` y su enlace bidireccional mediante el parámetro `textvariable`.
  - **Modificación dinámica de widgets:** Uso de `.config()` / `.configure()` para cambiar estilos, colores y textos en tiempo de ejecución en respuesta a eventos de clic.
* **Cómo ejecutarlo:**
  ```bash
  python 01_fundamentos_y_conceptos_basicos.py
  ```

---

### `02_gestores_de_posicionamiento.py`

* **Propósito:** Analizar y comparar los tres motores de maquetación y diseño de interfaces que ofrece Tkinter.
* **Nivel:** Principiante.
* **Widgets Utilizados:** `ttk.Notebook`, `tk.Frame`, `tk.Label`, `tk.Button`, `tk.Entry`, `tk.Text`.
* **Conceptos Clave Explicados:**
  - **1. Gestor `pack()`:** Empaquetamiento lineal contra los bordes de la ventana o contenedor padre (`side=TOP, BOTTOM, LEFT, RIGHT`), relleno de espacio adicional (`fill=X, Y, BOTH`), reclamación de espacio sobrante (`expand=True`) y márgenes internos/externos (`padx`, `pady`, `ipadx`, `ipady`).
  - **2. Gestor `grid()`:** Distribución tabular por filas y columnas (matriz). Control de expansión con `sticky="nsew"`, fusión de celdas adyacentes (`columnspan`, `rowspan`) y configuración de columnas responsivas mediante `columnconfigure(col, weight=1)`.
  - **3. Gestor `place()`:** Posicionamiento explícito por coordenadas absolutas fijas (`x`, `y`, `width`, `height`) y coordenadas porcentuales o relativas (`relx`, `rely`, `relwidth`, `relheight`, `anchor`).
  - **Regla de oro de Tkinter:** Por qué **nunca** se deben mezclar `pack()` y `grid()` en el mismo contenedor padre (evitar bucles infinitos de redibujado de la interfaz).
* **Cómo ejecutarlo:**
  ```bash
  python 02_gestores_de_posicionamiento.py
  ```

---

### `03_widgets_interactivos_formulario.py`

* **Propósito:** Mostrar cómo construir formularios completos de captura de información, validación y lectura reactiva de datos.
* **Nivel:** Intermedio.
* **Widgets Utilizados:** `tk.Entry`, `tk.Text`, `tk.Scrollbar`, `tk.Checkbutton`, `tk.Radiobutton`, `ttk.Combobox`, `ttk.Spinbox`, `tk.Scale`.
* **Conceptos Clave Explicados:**
  - **Enmascarado de contraseñas:** Uso de `show="•"` o `show="*"` en campos `tk.Entry`.
  - **Variables BooleanVar y Checkbuttons:** Manejo de casillas de verificación independientes para términos, condiciones y preferencias.
  - **Radiobuttons agrupados:** Agrupación de botones de opción mutuamente excluyentes vinculados a una misma variable `StringVar`.
  - **Selectores modernos:** Desplegables de solo lectura con `ttk.Combobox` y selectores numéricos con rangos mínimos y máximos mediante `ttk.Spinbox`.
  - **Control deslizante `tk.Scale`:** Configuración de controles de rango continuo horizontal y vertical.
  - **Editor multilínea con barra de desplazamiento:** Acoplamiento bidireccional de `tk.Scrollbar` con `tk.Text` (`yscrollcommand` y `command=widget.yview`).
  - **Inspección de datos en tiempo real:** Uso de `.trace_add("write", callback)` en las variables de Tkinter para serializar y renderizar automáticamente un panel JSON dinámico conforme el usuario interactúa.
* **Cómo ejecutarlo:**
  ```bash
  python 03_widgets_interactivos_formulario.py
  ```

---

### `04_canvas_y_dibujo_grafico.py`

* **Propósito:** Demostrar las capacidades gráficas vectoriales del widget `Canvas`: dibujo de primitivas, pizarras interactivas y animaciones fluidas.
* **Nivel:** Intermedio.
* **Widgets Utilizados:** `tk.Canvas`, `ttk.Notebook`, `tk.Scale`, `tk.Button`, `tk.Frame`.
* **Conceptos Clave Explicados:**
  - **Primitivas vectoriales 2D:** Creación de líneas rectas y flechas (`create_line`), rectángulos y cuadrados (`create_rectangle`), círculos y elipses (`create_oval`), polígonos irregulares (`create_polygon`), arcos y sectores circulares (`create_arc`) y texto tipográfico (`create_text`).
  - **Generación de gráficos estadísticos:** Dibujo manual de un diagrama de barras proporcional utilizando únicamente matemáticas vectoriales de Canvas.
  - **Pizarra de dibujo libre:** Captura de eventos de ratón (`<Button-1>`, `<B1-Motion>`, `<ButtonRelease-1>`) para crear trazos curvos y continuos con selector de paleta de colores y grosor dinámico de pincel.
  - **Motor de animación a 60 FPS con `.after()`:** Implementación de un bucle de animación sin bloquear el hilo de la interfaz mediante `root.after(16, self._paso)`.
  - **Física de rebote:** Detección de colisiones contra los bordes del lienzo y actualización dinámica de coordenadas con `canvas.coords()` y colores con `canvas.itemconfig()`.
* **Cómo ejecutarlo:**
  ```bash
  python 04_canvas_y_dibujo_grafico.py
  ```

---

### `05_dialogos_ventanas_secundarias.py`

* **Propósito:** Gestionar la interacción con el sistema operativo y el flujo de trabajo mediante cuadros de diálogo nativos y ventanas emergentes personalizadas.
* **Nivel:** Intermedio.
* **Widgets Utilizados:** `tk.Toplevel`, `tkinter.messagebox`, `tkinter.filedialog`, `tkinter.colorchooser`, `tkinter.simpledialog`.
* **Conceptos Clave Explicados:**
  - **Ventanas secundarias modales (`tk.Toplevel`):** Creación de ventanas hijas que bloquean la interacción con la ventana padre mediante `.transient(parent)` y `.grab_set()`.
  - **Retorno de datos entre ventanas:** Paso de callbacks y actualización de estados desde la ventana hija hacia la ventana principal.
  - **Alertas nativas (`messagebox`):** Notificaciones informativas (`showinfo`), de advertencia (`showwarning`), de error (`showerror`) y diálogos de decisión (`askyesno`, `askokcancel`).
  - **Explorador de archivos nativo (`filedialog`):** Apertura de archivos individuales con filtros de extensión (`askopenfilename`), guardado de archivos (`asksaveasfilename`) y selección de directorios (`askdirectory`).
  - **Paleta de colores (`colorchooser.askcolor`):** Invocación del selector de color nativo del sistema operativo y extracción de códigos HEX y tuplas RGB.
  - **Entradas directas (`simpledialog`):** Diálogos preconstruidos para solicitar cadenas (`askstring`) y números (`askinteger`).
* **Cómo ejecutarlo:**
  ```bash
  python 05_dialogos_ventanas_secundarias.py
  ```

---

### `06_menus_eventos_y_atajos.py`

* **Propósito:** Implementar barras de menús completas, menús emergentes de clic derecho, atajos de teclado globales y sistema de eventos.
* **Nivel:** Intermedio.
* **Widgets Utilizados:** `tk.Menu`, `tk.Text`, `tk.Label`, `tk.Frame`.
* **Conceptos Clave Explicados:**
  - **Barra de menú superior:** Construcción de menús en cascada (`Archivo`, `Edición`, `Ver`, `Ayuda`) utilizando `tk.Menu(root)` y asignación con `root.config(menu=barra_menu)`.
  - **Opciones avanzadas en menús:** Inserción de líneas divisorias (`add_separator`), casillas de verificación (`add_checkbutton`) y grupos de opciones excluyentes (`add_radiobutton`).
  - **Aceleradores de teclado visuales:** Configuración del atributo `accelerator="Ctrl+S"` para mostrar atajos en los menús.
  - **Menú contextual emergente (Popup Menu):** Despliegue de menús al presionar clic derecho mediante `<Button-3>` y el método `.tk_popup(x, y)`.
  - **Sistema de enlace de eventos (`.bind()`):**
    * Atajos de teclado: `<Control-n>`, `<Control-s>`, `<Control-q>`.
    * Eventos del ratón: `<Enter>`, `<Leave>`, `<Motion>`.
  - **Barra de estado (Status Bar):** Actualización en vivo de información de coordenadas del cursor y estado de operaciones.
* **Cómo ejecutarlo:**
  ```bash
  python 06_menus_eventos_y_atajos.py
  ```

---

### `07_estilos_modernos_ttk.py`

* **Propósito:** Dominar el subsistema de estilos avanzados `ttk.Style` para modernizar el aspecto visual de las aplicaciones Tkinter.
* **Nivel:** Avanzado.
* **Widgets Utilizados:** `ttk.Style`, `ttk.Notebook`, `ttk.Progressbar`, `ttk.Separator`, `ttk.Sizegrip`, `ttk.LabelFrame`, `ttk.Button`, `ttk.Combobox`.
* **Conceptos Clave Explicados:**
  - **Arquitectura de estilos de `ttk`:** Separación entre la lógica del widget y su presentación visual (análogo a CSS en desarrollo web).
  - **Explorador y selector de temas del sistema:** Alternancia en caliente entre temas incorporados (`'clam'`, `'alt'`, `'default'`, `'classic'`).
  - **Creación de clases de estilo personalizadas:** Configuración de propiedades visuales con `style.configure()` y mapeo de estados dinámicos (hover, active, disabled) con `style.map()`.
  - **Barras de progreso (`ttk.Progressbar`):**
    * Modo **determinado**: Avance porcentual controlado por variables numéricas.
    * Modo **indeterminado**: Efecto de carga continua o "spinner" para procesos de duración desconocida.
  - **Comparativa directa:** Vista en paralelo que compara widgets tradicionales del módulo `tk` frente a los widgets temáticos de `ttk`.
* **Cómo ejecutarlo:**
  ```bash
  python 07_estilos_modernos_ttk.py
  ```

---

### `08_tablas_y_jerarquias_treeview.py`

* **Propósito:** Mostrar cómo presentar y manipular grandes volúmenes de datos tabulares y estructuras jerárquicas con `ttk.Treeview`.
* **Nivel:** Avanzado.
* **Widgets Utilizados:** `ttk.Treeview`, `ttk.Scrollbar`, `tk.Entry`, `tk.Button`, `tk.Toplevel`.
* **Conceptos Clave Explicados:**
  - **Modo Tabla Tabular:** Configuración de columnas nombradas, anchos fijos o proporcionales, encabezados (`headings`) y alineación de texto a la izquierda, centro o derecha.
  - **Operaciones CRUD:** Flujo completo para **C**rear registros con diálogos modales, **L**eer y visualizar, **U**pdate (editar fila al hacer doble clic) y **D**elete (eliminar registros seleccionados con confirmación).
  - **Ordenamiento interactivo por columnas:** Detección de clics en los encabezados para ordenar datos alfabética o numéricamente en orden ascendente y descendente (indicado con flechas ▲/▼).
  - **Buscador y filtrado en tiempo real:** Filtrado instantáneo de filas conforme el usuario escribe en un campo de búsqueda.
  - **Filas alternadas (Zebra Striping):** Uso de `tag_configure()` para colorear filas pares e impares y mejorar la legibilidad.
  - **Modo Árbol Jerárquico:** Configuración de la columna especial `#0` para representar estructuras de árbol tipo explorador de archivos con carpetas, subcarpetas y elementos expandibles/colapsables.
* **Cómo ejecutarlo:**
  ```bash
  python 08_tablas_y_jerarquias_treeview.py
  ```

---

### `09_multihilo_y_tareas_en_segundo_plano.py`

* **Propósito:** Resolver de forma definitiva el problema de congelamiento de la interfaz de usuario al ejecutar tareas lentas o que consumen mucho tiempo.
* **Nivel:** Avanzado.
* **Widgets Utilizados:** `ttk.Progressbar`, `tk.Canvas`, `tk.Text`, `tk.Button`, `tk.Label`.
* **Conceptos Clave Explicados:**
  - **El problema del hilo único en interfaces gráficas:** Por qué operaciones de red, cálculos pesados o bucles lentos en el hilo principal bloquean `root.mainloop()` e impiden procesar eventos de ratón, teclado y repintado de pantalla.
  - **La solución profesional:** Uso de hilos en segundo plano con `threading.Thread(target=..., daemon=True)`.
  - **Regla crítica de seguridad en hilos:** Por qué los hilos secundarios **nunca deben modificar directamente los widgets de Tkinter** (evitar condiciones de carrera y fallos de segmentación en Tcl/Tk).
  - **Paso de mensajes seguro con `queue.Queue`:** Envío de paquetes de datos y estados desde el hilo secundario hacia una cola de mensajes en memoria.
  - **Polling periódico con `root.after()`:** Monitoreo regular y no bloqueante de la cola desde el hilo principal para actualizar barras de progreso y bitácoras de texto.
  - **Demostración interactiva en vivo:** Comparación directa entre un botón que congela la ventana y un botón multihilo que mantiene un testigo giratorio a 60 FPS sin interrupciones, con soporte para cancelación de tareas.
* **Cómo ejecutarlo:**
  ```bash
  python 09_multihilo_y_tareas_en_segundo_plano.py
  ```

---

### `10_proyecto_integrador_gestor_tareas.py`

* **Propósito:** Proyecto final integrador que reúne todas las técnicas vistas en una aplicación completa, profesional y modular: **TaskFlow Pro**.
* **Nivel:** Proyecto Completo.
* **Widgets Utilizados:** `tk.Tk`, `ttk.Treeview`, `tk.Canvas`, `ttk.Notebook`, `tk.Menu`, `tk.Toplevel`, `ttk.Combobox`, `tk.Entry`, `tk.Text`.
* **Conceptos Clave Explicados:**
  - **Arquitectura Orientada a Objetos (POO):** Separación limpia entre modelo de datos (`Tarea`), persistencia y controlador de interfaz gráfica.
  - **Persistencia local en formato JSON:** Carga automática y guardado persistente de las tareas en un archivo local `tareas.json`.
  - **Dashboard con gráfico Donut Chart vectorial:** Dibujo dinámico de un gráfico circular en `tk.Canvas` que calcula en tiempo real el porcentaje de tareas completadas.
  - **Tarjetas métricas superiores:** Contadores visuales de tareas totales, pendientes, en progreso y completadas.
  - **Filtros por estado y buscador integrado:** Pestañas de filtrado rápido combinadas con un buscador por texto que filtra título, categoría o descripción.
  - **Formularios modales avanzados:** Ventanas `Toplevel` para agregar y editar tareas con validación de campos obligatorios.
  - **Importación y Exportación:** Menú para exportar e importar datos desde archivos JSON externos seleccionados mediante `filedialog`.
  - **Atajos de productividad:** Combinaciones de teclas para crear tareas (`Ctrl+N`), alternar estado completada (`Ctrl+D`) y eliminar (`Supr`).
* **Cómo ejecutarlo:**
  ```bash
  python 10_proyecto_integrador_gestor_tareas.py
  ```

---

## 💻 Requisitos e Instalación

### 1. Requisitos
- **Python 3.8** o superior instalado en el sistema.
- **Tkinter** habilitado en la instalación de Python.

### 2. Verificación de Tkinter
Puedes comprobar que tu entorno cuenta con soporte para Tkinter ejecutando este comando en tu terminal:

```bash
python -m tkinter
```
*Si se abre una pequeña ventana con el título "tk" y dos botones, tu instalación está lista.*

### 3. Instalación de Tkinter en Linux (si es necesario)
En sistemas operativos basados en Debian/Ubuntu, Tkinter puede requerir la instalación de su paquete nativo:
```bash
sudo apt update
sudo apt install -y python3-tk
```
*(En Windows y macOS no es necesario, ya que el instalador oficial de [python.org](https://www.python.org/) lo incluye por defecto).*

---

## 🌐 Cómo Publicar este Repositorio en GitHub

Si deseas publicar este repositorio en tu cuenta personal de GitHub, sigue estos sencillos pasos:

### Opción A: Usando la terminal con Git (Recomendado)

1. **Abre tu terminal o consola (PowerShell / Bash) dentro de esta carpeta:**
   ```bash
   cd ruta/al/proyecto/tkinter-showcase
   ```

2. **Inicializa el repositorio Git local:**
   ```bash
   git init
   ```

3. **Agrega todos los archivos al seguimiento:**
   ```bash
   git add .
   ```

4. **Realiza tu primer commit:**
   ```bash
   git commit -m "feat: commit inicial con los 10 módulos didácticos y documentación de Tkinter"
   ```

5. **Crea un nuevo repositorio en GitHub:**
   - Ve a [github.com/new](https://github.com/new).
   - Asigna un nombre a tu repositorio (por ejemplo: `tkinter-python-showcase`).
   - Deja el repositorio **vacío** (no agregues README ni .gitignore adicionales, ya están incluidos aquí).

6. **Vincula tu repositorio local con GitHub y sube los cambios:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/tkinter-python-showcase.git
   git push -u origin main
   ```

---

### Opción B: Usando GitHub Desktop

1. Abre **GitHub Desktop**.
2. Ve al menú superior y selecciona **File > Add Local Repository...**
3. Elige la carpeta donde se encuentra este proyecto.
4. Si te indica que no es un repositorio Git, haz clic en **Create a repository**.
5. Haz clic en **Publish repository** para subirlo directamente a tu cuenta de GitHub.

---

### Opción C: Subida directa mediante la Web de GitHub

1. Crea un nuevo repositorio en [github.com/new](https://github.com/new).
2. En la pantalla principal del repositorio vacío, haz clic en **"uploading an existing file"** (subir archivos existentes).
3. Arrastra todos los archivos de esta carpeta hacia el navegador.
4. Escribe un mensaje de commit (por ejemplo, `Primer commit`) y haz clic en **Commit changes**.

---

## 💡 Buenas Prácticas en Tkinter

1. **Estructura en Clases (POO):** Encapsula tus ventanas en clases de Python para mantener el estado de los widgets limpio y evitar el uso de variables globales `global`.
2. **Nunca mezcles gestores:** No utilices `pack()` y `grid()` sobre el mismo contenedor o `Frame` padre.
3. **Usa `ttk` para interfaces modernas:** Prefiere siempre los widgets de `tkinter.ttk` por encima de los widgets clásicos de `tk` para lograr un acabado visual nativo y profesional.
4. **No bloquees el hilo principal:** Para peticiones HTTP, accesos a bases de datos o cálculos que tomen más de 50 milisegundos, utiliza hilos secundarios (`threading.Thread`) y comunica los cambios a la GUI a través de colas (`queue.Queue`) y `root.after()`.
5. **Gestiona el ciclo de vida:** Libera recursos, detiene hilos trabajadores y cierra ventanas secundarias de manera explícita usando el protocolo `WM_DELETE_WINDOW`:
   ```python
   root.protocol("WM_DELETE_WINDOW", self.al_cerrar)
   ```

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles. Puedes utilizar, modificar y compartir este código libremente tanto en proyectos educativos como comerciales.
