#!/usr/bin/env python3
"""
Simulación sencilla de la mitosis de dos células.

Muestra de forma animada las etapas principales:
Interfase, Profase, Metafase, Anafase, Telofase y Citocinesis.
Al finalizar, cada una de las dos células iniciales se divide en dos (4 células en total).
"""

import tkinter as tk


class Celula:
    def __init__(self, canvas, cx, cy, r, color="#7ec8e3", borde="#2b6f8a"):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.r = r
        self.color = color
        self.borde = borde

        # Elementos gráficos
        self.cuerpo = canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill=color, outline=borde, width=3
        )
        self.nucleo = canvas.create_oval(
            cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45,
            fill="#f7d774", outline="#b08900", width=2
        )
        # Cromosomas representados como líneas (se ocultan/muestran según la fase)
        self.cromosomas = []
        self._crear_cromosomas()

    def _crear_cromosomas(self):
        offsets = [(-10, -6), (10, -6), (-10, 6), (10, 6)]
        for dx, dy in offsets:
            x1 = self.cx + dx - 6
            y1 = self.cy + dy
            x2 = self.cx + dx + 6
            y2 = self.cy + dy
            c = self.canvas.create_line(
                x1, y1, x2, y2, fill="#8b0000", width=4, state="hidden"
            )
            self.cromosomas.append(c)

    def mostrar_nucleo(self, visible=True):
        state = "normal" if visible else "hidden"
        self.canvas.itemconfigure(self.nucleo, state=state)

    def mostrar_cromosomas(self, visible=True):
        state = "normal" if visible else "hidden"
        for c in self.cromosomas:
            self.canvas.itemconfigure(c, state=state)

    def posicionar_cromosomas(self, fase, progreso=0.0):
        """Ajusta la posición de los cromosomas según la fase y el progreso (0..1)."""
        # posiciones base: centro
        if fase == "Profase":
            # Se condensan cerca del centro
            spread = 12 - 4 * progreso
            coords = [(-spread, -6), (spread, -6), (-spread, 6), (spread, 6)]
            for (dx, dy), c in zip(coords, self.cromosomas):
                self.canvas.coords(c, self.cx + dx - 6, self.cy + dy,
                                   self.cx + dx + 6, self.cy + dy)

        elif fase == "Metafase":
            # Alineados en el ecuador
            xs = [-18, -6, 6, 18]
            for x, c in zip(xs, self.cromosomas):
                self.canvas.coords(c, self.cx + x, self.cy - 8,
                                   self.cx + x, self.cy + 8)

        elif fase == "Anafase":
            # Se separan hacia los polos
            sep = 10 + 30 * progreso
            pares = [(-sep, -6), (-sep, 6), (sep, -6), (sep, 6)]
            for (dx, dy), c in zip(pares, self.cromosomas):
                self.canvas.coords(c, self.cx + dx - 5, self.cy + dy,
                                   self.cx + dx + 5, self.cy + dy)

        elif fase == "Telofase":
            # Dos grupos en polos opuestos
            sep = 35
            pares = [(-sep, -6), (-sep, 6), (sep, -6), (sep, 6)]
            for (dx, dy), c in zip(pares, self.cromosomas):
                self.canvas.coords(c, self.cx + dx - 5, self.cy + dy,
                                   self.cx + dx + 5, self.cy + dy)

    def estirar(self, progreso):
        """Estira la célula horizontalmente durante la citocinesis."""
        rx = self.r * (1 + 0.5 * progreso)
        ry = self.r * (1 - 0.2 * progreso)
        self.canvas.coords(self.cuerpo, self.cx - rx, self.cy - ry,
                           self.cx + rx, self.cy + ry)

    def borrar(self):
        self.canvas.delete(self.cuerpo)
        self.canvas.delete(self.nucleo)
        for c in self.cromosomas:
            self.canvas.delete(c)


class SimulacionMitosis:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de mitosis - 2 células")
        self.canvas = tk.Canvas(root, width=900, height=500, bg="#f4f7fb")
        self.canvas.pack()

        self.titulo = self.canvas.create_text(
            450, 30, text="Mitosis de dos células sencillas",
            font=("Helvetica", 20, "bold"), fill="#1f3b57"
        )
        self.fase_texto = self.canvas.create_text(
            450, 70, text="", font=("Helvetica", 16, "bold"), fill="#2b6f8a"
        )
        self.desc_texto = self.canvas.create_text(
            450, 100, text="", font=("Helvetica", 12), fill="#333333"
        )

        self.fases = [
            ("Interfase", "La célula crece y duplica su ADN. El núcleo es visible."),
            ("Profase", "La cromatina se condensa en cromosomas y el núcleo se desorganiza."),
            ("Metafase", "Los cromosomas se alinean en el ecuador de la célula."),
            ("Anafase", "Las cromátidas hermanas se separan hacia polos opuestos."),
            ("Telofase", "Se forman dos núcleos y los cromosomas se descondensan."),
            ("Citocinesis", "El citoplasma se divide: cada célula origina dos células hijas."),
        ]

        self.celulas = [
            Celula(self.canvas, 300, 280, 80),
            Celula(self.canvas, 600, 280, 80),
        ]
        self.celulas_hijas = []

        self.fase_idx = 0
        self.paso = 0
        self.pasos_por_fase = 40
        self.animando = True

        self.boton = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.boton.pack(pady=8)

        self.root.after(50, self.actualizar)

    def reiniciar(self):
        for c in self.celulas + self.celulas_hijas:
            c.borrar()
        self.celulas = [
            Celula(self.canvas, 300, 280, 80),
            Celula(self.canvas, 600, 280, 80),
        ]
        self.celulas_hijas = []
        self.fase_idx = 0
        self.paso = 0
        self.animando = True
        self.actualizar()

    def actualizar(self):
        if not self.animando:
            return

        if self.fase_idx >= len(self.fases):
            self.fase_texto_set("Resultado", "Se obtuvieron 4 células hijas a partir de las 2 iniciales.")
            self.animando = False
            return

        nombre, descripcion = self.fases[self.fase_idx]
        progreso = self.paso / self.pasos_por_fase
        self.fase_texto_set(nombre, descripcion)
        self.aplicar_fase(nombre, progreso)

        self.paso += 1
        if self.paso > self.pasos_por_fase:
            self.paso = 0
            # Al terminar citocinesis, crear células hijas y finalizar
            if nombre == "Citocinesis":
                self.crear_celulas_hijas()
                self.fase_idx += 1
                self.animando = False
                self.fase_texto_set(
                    "Resultado",
                    "Cada célula se dividió en dos: ahora hay 4 células hijas."
                )
                return
            self.fase_idx += 1

        self.root.after(80, self.actualizar)

    def fase_texto_set(self, fase, desc):
        self.canvas.itemconfigure(self.fase_texto, text=f"Fase: {fase}")
        self.canvas.itemconfigure(self.desc_texto, text=desc)

    def aplicar_fase(self, nombre, progreso):
        for celula in self.celulas:
            if nombre == "Interfase":
                celula.mostrar_nucleo(True)
                celula.mostrar_cromosomas(False)
            elif nombre == "Profase":
                celula.mostrar_nucleo(progreso < 0.5)
                celula.mostrar_cromosomas(True)
                celula.posicionar_cromosomas("Profase", progreso)
            elif nombre == "Metafase":
                celula.mostrar_nucleo(False)
                celula.mostrar_cromosomas(True)
                celula.posicionar_cromosomas("Metafase", progreso)
            elif nombre == "Anafase":
                celula.mostrar_nucleo(False)
                celula.mostrar_cromosomas(True)
                celula.posicionar_cromosomas("Anafase", progreso)
            elif nombre == "Telofase":
                celula.mostrar_nucleo(True)
                celula.mostrar_cromosomas(True)
                celula.posicionar_cromosomas("Telofase", progreso)
            elif nombre == "Citocinesis":
                celula.mostrar_nucleo(True)
                celula.mostrar_cromosomas(False)
                celula.estirar(progreso)

    def crear_celulas_hijas(self):
        # Reemplazar cada célula madre por dos hijas más pequeñas
        nuevas = []
        posiciones = []
        for celula in self.celulas:
            posiciones.append((celula.cx - 55, celula.cy))
            posiciones.append((celula.cx + 55, celula.cy))
            celula.borrar()
        self.celulas = []
        for (x, y) in posiciones:
            nuevas.append(Celula(self.canvas, x, y, 45, color="#9fd3a6", borde="#3f7a4a"))
        self.celulas_hijas = nuevas


def main():
    root = tk.Tk()
    SimulacionMitosis(root)
    root.mainloop()


if __name__ == "__main__":
    main()
