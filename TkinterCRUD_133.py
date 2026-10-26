import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATA LAYER (SQLite Database Operations) ---
DB_NAME = "nilai_siswa.db"

def run_query(sql, params=()):
    """Helper function untuk menjalankan query SQL secara aman."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:  # Otomatis melakukan commit atau rollback jika ada error
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()
