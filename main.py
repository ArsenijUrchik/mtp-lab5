import tkinter as tk
from tkinter import ttk
from tasks_medium import CalculatorFrame, ColorPanelFrame
from tasks_advanced import ClickerGameFrame, SQLiteManagerFrame


def create_application() -> tk.Tk:
    root = tk.Tk()
    root.title("абораторная работа  5 (ариант 3)")
    root.geometry("680x440")
    root.minsize(620, 380)

    # Средняя сложность  5: рограмма со вкладками (Notebook)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    tab_calc = CalculatorFrame(notebook)
    tab_color = ColorPanelFrame(notebook)
    tab_clicker = ClickerGameFrame(notebook)
    tab_db = SQLiteManagerFrame(notebook)

    notebook.add(tab_calc, text="алькулятор (Средн. 3)")
    notebook.add(tab_color, text="ветная панель (Средн. 9)")
    notebook.add(tab_clicker, text="ликер (овыш. 3)")
    notebook.add(tab_db, text="SQLite GUI (овыш. 7)")

    return root


def main() -> None:
    app = create_application()
    app.mainloop()


if __name__ == "__main__":
    main()
