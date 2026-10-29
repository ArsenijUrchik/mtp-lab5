import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class ClickerGameFrame(ttk.Frame):
    """овышенная сложность  3: гра «ликер» со счётом и апгрейдами."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=12)
        self.score: int = 0
        self.points_per_click: int = 1
        self.upgrade_cost: int = 10
        self._build_ui()

    def _build_ui(self) -> None:
        title = ttk.Label(self, text="гра «ликер»", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(0, 6))

        self.lbl_score = ttk.Label(self, text="чки: 0", font=("Segoe UI", 16, "bold"))
        self.lbl_score.pack(pady=6)

        self.lbl_rate = ttk.Label(self, text="Сила клика: +1 | Стоимость улучшения: 10", font=("Segoe UI", 9))
        self.lbl_rate.pack(pady=2)

        self.btn_click = ttk.Button(self, text="ТЬ!", width=20, command=self._on_click)
        self.btn_click.pack(pady=10)

        self.btn_upgrade = ttk.Button(self, text="упить улучшение (+1 к клику)", command=self._on_upgrade)
        self.btn_upgrade.pack(pady=4)

        btn_reset = ttk.Button(self, text="Сброс игры", command=self._reset)
        btn_reset.pack(pady=(8, 0))

    def _on_click(self) -> None:
        self.score += self.points_per_click
        self._update_labels()

    def _on_upgrade(self) -> None:
        if self.score >= self.upgrade_cost:
            self.score -= self.upgrade_cost
            self.points_per_click += 1
            self.upgrade_cost = int(self.upgrade_cost * 1.8)
            self._update_labels()
        else:
            messagebox.showinfo("едостаточно очков", f"ля апгрейда нужно {self.upgrade_cost} очков.")

    def _reset(self) -> None:
        self.score = 0
        self.points_per_click = 1
        self.upgrade_cost = 10
        self._update_labels()

    def _update_labels(self) -> None:
        self.lbl_score.config(text=f"чки: {self.score}")
        self.lbl_rate.config(
            text=f"Сила клика: +{self.points_per_click} | Стоимость улучшения: {self.upgrade_cost}"
        )


class SQLiteManagerFrame(ttk.Frame):
    """овышенная сложность  7: GUI для управления базой данных SQLite."""

    def __init__(self, parent: tk.Widget, db_path: str = "lab5_database.db") -> None:
        super().__init__(parent, padding=10)
        self.db_path = db_path
        self._init_db()
        self._build_ui()
        self.refresh_records()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
                """
            )

    def _build_ui(self) -> None:
        input_frame = ttk.LabelFrame(self, text="овая запись", padding=8)
        input_frame.pack(fill="x", padx=4, pady=4)

        ttk.Label(input_frame, text="мя:").grid(row=0, column=0, sticky="w", padx=3, pady=2)
        self.ent_name = ttk.Entry(input_frame, width=16)
        self.ent_name.grid(row=0, column=1, padx=3, pady=2)

        ttk.Label(input_frame, text="атегория:").grid(row=0, column=2, sticky="w", padx=3, pady=2)
        self.ent_cat = ttk.Entry(input_frame, width=14)
        self.ent_cat.grid(row=0, column=3, padx=3, pady=2)

        ttk.Label(input_frame, text="Телефон:").grid(row=0, column=4, sticky="w", padx=3, pady=2)
        self.ent_phone = ttk.Entry(input_frame, width=14)
        self.ent_phone.grid(row=0, column=5, padx=3, pady=2)

        btn_add = ttk.Button(input_frame, text="обавить", command=self.add_record)
        btn_add.grid(row=0, column=6, padx=6, pady=2)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=4, pady=6)

        columns = ("id", "name", "category", "phone")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text=" / онтакт")
        self.tree.heading("category", text="атегория")
        self.tree.heading("phone", text="Телефон")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("phone", width=120, anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        btn_box = ttk.Frame(self)
        btn_box.pack(fill="x", padx=4, pady=4)
        ttk.Button(btn_box, text="далить выбранное", command=self.delete_selected).pack(side="left", padx=4)
        ttk.Button(btn_box, text="бновить таблицу", command=self.refresh_records).pack(side="left", padx=4)

    def add_record(self) -> None:
        name = self.ent_name.get().strip()
        cat = self.ent_cat.get().strip()
        phone = self.ent_phone.get().strip()

        if not name or not cat or not phone:
            messagebox.showwarning("алидация", "се поля должны быть заполнены.")
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO contacts (name, category, phone) VALUES (?, ?, ?)",
                (name, cat, phone)
            )
        self.ent_name.delete(0, tk.END)
        self.ent_cat.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.refresh_records()

    def refresh_records(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, category, phone FROM contacts ORDER BY id ASC")
            for record in cursor.fetchall():
                self.tree.insert("", tk.END, values=record)

    def delete_selected(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("ыбор записи", "ыберите строку в таблице для удаления.")
            return

        rec_values = self.tree.item(selected_item[0], "values")
        record_id = rec_values[0]

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM contacts WHERE id = ?", (record_id,))
        self.refresh_records()
