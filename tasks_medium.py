import tkinter as tk
from tkinter import ttk, messagebox
import random


class CalculatorFrame(ttk.Frame):
    """Средняя сложность  3: ростейший калькулятор."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=12)
        self._build_ui()

    def _build_ui(self) -> None:
        title = ttk.Label(self, text="алькулятор двух чисел", font=("Segoe UI", 11, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(self, text="исло A:").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_a = ttk.Entry(self, width=18)
        self.entry_a.grid(row=1, column=1, pady=4)

        ttk.Label(self, text="исло B:").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_b = ttk.Entry(self, width=18)
        self.entry_b.grid(row=2, column=1, pady=4)

        btn_box = ttk.Frame(self)
        btn_box.grid(row=3, column=0, columnspan=2, pady=8)

        ttk.Button(btn_box, text="+", width=4, command=lambda: self._calc("+")).pack(side="left", padx=2)
        ttk.Button(btn_box, text="-", width=4, command=lambda: self._calc("-")).pack(side="left", padx=2)
        ttk.Button(btn_box, text="*", width=4, command=lambda: self._calc("*")).pack(side="left", padx=2)
        ttk.Button(btn_box, text="/", width=4, command=lambda: self._calc("/")).pack(side="left", padx=2)

        self.lbl_result = ttk.Label(self, text="езультат: --", font=("Segoe UI", 10, "bold"))
        self.lbl_result.grid(row=4, column=0, columnspan=2, pady=(6, 0))

    def _calc(self, op: str) -> None:
        try:
            val_a = float(self.entry_a.get().strip().replace(",", "."))
            val_b = float(self.entry_b.get().strip().replace(",", "."))
            if op == "+":
                res = val_a + val_b
            elif op == "-":
                res = val_a - val_b
            elif op == "*":
                res = val_a * val_b
            elif op == "/":
                if val_b == 0:
                    raise ZeroDivisionError("еление на ноль невозможно.")
                res = val_a / val_b
            else:
                return
            self.lbl_result.config(text=f"езультат: {res:g}")
        except ValueError:
            messagebox.showerror("шибка ввода", "ведите корректные числовые значения в поля A и B.")
        except ZeroDivisionError as err:
            messagebox.showwarning("шибка вычисления", str(err))


class ColorPanelFrame(ttk.Frame):
    """Средняя сложность  9: ветная панель, меняющая цвет по кнопке."""

    PALETTE = ("#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7D794", "#786FA6")

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=12)
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Label(self, text="нтерактивная панель цветов", font=("Segoe UI", 11, "bold"))
        header.pack(pady=(0, 8))

        self.color_canvas = tk.Canvas(self, width=280, height=130, bg="#4ECDC4", relief="groove", bd=2)
        self.color_canvas.pack(pady=6)

        self.lbl_code = ttk.Label(self, text="Текущий цвет: #4ECDC4", font=("Segoe UI", 10))
        self.lbl_code.pack(pady=4)

        btn = ttk.Button(self, text="Сменить цвет", command=self.change_color)
        btn.pack(pady=6)

    def change_color(self) -> None:
        current_color = self.color_canvas.cget("bg")
        candidates = [c for c in self.PALETTE if c.lower() != current_color.lower()]
        new_color = random.choice(candidates)
        self.color_canvas.config(bg=new_color)
        self.lbl_code.config(text=f"Текущий цвет: {new_color}")
