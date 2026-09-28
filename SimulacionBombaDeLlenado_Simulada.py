import tkinter as tk
from tkinter import messagebox, ttk


CAPACIDAD_ML = 1000
VOLUMEN_MINIMO_ML = 200
VOLUMEN_MAXIMO_ML = 800
PASO_TRANSFERENCIA_ML = 10
INTERVALO_MS = 100


class SimuladorBombasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Transferencia entre Tanques")
        self.root.geometry("900x760")
        self.root.minsize(760, 680)
        self.root.configure(bg="#121212")
        self.root.resizable(True, True)

        self.nivel_a_ml = 500
        self.nivel_b_ml = 500
        self.direccion = 0
        self.simulacion_activa = False
        self.interruptor_a = 0
        self.interruptor_b = 0
        self.ciclo_programado = False
        self.normalizacion_activa = False
        self.accion_pendiente = None
        self.objetivo_normalizacion_ml = None

        self.nivel_a_var = tk.StringVar()
        self.nivel_b_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Sistema detenido")

        self.crear_interfaz()
        self.actualizar_interfaz()

    def crear_interfaz(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#121212")
        style.configure(
            "TLabel",
            background="#121212",
            foreground="#ffffff",
            font=("Segoe UI", 11),
        )
        style.configure(
            "TLabelframe",
            background="#121212",
            foreground="#ffffff",
        )
        style.configure(
            "TLabelframe.Label",
            background="#121212",
            foreground="#ffb000",
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Green.TButton",
            background="#2e7d32",
            foreground="white",
            font=("Segoe UI", 11, "bold"),
        )
        style.map("Green.TButton", background=[("active", "#388e3c")])
        style.configure(
            "Red.TButton",
            background="#8b0000",
            foreground="white",
            font=("Segoe UI", 11, "bold"),
        )
        style.map("Red.TButton", background=[("active", "#a50000")])
        style.configure(
            "Gray.TButton",
            background="#424242",
            foreground="white",
            font=("Segoe UI", 11, "bold"),
        )
        style.map("Gray.TButton", background=[("active", "#616161")])
        style.configure(
            "Manual.TButton",
            background="#996c00",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Manual.TButton", background=[("active", "#bd8800")])

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        contenido_frame = ttk.Frame(main_frame)
        contenido_frame.grid(row=0, column=0, sticky="nsew")
        contenido_frame.columnconfigure(0, weight=1)
        contenido_frame.rowconfigure(0, weight=1)
        contenido_frame.rowconfigure(1, weight=0)
        contenido_frame.rowconfigure(2, weight=0)
        contenido_frame.rowconfigure(3, weight=0)

        tanque_frame = ttk.LabelFrame(
            contenido_frame,
            text="NIVEL DE LIQUIDO - CAPACIDAD: 1000 ML POR TANQUE",
            padding=15,
        )
        tanque_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        tanque_frame.columnconfigure(0, weight=1)

        depositos_frame = ttk.Frame(tanque_frame)
        depositos_frame.pack(fill=tk.BOTH, expand=True)
        depositos_frame.columnconfigure(0, weight=1)
        depositos_frame.columnconfigure(1, weight=1)

        tanque_a_frame, self.canvas_a, self.agua_a, self.led_a, self.estado_a_var = self.crear_tanque(
            depositos_frame, "DEPOSITO A", "#1a6dff"
        )
        tanque_a_frame.grid(row=0, column=0, padx=25, sticky="nsew")

        tanque_b_frame, self.canvas_b, self.agua_b, self.led_b, self.estado_b_var = self.crear_tanque(
            depositos_frame, "DEPOSITO B", "#21a366"
        )
        tanque_b_frame.grid(row=0, column=1, padx=25, sticky="nsew")

        niveles_frame = ttk.Frame(tanque_frame)
        niveles_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(
            niveles_frame,
            textvariable=self.nivel_a_var,
            font=("Segoe UI", 14, "bold"),
            foreground="#5ca9ff",
        ).pack(side=tk.LEFT, expand=True)
        ttk.Label(
            niveles_frame,
            textvariable=self.nivel_b_var,
            font=("Segoe UI", 14, "bold"),
            foreground="#55d98b",
        ).pack(side=tk.LEFT, expand=True)

        control_frame = ttk.LabelFrame(
            contenido_frame,
            text="CONTROL DE TRANSFERENCIA",
            padding=15,
        )
        control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        control_frame.columnconfigure(0, weight=1)

        ttk.Button(
            control_frame,
            text="LLENAR DEPOSITO A",
            style="Green.TButton",
            command=self.empezar_llenado,
        ).pack(fill=tk.X, pady=5)
        ttk.Button(
            control_frame,
            text="VACIAR DEPOSITO A",
            style="Red.TButton",
            command=self.empezar_vaciado,
        ).pack(fill=tk.X, pady=5)
        ttk.Button(
            control_frame,
            text="DETENER SISTEMA",
            style="Gray.TButton",
            command=self.detener_simulacion,
        ).pack(fill=tk.X, pady=5)

        manual_frame = ttk.LabelFrame(
            contenido_frame,
            text="INTERRUPTORES MANUALES",
            padding=12,
        )
        manual_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        manual_frame.columnconfigure(0, weight=1)
        manual_frame.columnconfigure(1, weight=1)

        self.crear_control_manual(
            manual_frame,
            0,
            "DEPOSITO A",
            self.activar_llenado_manual_a,
            self.activar_vaciado_manual_a,
        )
        self.crear_control_manual(
            manual_frame,
            1,
            "DEPOSITO B",
            self.activar_llenado_manual_b,
            self.activar_vaciado_manual_b,
        )

        ttk.Label(
            contenido_frame,
            textvariable=self.estado_var,
            font=("Segoe UI", 12, "bold"),
            foreground="#ffb000",
        ).grid(row=3, column=0, sticky="ew", pady=5)

        ttk.Label(
            contenido_frame,
            text="Practica 3 Simulación de un Sistema de Control",
            foreground="#aaaaaa",
        ).grid(row=4, column=0, sticky="ew")

    def crear_control_manual(self, parent, columna, titulo, comando_llenar, comando_vaciar):
        frame = ttk.Frame(parent, padding=5)
        frame.grid(row=0, column=columna, sticky="ew")
        frame.columnconfigure(0, weight=1)

        ttk.Label(
            frame,
            text=titulo,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        llenar = tk.Button(
            frame,
            text="LLENADO MANUAL",
            command=comando_llenar,
            bg="#996c00",
            activebackground="#bd8800",
            fg="white",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        llenar.grid(row=1, column=0, sticky="ew", pady=3)

        vaciar = tk.Button(
            frame,
            text="VACIADO MANUAL",
            command=comando_vaciar,
            bg="#996c00",
            activebackground="#bd8800",
            fg="white",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        vaciar.grid(row=2, column=0, sticky="ew", pady=3)

        if columna == 0:
            self.llenar_a_button = llenar
            self.vaciar_a_button = vaciar
        else:
            self.llenar_b_button = llenar
            self.vaciar_b_button = vaciar

    def crear_tanque(self, parent, titulo, color):
        frame = ttk.Frame(parent)
        ttk.Label(
            frame,
            text=titulo,
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 5))

        canvas = tk.Canvas(
            frame,
            width=150,
            height=240,
            bg="#1e1e1e",
            highlightthickness=2,
            highlightbackground="#444444",
        )
        canvas.pack()
        canvas.create_rectangle(10, 10, 140, 230, outline="#777777", width=2, fill="#0a0a0a")
        agua = canvas.create_rectangle(12, 120, 138, 228, fill=color, outline="")

        for y in (65, 120, 175):
            canvas.create_line(10, y, 140, y, dash=(2, 4), fill="#333333")

        estado_frame = ttk.Frame(frame)
        estado_frame.pack(fill=tk.X, pady=(7, 0))
        led = tk.Canvas(
            estado_frame,
            width=28,
            height=28,
            bg="#121212",
            highlightthickness=0,
        )
        led.pack(side=tk.LEFT, padx=(8, 5))
        led.create_oval(5, 5, 23, 23, fill="#d18b00", outline="#777777")
        estado_var = tk.StringVar(value="NIVEL INTERMEDIO")
        ttk.Label(
            estado_frame,
            textvariable=estado_var,
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT)

        return frame, canvas, agua, led, estado_var

    def empezar_llenado(self):
        if not self.confirmar_rango_operativo(1):
            return
        self.interruptor_a = 0
        self.interruptor_b = 0
        self.direccion = 1
        self.simulacion_activa = True
        self.estado_var.set("Bomba de llenado activa: A recibe liquido de B")
        self.actualizar_interruptores()
        self.ejecutar_simulacion()

    def empezar_vaciado(self):
        if not self.confirmar_rango_operativo(-1):
            return
        self.interruptor_a = 0
        self.interruptor_b = 0
        self.direccion = -1
        self.simulacion_activa = True
        self.estado_var.set("Bomba de vaciado activa: A envia liquido hacia B")
        self.actualizar_interruptores()
        self.ejecutar_simulacion()

    def confirmar_rango_operativo(self, accion_direccion):
        if VOLUMEN_MINIMO_ML <= self.nivel_a_ml <= VOLUMEN_MAXIMO_ML:
            return True

        nivel_porcentaje = self.nivel_a_ml / CAPACIDAD_ML * 100
        if self.nivel_a_ml > VOLUMEN_MAXIMO_ML:
            mensaje = (
                "El deposito A se encuentra al {:.0f}% ({} ml).\n\n"
                "El nivel maximo operativo es 80% (800 ml).\n"
                "¿Desea transferir el excedente al deposito B?"
            ).format(nivel_porcentaje, self.nivel_a_ml)
            nivel_objetivo = VOLUMEN_MAXIMO_ML
        else:
            mensaje = (
                "El deposito A se encuentra al {:.0f}% ({} ml).\n\n"
                "El nivel minimo operativo es 20% (200 ml).\n"
                "¿Desea transferir liquido desde el deposito B?"
            ).format(nivel_porcentaje, self.nivel_a_ml)
            nivel_objetivo = VOLUMEN_MINIMO_ML

        respuesta = messagebox.askyesnocancel(
            "Nivel fuera del rango operativo",
            mensaje,
            parent=self.root,
        )
        if respuesta is True:
            self.normalizacion_activa = True
            self.objetivo_normalizacion_ml = nivel_objetivo
            self.accion_pendiente = accion_direccion
            self.estado_var.set("Transfiriendo liquido al rango operativo...")
            self.ejecutar_simulacion()
            return False

        self.estado_var.set("Operacion no ejecutada")
        return False

    def detener_simulacion(self):
        self.direccion = 0
        self.simulacion_activa = False
        self.interruptor_a = 0
        self.interruptor_b = 0
        self.normalizacion_activa = False
        self.accion_pendiente = None
        self.objetivo_normalizacion_ml = None
        self.actualizar_interruptores()
        self.estado_var.set("Sistema detenido")

    def activar_llenado_manual_a(self):
        self.activar_interruptor_manual("a", 1)

    def activar_vaciado_manual_a(self):
        self.activar_interruptor_manual("a", -1)

    def activar_llenado_manual_b(self):
        self.activar_interruptor_manual("b", 1)

    def activar_vaciado_manual_b(self):
        self.activar_interruptor_manual("b", -1)

    def activar_interruptor_manual(self, deposito, direccion):
        self.direccion = 0
        self.simulacion_activa = False
        if deposito == "a":
            self.interruptor_a = 0 if self.interruptor_a == direccion else direccion
            self.interruptor_b = 0
            deposito_texto = "A"
        else:
            self.interruptor_b = 0 if self.interruptor_b == direccion else direccion
            self.interruptor_a = 0
            deposito_texto = "B"

        if direccion == 1:
            accion = "llenando"
        else:
            accion = "vaciando"
        if self.interruptor_a == 0 and self.interruptor_b == 0:
            self.estado_var.set("Sistema detenido")
        else:
            self.estado_var.set("Control manual activo: {} {}".format(deposito_texto, accion))
        self.actualizar_interruptores()
        self.ejecutar_simulacion()

    def actualizar_interruptores(self):
        botones = (
            (self.llenar_a_button, self.interruptor_a == 1),
            (self.vaciar_a_button, self.interruptor_a == -1),
            (self.llenar_b_button, self.interruptor_b == 1),
            (self.vaciar_b_button, self.interruptor_b == -1),
        )
        for boton, activo in botones:
            boton.configure(
                bg="#2e7d32" if activo else "#996c00",
                relief=tk.SUNKEN if activo else tk.RAISED,
            )

    def ejecutar_simulacion(self):
        if self.ciclo_programado:
            return

        if (
            not self.simulacion_activa
            and not self.normalizacion_activa
            and self.interruptor_a == 0
            and self.interruptor_b == 0
        ):
            return

        self.ciclo_programado = True
        self.root.after(INTERVALO_MS, self.actualizar_niveles)

    def actualizar_niveles(self):
        self.ciclo_programado = False
        if (
            not self.simulacion_activa
            and not self.normalizacion_activa
            and self.interruptor_a == 0
            and self.interruptor_b == 0
        ):
            return

        if self.normalizacion_activa:
            diferencia_ml = self.objetivo_normalizacion_ml - self.nivel_a_ml
            cambio_ml = max(
                -PASO_TRANSFERENCIA_ML,
                min(PASO_TRANSFERENCIA_ML, diferencia_ml),
            )
            self.nivel_a_ml += cambio_ml
            self.nivel_b_ml = CAPACIDAD_ML - self.nivel_a_ml
            self.actualizar_interfaz()

            if self.nivel_a_ml == self.objetivo_normalizacion_ml:
                self.normalizacion_activa = False
                accion_pendiente = self.accion_pendiente
                self.accion_pendiente = None
                self.objetivo_normalizacion_ml = None
                if accion_pendiente is not None:
                    self.direccion = accion_pendiente
                    self.simulacion_activa = True
                    self.estado_var.set("Bomba autorizada: transferencia en curso")
                else:
                    self.estado_var.set("Rango operativo alcanzado")
            self.ejecutar_simulacion()
            return

        if self.interruptor_a != 0:
            self.nivel_a_ml += PASO_TRANSFERENCIA_ML * self.interruptor_a
            self.nivel_a_ml = max(0, min(CAPACIDAD_ML, self.nivel_a_ml))
            self.nivel_b_ml = CAPACIDAD_ML - self.nivel_a_ml
        elif self.interruptor_b != 0:
            self.nivel_b_ml += PASO_TRANSFERENCIA_ML * self.interruptor_b
            self.nivel_b_ml = max(0, min(CAPACIDAD_ML, self.nivel_b_ml))
            self.nivel_a_ml = CAPACIDAD_ML - self.nivel_b_ml
        elif self.simulacion_activa:
            nuevo_nivel_a_ml = self.nivel_a_ml + (PASO_TRANSFERENCIA_ML * self.direccion)
            self.nivel_a_ml = max(
                VOLUMEN_MINIMO_ML,
                min(VOLUMEN_MAXIMO_ML, nuevo_nivel_a_ml),
            )
            self.nivel_b_ml = CAPACIDAD_ML - self.nivel_a_ml

        self.actualizar_interfaz()

        transferencia_terminada = (
            self.simulacion_activa
            and self.nivel_a_ml in (VOLUMEN_MINIMO_ML, VOLUMEN_MAXIMO_ML)
        )
        manual_terminado = (
            self.interruptor_a == 1 and self.nivel_a_ml == CAPACIDAD_ML
        ) or (
            self.interruptor_a == -1 and self.nivel_a_ml == 0
        ) or (
            self.interruptor_b == 1 and self.nivel_b_ml == CAPACIDAD_ML
        ) or (
            self.interruptor_b == -1 and self.nivel_b_ml == 0
        )

        if transferencia_terminada or manual_terminado:
            self.detener_simulacion()
            self.estado_var.set(
                "Limite alcanzado: A={} ml / B={} ml".format(
                    self.nivel_a_ml, self.nivel_b_ml
                )
            )
            return

        self.ejecutar_simulacion()

    def actualizar_interfaz(self):
        self.nivel_a_var.set(
            "Deposito A: {} ml / {} ml ({:.0f}%)".format(
                self.nivel_a_ml,
                CAPACIDAD_ML,
                self.nivel_a_ml / CAPACIDAD_ML * 100,
            )
        )
        self.nivel_b_var.set(
            "Deposito B: {} ml / {} ml ({:.0f}%)".format(
                self.nivel_b_ml,
                CAPACIDAD_ML,
                self.nivel_b_ml / CAPACIDAD_ML * 100,
            )
        )
        self.actualizar_tanque(self.canvas_a, self.agua_a, self.nivel_a_ml, "#1a6dff")
        self.actualizar_tanque(self.canvas_b, self.agua_b, self.nivel_b_ml, "#21a366")
        self.actualizar_led(self.led_a, self.estado_a_var, self.nivel_a_ml)
        self.actualizar_led(self.led_b, self.estado_b_var, self.nivel_b_ml)

    def actualizar_tanque(self, canvas, agua, nivel, color):
        y_bottom = 228
        altura_agua = (nivel / CAPACIDAD_ML) * 216
        y_top = y_bottom - altura_agua
        canvas.coords(agua, 12, y_top, 138, y_bottom)
        canvas.itemconfig(agua, fill=color)

    def actualizar_led(self, led, estado_var, nivel_ml):
        nivel_porcentaje = nivel_ml / CAPACIDAD_ML * 100
        if nivel_porcentaje >= 80:
            color = "#33cc33"
            estado = "LLENO"
        elif nivel_porcentaje >= 30:
            color = "#d18b00"
            estado = "NIVEL INTERMEDIO"
        elif nivel_porcentaje > 20:
            color = "#ff7f27"
            estado = "NIVEL BAJO"
        else:
            color = "#e53935"
            estado = "VACIO"
        led.delete("all")
        led.create_oval(5, 5, 23, 23, fill=color, outline="#777777")
        estado_var.set(estado)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorBombasApp(root)
    root.mainloop()
    
